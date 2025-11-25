"""
Diagnostic script to identify why analysis produces 0 findings
Run inside Docker: docker-compose exec backend python diagnose_analysis.py
"""
import sys
sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.data_source import DataSource
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata
from app.models.finding import Finding
from app.models.analysis_run import AnalysisRun
from app.models.focus_area import FocusArea
from app.models.issue_type import IssueType

def diagnose():
    db = SessionLocal()

    print("=" * 60)
    print("TREASURE HUNT ANALYZER - DIAGNOSTIC REPORT")
    print("=" * 60)

    # 1. Check Focus Areas (required for classification)
    print("\n1. FOCUS AREAS IN DATABASE:")
    focus_areas = db.query(FocusArea).all()
    if not focus_areas:
        print("   ❌ NO FOCUS AREAS FOUND - Run: python -m app.utils.init_db")
    else:
        print(f"   ✅ Found {len(focus_areas)} focus areas:")
        for fa in focus_areas:
            print(f"      - {fa.code}: {fa.name}")

    # 2. Check Issue Types (required for classification)
    print("\n2. ISSUE TYPES IN DATABASE:")
    issue_types = db.query(IssueType).all()
    if not issue_types:
        print("   ❌ NO ISSUE TYPES FOUND - Run: python -m app.utils.init_db")
    else:
        print(f"   ✅ Found {len(issue_types)} issue types")

    # 3. Check Data Sources
    print("\n3. DATA SOURCES (uploaded files):")
    data_sources = db.query(DataSource).all()
    if not data_sources:
        print("   ❌ NO DATA SOURCES - No files have been uploaded")
    else:
        print(f"   Found {len(data_sources)} data source(s):")
        for ds in data_sources:
            print(f"\n   ID: {ds.id}")
            print(f"   Filename: {ds.filename}")
            print(f"   Data Type: {ds.data_type}")
            print(f"   Status: {ds.status}")
            print(f"   Error: {ds.error_message or 'None'}")

    # 4. Check Alert Metadata & Alerts
    print("\n4. ALERT DATA:")
    alert_metadata = db.query(AlertMetadata).all()
    alerts = db.query(Alert).all()
    print(f"   AlertMetadata records: {len(alert_metadata)}")
    print(f"   Alert records: {len(alerts)}")

    if alert_metadata:
        for am in alert_metadata[:3]:  # Show first 3
            print(f"\n   AlertMetadata ID={am.id}:")
            print(f"      data_source_id: {am.data_source_id}")
            print(f"      alert_name: {am.alert_name}")
            print(f"      alert_id: {am.alert_id}")

    if alerts:
        print(f"\n   Sample Alert (first record):")
        a = alerts[0]
        print(f"      data_source_id: {a.data_source_id}")
        print(f"      user_name: {a.user_name}")
        print(f"      raw_data keys: {list(a.raw_data.keys())[:10] if a.raw_data else 'None'}...")

    # 5. Check SoDA Metadata & Reports
    print("\n5. SODA REPORT DATA:")
    soda_metadata = db.query(SoDAReportMetadata).all()
    soda_reports = db.query(SoDAReport).all()
    print(f"   SoDAReportMetadata records: {len(soda_metadata)}")
    print(f"   SoDAReport records: {len(soda_reports)}")

    # 6. Check Analysis Runs
    print("\n6. ANALYSIS RUNS:")
    analysis_runs = db.query(AnalysisRun).all()
    if not analysis_runs:
        print("   No analysis runs yet")
    else:
        print(f"   Found {len(analysis_runs)} analysis run(s):")
        for ar in analysis_runs:
            print(f"\n   Run ID: {ar.id}")
            print(f"      Status: {ar.status}")
            print(f"      data_source_id: {ar.data_source_id}")
            print(f"      Total Findings: {ar.total_findings}")
            print(f"      Error: {ar.error_message[:200] if ar.error_message else 'None'}")

    # 7. Check Findings
    print("\n7. FINDINGS:")
    findings = db.query(Finding).all()
    print(f"   Total findings: {len(findings)}")

    # 8. DIAGNOSIS
    print("\n" + "=" * 60)
    print("DIAGNOSIS:")
    print("=" * 60)

    issues = []

    if not focus_areas:
        issues.append("Focus areas not initialized - run: docker-compose exec backend python -m app.utils.init_db")

    if not issue_types:
        issues.append("Issue types not initialized - run: docker-compose exec backend python -m app.utils.init_db")

    if not data_sources:
        issues.append("No files uploaded - upload a file via the UI or API")
    else:
        for ds in data_sources:
            if ds.status == "error":
                issues.append(f"Data source {ds.id} ({ds.filename}) has error: {ds.error_message}")

    if data_sources and not alerts and not soda_reports:
        issues.append("Files uploaded but no Alert/SoDAReport records created - parsing may have failed")

    if alerts and not alert_metadata:
        issues.append("Alerts exist but no AlertMetadata - data saving is incomplete")

    if analysis_runs:
        for ar in analysis_runs:
            if ar.status == "failed":
                issues.append(f"Analysis run {ar.id} failed: {ar.error_message}")
            elif ar.total_findings == 0 and ar.status == "completed":
                # Check if data_source has data
                ds_id = ar.data_source_id
                if ds_id:
                    am_count = db.query(AlertMetadata).filter(AlertMetadata.data_source_id == ds_id).count()
                    a_count = db.query(Alert).filter(Alert.data_source_id == ds_id).count()
                    sm_count = db.query(SoDAReportMetadata).filter(SoDAReportMetadata.data_source_id == ds_id).count()
                    sr_count = db.query(SoDAReport).filter(SoDAReport.data_source_id == ds_id).count()

                    if am_count == 0 and sm_count == 0:
                        issues.append(f"Analysis run {ar.id}: No metadata for data_source {ds_id} - parsing didn't create AlertMetadata/SoDAReportMetadata")
                    elif a_count == 0 and sr_count == 0:
                        issues.append(f"Analysis run {ar.id}: No records for data_source {ds_id} - parsing didn't create Alert/SoDAReport records")

    if issues:
        print("\n❌ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ No obvious issues found. Check:")
        print("   - Are the uploaded files in correct format?")
        print("   - Check backend logs: docker-compose logs backend")

    print("\n" + "=" * 60)
    print("RECOMMENDED ACTIONS:")
    print("=" * 60)
    print("1. Initialize DB: docker-compose exec backend python -m app.utils.init_db")
    print("2. Upload a sample file via http://localhost:3010/upload")
    print("3. Run analysis: curl -X POST http://localhost:3011/api/v1/analysis/run -H 'Content-Type: application/json' -d '{\"data_source_id\": 1}'")
    print("4. Check logs: docker-compose logs -f backend")

    db.close()

if __name__ == "__main__":
    diagnose()
