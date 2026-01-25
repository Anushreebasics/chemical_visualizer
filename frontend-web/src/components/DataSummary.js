import React from 'react';
import './DataSummary.css';

function DataSummary({ data, onGeneratePDF, onUploadClick }) {
  const {
    total_count,
    avg_flowrate,
    avg_pressure,
    avg_temperature,
    equipment_type_distribution,
  } = data;

  return (
    <div className="data-summary">
      <div className="summary-header">
        <h2>Data Summary</h2>
        <div className="summary-actions">
          <button className="btn btn-primary" onClick={() => onGeneratePDF()}>
            <i className="fas fa-file-pdf"></i> Generate PDF Report
          </button>
          {onUploadClick && (
            <button className="btn btn-secondary" onClick={onUploadClick}>
              <i className="fas fa-file-upload"></i> Upload New File
            </button>
          )}
        </div>
      </div>

      <div className="summary-stats">
        <div className="stat-card">
          <h3>Total Records</h3>
          <p className="stat-value">{total_count}</p>
        </div>

        <div className="stat-card">
          <h3>Avg Flowrate</h3>
          <p className="stat-value">{avg_flowrate.toFixed(2)}</p>
          <p className="stat-unit">m³/h</p>
        </div>

        <div className="stat-card">
          <h3>Avg Pressure</h3>
          <p className="stat-value">{avg_pressure.toFixed(2)}</p>
          <p className="stat-unit">bar</p>
        </div>

        <div className="stat-card">
          <h3>Avg Temperature</h3>
          <p className="stat-value">{avg_temperature.toFixed(2)}</p>
          <p className="stat-unit">°C</p>
        </div>
      </div>

      {Object.keys(equipment_type_distribution).length > 0 && (
        <div className="equipment-distribution">
          <h3>Equipment Type Distribution</h3>
          <ul className="distribution-list">
            {Object.entries(equipment_type_distribution).map(([type, count]) => (
              <li key={type}>
                <span className="type-label">{type}</span>
                <span className="type-count">{count}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default DataSummary;
