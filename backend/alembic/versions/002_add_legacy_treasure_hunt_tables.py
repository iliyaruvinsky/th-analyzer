"""Add legacy Treasure Hunt Analyzer tables

Revision ID: 002_legacy_tha_tables
Revises: 001_dashboard_tables
Create Date: 2025-12-10

Creates the following legacy THA tables that were previously created by init_db.py:
1. focus_areas - 6 focus area classifications
2. issue_types - Issue type classifications under focus areas
3. issue_groups - Aggregated issue groups per analysis run
4. data_sources - Uploaded file metadata
5. alerts - Parsed 4C alert data
6. alert_metadata - Alert metadata from Skywind exports
7. soda_reports - Parsed SoDA report data
8. soda_report_metadata - SoDA report metadata
9. findings - Detected issues/risks
10. risk_assessments - Risk scores (0-100)
11. money_loss_calculations - Financial impact estimates
12. analysis_runs - Execution tracking
13. audit_logs - Audit trail
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_legacy_tha_tables'
down_revision = '001_dashboard_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Create focus_areas table
    op.create_table(
        'focus_areas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_focus_areas_id', 'focus_areas', ['id'], unique=False)
    op.create_index('ix_focus_areas_code', 'focus_areas', ['code'], unique=True)

    # 2. Create issue_types table
    op.create_table(
        'issue_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('focus_area_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('default_severity', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['focus_area_id'], ['focus_areas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_issue_types_id', 'issue_types', ['id'], unique=False)
    op.create_index('ix_issue_types_code', 'issue_types', ['code'], unique=True)

    # 3. Create data_sources table
    op.create_table(
        'data_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('file_format', sa.Enum('pdf', 'csv', 'docx', 'xlsx', 'json', name='fileformat'), nullable=False),
        sa.Column('data_type', sa.Enum('alert', 'report', name='datasourcetype'), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('alert_id', sa.String(), nullable=True),
        sa.Column('report_type', sa.String(), nullable=True),
        sa.Column('upload_date', sa.DateTime(), nullable=False),
        sa.Column('uploaded_by', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_data_sources_id', 'data_sources', ['id'], unique=False)
    op.create_index('ix_data_sources_filename', 'data_sources', ['filename'], unique=False)
    op.create_index('ix_data_sources_alert_id', 'data_sources', ['alert_id'], unique=False)

    # 4. Create analysis_runs table
    op.create_table(
        'analysis_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=True),
        sa.Column('run_name', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('total_findings', sa.Integer(), nullable=True),
        sa.Column('findings_by_focus_area', sa.JSON(), nullable=True),
        sa.Column('findings_by_issue_type', sa.JSON(), nullable=True),
        sa.Column('total_risk_score', sa.Integer(), nullable=True),
        sa.Column('total_money_loss', sa.Float(), nullable=True),
        sa.Column('analysis_config', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_analysis_runs_id', 'analysis_runs', ['id'], unique=False)
    op.create_index('ix_analysis_runs_data_source_id', 'analysis_runs', ['data_source_id'], unique=False)

    # 5. Create issue_groups table (depends on issue_types and analysis_runs)
    op.create_table(
        'issue_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issue_type_id', sa.Integer(), nullable=False),
        sa.Column('analysis_run_id', sa.Integer(), nullable=False),
        sa.Column('finding_count', sa.Integer(), nullable=True),
        sa.Column('total_risk_score', sa.Integer(), nullable=True),
        sa.Column('total_money_loss', sa.Float(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['issue_type_id'], ['issue_types.id'], ),
        sa.ForeignKeyConstraint(['analysis_run_id'], ['analysis_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_issue_groups_id', 'issue_groups', ['id'], unique=False)

    # 6. Create alert_metadata table
    op.create_table(
        'alert_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('alert_name', sa.String(), nullable=False),
        sa.Column('alert_id', sa.String(), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('filter_criteria', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('data_source_id')
    )
    op.create_index('ix_alert_metadata_id', 'alert_metadata', ['id'], unique=False)
    op.create_index('ix_alert_metadata_alert_name', 'alert_metadata', ['alert_name'], unique=False)
    op.create_index('ix_alert_metadata_alert_id', 'alert_metadata', ['alert_id'], unique=False)

    # 7. Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('application_server', sa.String(), nullable=True),
        sa.Column('user_name', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('client', sa.String(), nullable=True),
        sa.Column('terminal', sa.String(), nullable=True),
        sa.Column('transaction_code', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('duration_unit', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('memory_consumption', sa.Integer(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('raw_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_alerts_id', 'alerts', ['id'], unique=False)
    op.create_index('ix_alerts_user_name', 'alerts', ['user_name'], unique=False)
    op.create_index('ix_alerts_timestamp', 'alerts', ['timestamp'], unique=False)

    # 8. Create soda_report_metadata table
    op.create_table(
        'soda_report_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('report_type', sa.String(), nullable=False),
        sa.Column('report_date', sa.DateTime(), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('kpis', sa.JSON(), nullable=True),
        sa.Column('result_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('data_source_id')
    )
    op.create_index('ix_soda_report_metadata_id', 'soda_report_metadata', ['id'], unique=False)
    op.create_index('ix_soda_report_metadata_report_type', 'soda_report_metadata', ['report_type'], unique=False)

    # 9. Create soda_reports table
    op.create_table(
        'soda_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('user_name', sa.String(), nullable=True),
        sa.Column('role_name', sa.String(), nullable=True),
        sa.Column('transaction_code', sa.String(), nullable=True),
        sa.Column('authorization_object', sa.String(), nullable=True),
        sa.Column('violation_type', sa.String(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('raw_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_soda_reports_id', 'soda_reports', ['id'], unique=False)
    op.create_index('ix_soda_reports_user_name', 'soda_reports', ['user_name'], unique=False)
    op.create_index('ix_soda_reports_role_name', 'soda_reports', ['role_name'], unique=False)

    # 10. Create findings table
    op.create_table(
        'findings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source_id', sa.Integer(), nullable=False),
        sa.Column('alert_id', sa.Integer(), nullable=True),
        sa.Column('soda_report_id', sa.Integer(), nullable=True),
        sa.Column('focus_area_id', sa.Integer(), nullable=False),
        sa.Column('issue_type_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('classification_confidence', sa.Float(), nullable=True),
        # Alert source tracking
        sa.Column('source_alert_id', sa.String(), nullable=True),
        sa.Column('source_alert_name', sa.String(), nullable=True),
        sa.Column('source_module', sa.String(), nullable=True),
        sa.Column('source_directory', sa.String(), nullable=True),
        # Report storage
        sa.Column('markdown_report', sa.Text(), nullable=True),
        sa.Column('report_path', sa.String(), nullable=True),
        sa.Column('report_level', sa.String(), nullable=True),
        sa.Column('key_findings_json', sa.JSON(), nullable=True),
        # Analysis status
        sa.Column('analysis_status', sa.String(), nullable=True),
        sa.Column('analysis_error', sa.Text(), nullable=True),
        # Timestamps
        sa.Column('detected_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
        sa.ForeignKeyConstraint(['alert_id'], ['alerts.id'], ),
        sa.ForeignKeyConstraint(['soda_report_id'], ['soda_reports.id'], ),
        sa.ForeignKeyConstraint(['focus_area_id'], ['focus_areas.id'], ),
        sa.ForeignKeyConstraint(['issue_type_id'], ['issue_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_findings_id', 'findings', ['id'], unique=False)

    # 11. Create risk_assessments table
    op.create_table(
        'risk_assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('finding_id', sa.Integer(), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=False),
        sa.Column('risk_level', sa.String(), nullable=False),
        sa.Column('risk_category', sa.String(), nullable=True),
        sa.Column('risk_description', sa.Text(), nullable=True),
        sa.Column('risk_factors', sa.JSON(), nullable=True),
        sa.Column('potential_impact', sa.Text(), nullable=True),
        sa.Column('affected_systems', sa.JSON(), nullable=True),
        sa.Column('affected_users', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['finding_id'], ['findings.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('finding_id')
    )
    op.create_index('ix_risk_assessments_id', 'risk_assessments', ['id'], unique=False)

    # 12. Create money_loss_calculations table
    op.create_table(
        'money_loss_calculations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('finding_id', sa.Integer(), nullable=False),
        sa.Column('estimated_loss', sa.Float(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('calculation_method', sa.String(), nullable=True),
        sa.Column('llm_estimate', sa.Float(), nullable=True),
        sa.Column('ml_estimate', sa.Float(), nullable=True),
        sa.Column('final_estimate', sa.Float(), nullable=True),
        sa.Column('calculation_details', sa.JSON(), nullable=True),
        sa.Column('reasoning', sa.Text(), nullable=True),
        sa.Column('factors_considered', sa.JSON(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['finding_id'], ['findings.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('finding_id')
    )
    op.create_index('ix_money_loss_calculations_id', 'money_loss_calculations', ['id'], unique=False)

    # 13. Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=True),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('user_ip', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_audit_logs_id', 'audit_logs', ['id'], unique=False)
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key dependencies)
    op.drop_table('audit_logs')
    op.drop_table('money_loss_calculations')
    op.drop_table('risk_assessments')
    op.drop_table('findings')
    op.drop_table('soda_reports')
    op.drop_table('soda_report_metadata')
    op.drop_table('alerts')
    op.drop_table('alert_metadata')
    op.drop_table('issue_groups')
    op.drop_table('analysis_runs')
    op.drop_table('data_sources')
    op.drop_table('issue_types')
    op.drop_table('focus_areas')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS fileformat")
    op.execute("DROP TYPE IF EXISTS datasourcetype")
