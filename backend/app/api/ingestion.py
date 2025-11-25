from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.data_source import DataSource, DataSourceType, FileFormat
from app.services.ingestion.parser_factory import ParserFactory
from app.services.ingestion.data_saver import DataSaver
from app.schemas.ingestion import DataSourceResponse, UploadResponse
from app.utils.audit_logger import audit_log
from pydantic import BaseModel

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse a file (PDF, CSV, DOCX, Excel)"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Check if parser can handle this file
    if not ParserFactory.can_parse_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file.filename}"
        )
    
    # Determine file format
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    try:
        file_format = FileFormat(file_ext)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file_ext}"
        )
    
    # Determine data type (alert or report)
    # Check for 4C alert patterns: _XXXXXX_XXXXXX (6 digits _ 6 digits)
    filename_lower = file.filename.lower()
    import re
    if 'alert' in filename_lower or 'slg_' in filename_lower or re.search(r'_\d{6}_\d{6}', file.filename):
        data_type = DataSourceType.ALERT
    # Check for SoDA report patterns
    elif any(pattern in filename_lower for pattern in ['avr_', 'pvr_', 'arp_', 'crv_', 'ivr_', 'rau_', 'tru_', 'uat_']):
        data_type = DataSourceType.REPORT
    else:
        # Default to ALERT for 4C files, REPORT for others
        data_type = DataSourceType.ALERT if file_ext == 'xlsx' else DataSourceType.REPORT
    
    # Create storage directory if it doesn't exist
    storage_path = Path(settings.STORAGE_PATH)
    storage_path.mkdir(parents=True, exist_ok=True)
    
    # Save file (with size limit check)
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    file_path = storage_path / f"{datetime.utcnow().timestamp()}_{file.filename}"
    try:
        # Read file in chunks to handle large files and check size
        file_size = 0
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(8192)  # Read 8KB chunks
                if not chunk:
                    break
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB"
                    )
                buffer.write(chunk)
        
    except HTTPException:
        # Re-raise HTTP exceptions (like file size limit)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Create data source record
    data_source = DataSource(
        filename=file.filename,
        original_filename=file.filename,
        file_format=file_format,
        data_type=data_type,
        file_size=file_size,
        file_path=str(file_path),
        status="pending"
    )
    
    db.add(data_source)
    db.commit()
    db.refresh(data_source)
    
    # Parse file
    parser = ParserFactory.get_parser(str(file_path))
    if not parser:
        # Try to diagnose why no parser was found
        from app.services.ingestion.excel_parser_4c import ExcelParser4C
        from app.services.ingestion.excel_parser_soda import ExcelParserSoDA
        from pathlib import Path as PathLib
        
        file_ext = PathLib(file_path).suffix.lower()
        filename = PathLib(file_path).stem
        diagnosis = []
        
        if file_ext == '.xlsx':
            parser_4c = ExcelParser4C()
            parser_soda = ExcelParserSoDA()
            can_parse_4c = parser_4c.can_parse(str(file_path))
            can_parse_soda = parser_soda.can_parse(str(file_path))
            diagnosis.append(f"4C parser can_parse: {can_parse_4c}")
            diagnosis.append(f"SoDA parser can_parse: {can_parse_soda}")
            
            # Check if file has Alert Parameters sheet
            try:
                import pandas as pd
                xl_file = pd.ExcelFile(file_path)
                has_alert_params = 'Alert Parameters' in xl_file.sheet_names
                diagnosis.append(f"Has 'Alert Parameters' sheet: {has_alert_params}")
                diagnosis.append(f"Sheet names: {xl_file.sheet_names}")
            except Exception as e:
                diagnosis.append(f"Error checking sheets: {str(e)}")
        
        error_msg = f"No parser available for this file: {file.filename}. Diagnosis: {'; '.join(diagnosis)}"
        data_source.status = "error"
        data_source.error_message = error_msg
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    try:
        parse_result = parser.parse(str(file_path))
        
        # Update data source with metadata
        if parse_result.get('metadata'):
            metadata = parse_result['metadata']
            
            # Extract alert_id or report_type from metadata
            if 'alert_id' in metadata:
                data_source.alert_id = metadata['alert_id']
            if 'report_type' in metadata:
                data_source.report_type = metadata['report_type']
        
        # Save parsed data to database
        data_saver = DataSaver(db)
        if data_source.data_type == DataSourceType.ALERT:
            try:
                data_saver.save_4c_alert(data_source, parse_result)
            except Exception as e:
                parse_result['errors'] = parse_result.get('errors', []) + [f"Error saving alerts: {str(e)}"]
        elif data_source.data_type == DataSourceType.REPORT:
            try:
                data_saver.save_soda_report(data_source, parse_result)
            except Exception as e:
                parse_result['errors'] = parse_result.get('errors', []) + [f"Error saving reports: {str(e)}"]
        
        data_source.status = "completed" if not parse_result.get('errors') else "error"
        if parse_result.get('errors'):
            data_source.error_message = '; '.join(parse_result['errors'])
        
        db.commit()
        
        # Log the upload
        user_ip = request.client.host if request else None
        user_agent = request.headers.get("user-agent") if request else None
        audit_log(
            db=db,
            action="upload",
            entity_type="data_source",
            entity_id=data_source.id,
            user_ip=user_ip,
            user_agent=user_agent,
            description=f"Uploaded file: {file.filename}",
            details={
                "filename": file.filename,
                "file_format": data_source.file_format,
                "data_type": data_source.data_type,
                "file_size": data_source.file_size,
                "status": data_source.status,
                "records_count": len(parse_result.get('data', []))
            },
            status="success" if data_source.status == "completed" else "error",
            error_message=data_source.error_message if data_source.status == "error" else None
        )
        
        return UploadResponse(
            data_source_id=data_source.id,
            filename=file.filename or "unknown",
            status=data_source.status,
            parse_result=parse_result
        )
        
    except Exception as e:
        db.rollback()  # Rollback any pending transaction
        data_source.status = "error"
        data_source.error_message = str(e)
        try:
            db.commit()
        except Exception:
            db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing file: {str(e)}"
        )


@router.post("/upload-artifacts")
async def upload_artifacts(
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload multiple artifact files for a single alert (Code, Explanation, Metadata, Summary).

    This endpoint accepts multiple files at once and groups them by alert.
    Files should be named:
    - Code_*.txt
    - Explanation_*.txt
    - Metadata_*.txt
    - Summary_*.xlsx (or .csv, .txt)
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )

    # Create storage directory
    storage_path = Path(settings.STORAGE_PATH)
    artifacts_path = storage_path / "artifacts" / f"{datetime.utcnow().timestamp()}"
    artifacts_path.mkdir(parents=True, exist_ok=True)

    saved_files = []
    artifact_types = {"code": None, "explanation": None, "metadata": None, "summary": None}

    for file in files:
        if not file.filename:
            continue

        # Determine artifact type
        filename_lower = file.filename.lower()
        artifact_type = None
        if filename_lower.startswith("code_"):
            artifact_type = "code"
        elif filename_lower.startswith("explanation_"):
            artifact_type = "explanation"
        elif filename_lower.startswith("metadata_"):
            artifact_type = "metadata"
        elif filename_lower.startswith("summary_"):
            artifact_type = "summary"

        # Save file
        file_path = artifacts_path / file.filename
        try:
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            saved_files.append({
                "filename": file.filename,
                "path": str(file_path),
                "type": artifact_type,
                "size": len(content)
            })

            if artifact_type:
                artifact_types[artifact_type] = str(file_path)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file {file.filename}: {str(e)}"
            )

    # Extract alert info from filenames
    alert_name = "Unknown Alert"
    alert_id = "unknown"
    for f in saved_files:
        if f["type"] == "summary" or f["type"] == "explanation":
            # Try to extract alert name from filename
            import re
            # Pattern: Type_AlertName_ID.ext
            match = re.match(r'^(?:summary|explanation|code|metadata)_(.+?)_(\d+_\d+)', f["filename"], re.IGNORECASE)
            if match:
                alert_name = match.group(1).replace('_', ' ')
                alert_id = match.group(2)
                break

    # Create data source record for the artifact bundle
    data_source = DataSource(
        filename=f"Artifacts: {alert_name}",
        original_filename=", ".join([f["filename"] for f in saved_files]),
        file_format=FileFormat.XLSX if artifact_types["summary"] and ".xlsx" in artifact_types["summary"] else FileFormat.TXT,
        data_type=DataSourceType.ALERT,
        file_size=sum(f["size"] for f in saved_files),
        file_path=str(artifacts_path),
        status="completed",
        alert_id=alert_id
    )

    db.add(data_source)
    db.commit()
    db.refresh(data_source)

    return {
        "data_source_id": data_source.id,
        "alert_name": alert_name,
        "alert_id": alert_id,
        "artifacts_path": str(artifacts_path),
        "files": saved_files,
        "artifact_types": {k: v is not None for k, v in artifact_types.items()},
        "message": f"Successfully uploaded {len(saved_files)} files. Use /content-analysis/analyze-directory to analyze."
    }


@router.get("/data-sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all uploaded data sources"""
    data_sources = db.query(DataSource).offset(skip).limit(limit).all()
    return [DataSourceResponse.model_validate(ds) for ds in data_sources]


@router.get("/data-sources/{data_source_id}", response_model=DataSourceResponse)
async def get_data_source(
    data_source_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific data source"""
    data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
    if not data_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    return DataSourceResponse.model_validate(data_source)

