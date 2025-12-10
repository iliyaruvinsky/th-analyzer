import React, { useState } from 'react';

export interface FilterValues {
  focusArea: string;
  module: string;
  severity: string;
}

interface SidebarFiltersProps {
  filters: FilterValues;
  onFilterChange: (filters: FilterValues) => void;
  onClearFilters: () => void;
  focusAreaOptions: string[];
  moduleOptions: string[];
  severityOptions: string[];
  hasActiveFilters: boolean;
}

const SidebarFilters: React.FC<SidebarFiltersProps> = ({
  filters,
  onFilterChange,
  onClearFilters,
  focusAreaOptions,
  moduleOptions,
  severityOptions,
  hasActiveFilters,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = (field: keyof FilterValues, value: string) => {
    onFilterChange({
      ...filters,
      [field]: value,
    });
  };

  const activeFilterCount = [filters.focusArea, filters.module, filters.severity].filter(Boolean).length;

  return (
    <div className={`sidebar-filters ${isExpanded ? 'expanded' : 'collapsed'}`}>
      {/* Collapsible Header */}
      <div
        className="filters-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="filters-title">
          <span className="filter-icon">⊞</span>
          Filters
          {activeFilterCount > 0 && (
            <span className="active-filter-count">{activeFilterCount}</span>
          )}
        </span>
        <span className="filters-chevron">{isExpanded ? '▲' : '▼'}</span>
      </div>

      {/* Filter Content - Only shown when expanded */}
      {isExpanded && (
        <div className="filters-content">
          <div className="filter-row">
            <label className="filter-label">Focus Area</label>
            <select
              className="filter-select"
              value={filters.focusArea}
              onChange={(e) => handleChange('focusArea', e.target.value)}
            >
              <option value="">All Areas</option>
              {focusAreaOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-row">
            <label className="filter-label">Module</label>
            <select
              className="filter-select"
              value={filters.module}
              onChange={(e) => handleChange('module', e.target.value)}
            >
              <option value="">All Modules</option>
              {moduleOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-row">
            <label className="filter-label">Severity</label>
            <select
              className="filter-select"
              value={filters.severity}
              onChange={(e) => handleChange('severity', e.target.value)}
            >
              <option value="">All Severities</option>
              {severityOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>

          {hasActiveFilters && (
            <button className="clear-filters-btn" onClick={onClearFilters}>
              Clear Filters
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default SidebarFilters;
