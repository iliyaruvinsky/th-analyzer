"""Add alert analysis dashboard tables

Revision ID: 001_dashboard_tables
Revises:
Create Date: 2025-12-05

Creates the following tables for the Alert Analysis Dashboard:
1. clients - Company whose SAP we monitor
2. source_systems - SAP source systems
3. exception_indicators - EI definitions
4. ei_vocabulary - LLM-generated code interpretations
5. alert_instances - Alert configurations (EI + parameters)
6. alert_analyses - Analysis results per execution
7. critical_discoveries - Individual critical findings
8. key_findings - Top findings per analysis
9. concentration_metrics - Concentration data by dimension
10. action_items - Investigation queue with status tracking
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_dashboard_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Create clients table
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_clients_id', 'clients', ['id'], unique=False)
    op.create_index('ix_clients_code', 'clients', ['code'], unique=True)

    # 2. Create source_systems table
    op.create_table(
        'source_systems',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('system_type', sa.String(50), nullable=True),
        sa.Column('environment', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'code', name='uq_source_system_client_code')
    )
    op.create_index('ix_source_systems_id', 'source_systems', ['id'], unique=False)
    op.create_index('ix_source_systems_client_id', 'source_systems', ['client_id'], unique=False)

    # 3. Create exception_indicators table
    op.create_table(
        'exception_indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ei_id', sa.String(50), nullable=False),
        sa.Column('function_name', sa.String(100), nullable=True),
        sa.Column('module', sa.String(10), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_exception_indicators_id', 'exception_indicators', ['id'], unique=False)
    op.create_index('ix_exception_indicators_ei_id', 'exception_indicators', ['ei_id'], unique=True)
    op.create_index('ix_exception_indicators_module', 'exception_indicators', ['module'], unique=False)

    # 4. Create ei_vocabulary table
    op.create_table(
        'ei_vocabulary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ei_id', sa.Integer(), nullable=False),
        sa.Column('source_tables', sa.JSON(), nullable=True),
        sa.Column('key_fields', sa.JSON(), nullable=True),
        sa.Column('data_selection_logic', sa.Text(), nullable=True),
        sa.Column('aggregation_logic', sa.Text(), nullable=True),
        sa.Column('threshold_fields', sa.JSON(), nullable=True),
        sa.Column('risk_patterns', sa.JSON(), nullable=True),
        sa.Column('interpretation_notes', sa.Text(), nullable=True),
        sa.Column('external_functions_needed', sa.JSON(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['ei_id'], ['exception_indicators.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ei_id')
    )
    op.create_index('ix_ei_vocabulary_id', 'ei_vocabulary', ['id'], unique=False)

    # 5. Create alert_instances table
    op.create_table(
        'alert_instances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_id', sa.String(50), nullable=False),
        sa.Column('alert_name', sa.String(255), nullable=False),
        sa.Column('ei_id', sa.Integer(), nullable=True),
        sa.Column('source_system_id', sa.Integer(), nullable=True),
        sa.Column('focus_area', sa.String(50), nullable=False),
        sa.Column('subcategory', sa.String(100), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('business_purpose', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['ei_id'], ['exception_indicators.id'], ),
        sa.ForeignKeyConstraint(['source_system_id'], ['source_systems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_alert_instances_id', 'alert_instances', ['id'], unique=False)
    op.create_index('ix_alert_instances_alert_id', 'alert_instances', ['alert_id'], unique=True)
    op.create_index('ix_alert_instances_ei_id', 'alert_instances', ['ei_id'], unique=False)
    op.create_index('ix_alert_instances_source_system_id', 'alert_instances', ['source_system_id'], unique=False)
    op.create_index('ix_alert_instances_focus_area', 'alert_instances', ['focus_area'], unique=False)

    # 6. Create alert_analyses table
    op.create_table(
        'alert_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_instance_id', sa.Integer(), nullable=False),
        sa.Column('analysis_type', sa.String(20), nullable=False),
        sa.Column('execution_date', sa.Date(), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=True),
        sa.Column('period_end', sa.Date(), nullable=True),
        sa.Column('records_affected', sa.Integer(), nullable=True),
        sa.Column('unique_entities', sa.Integer(), nullable=True),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('fraud_indicator', sa.String(50), nullable=True),
        sa.Column('financial_impact_local', sa.Numeric(18, 2), nullable=True),
        sa.Column('financial_impact_usd', sa.Numeric(18, 2), nullable=True),
        sa.Column('local_currency', sa.String(10), nullable=True),
        sa.Column('exchange_rate', sa.Numeric(10, 4), nullable=True),
        sa.Column('report_path', sa.String(500), nullable=True),
        sa.Column('raw_summary_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['alert_instance_id'], ['alert_instances.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_alert_analyses_id', 'alert_analyses', ['id'], unique=False)
    op.create_index('ix_alert_analyses_alert_instance_id', 'alert_analyses', ['alert_instance_id'], unique=False)
    op.create_index('ix_alert_analyses_analysis_type', 'alert_analyses', ['analysis_type'], unique=False)
    op.create_index('ix_alert_analyses_execution_date', 'alert_analyses', ['execution_date'], unique=False)
    op.create_index('ix_alert_analyses_severity', 'alert_analyses', ['severity'], unique=False)
    op.create_index('idx_alert_analyses_severity_date', 'alert_analyses', ['severity', 'execution_date'], unique=False)
    op.create_index('idx_alert_analyses_type_date', 'alert_analyses', ['analysis_type', 'execution_date'], unique=False)

    # 7. Create critical_discoveries table
    op.create_table(
        'critical_discoveries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_analysis_id', sa.Integer(), nullable=False),
        sa.Column('discovery_order', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('affected_entity', sa.String(255), nullable=True),
        sa.Column('affected_entity_id', sa.String(50), nullable=True),
        sa.Column('metric_value', sa.Numeric(18, 2), nullable=True),
        sa.Column('metric_unit', sa.String(50), nullable=True),
        sa.Column('percentage_of_total', sa.Numeric(5, 2), nullable=True),
        sa.Column('is_fraud_indicator', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['alert_analysis_id'], ['alert_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_critical_discoveries_id', 'critical_discoveries', ['id'], unique=False)
    op.create_index('ix_critical_discoveries_alert_analysis_id', 'critical_discoveries', ['alert_analysis_id'], unique=False)

    # 8. Create key_findings table
    op.create_table(
        'key_findings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_analysis_id', sa.Integer(), nullable=False),
        sa.Column('finding_rank', sa.Integer(), nullable=False),
        sa.Column('finding_text', sa.Text(), nullable=False),
        sa.Column('finding_category', sa.String(50), nullable=True),
        sa.Column('financial_impact_usd', sa.Numeric(18, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['alert_analysis_id'], ['alert_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_key_findings_id', 'key_findings', ['id'], unique=False)
    op.create_index('ix_key_findings_alert_analysis_id', 'key_findings', ['alert_analysis_id'], unique=False)

    # 9. Create concentration_metrics table
    op.create_table(
        'concentration_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_analysis_id', sa.Integer(), nullable=False),
        sa.Column('dimension_type', sa.String(50), nullable=False),
        sa.Column('dimension_code', sa.String(50), nullable=False),
        sa.Column('dimension_name', sa.String(255), nullable=True),
        sa.Column('record_count', sa.Integer(), nullable=True),
        sa.Column('value_local', sa.Numeric(18, 2), nullable=True),
        sa.Column('value_usd', sa.Numeric(18, 2), nullable=True),
        sa.Column('percentage_of_total', sa.Numeric(5, 2), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['alert_analysis_id'], ['alert_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_concentration_metrics_id', 'concentration_metrics', ['id'], unique=False)
    op.create_index('ix_concentration_metrics_alert_analysis_id', 'concentration_metrics', ['alert_analysis_id'], unique=False)
    op.create_index('ix_concentration_metrics_dimension_type', 'concentration_metrics', ['dimension_type'], unique=False)
    op.create_index('idx_concentration_type_code', 'concentration_metrics', ['dimension_type', 'dimension_code'], unique=False)

    # 10. Create action_items table
    op.create_table(
        'action_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_analysis_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(30), nullable=True),
        sa.Column('assigned_to', sa.String(100), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_by', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['alert_analysis_id'], ['alert_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_action_items_id', 'action_items', ['id'], unique=False)
    op.create_index('ix_action_items_alert_analysis_id', 'action_items', ['alert_analysis_id'], unique=False)
    op.create_index('ix_action_items_status', 'action_items', ['status'], unique=False)
    op.create_index('idx_action_items_status_priority', 'action_items', ['status', 'priority'], unique=False)
    op.create_index('idx_action_items_type_status', 'action_items', ['action_type', 'status'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key dependencies)
    op.drop_table('action_items')
    op.drop_table('concentration_metrics')
    op.drop_table('key_findings')
    op.drop_table('critical_discoveries')
    op.drop_table('alert_analyses')
    op.drop_table('alert_instances')
    op.drop_table('ei_vocabulary')
    op.drop_table('exception_indicators')
    op.drop_table('source_systems')
    op.drop_table('clients')
