import React, { useState, useMemo } from 'react';
import './History.css';

function History({ history, onGeneratePDF }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'uploaded_at', direction: 'desc' });

  const list = Array.isArray(history)
    ? history
    : (history && Array.isArray(history.results) ? history.results : []);

  const processedData = useMemo(() => {
    let data = [...list];

    // Search Filter
    if (searchTerm) {
      data = data.filter(item =>
        item.filename.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Sort
    if (sortConfig.key) {
      data.sort((a, b) => {
        let aVal = a[sortConfig.key];
        let bVal = b[sortConfig.key];

        // Handle numeric conversion for stats
        if (['total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature'].includes(sortConfig.key)) {
          aVal = Number(aVal || 0);
          bVal = Number(bVal || 0);
        }
        // Handle dates
        if (sortConfig.key === 'uploaded_at') {
          aVal = new Date(aVal).getTime();
          bVal = new Date(bVal).getTime();
        }

        if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return data;
  }, [list, searchTerm, sortConfig]);

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const SortIcon = ({ colKey }) => {
    if (sortConfig.key !== colKey) return <i className="fas fa-sort" style={{ opacity: 0.3 }}></i>;
    return <i className={`fas fa-sort-${sortConfig.direction === 'asc' ? 'up' : 'down'}`}></i>;
  }

  if (!list || list.length === 0) {
    return (
      <div className="history">
        <h2>Upload History</h2>
        <p className="no-data">No uploads yet. Start by uploading a CSV file!</p>
      </div>
    );
  }

  return (
    <div className="history">
      <div className="history-header">
        <h2>Upload History</h2>
        <div className="history-controls">
          <div className="search-box">
            <i className="fas fa-search"></i>
            <input
              type="text"
              placeholder="Search filename..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          {/* Simple Sort Dropdown or Buttons */}
          <div className="sort-box">
            <span>Sort by:</span>
            <button onClick={() => handleSort('uploaded_at')} className={sortConfig.key === 'uploaded_at' ? 'active' : ''}>
              Date <SortIcon colKey="uploaded_at" />
            </button>
            <button onClick={() => handleSort('filename')} className={sortConfig.key === 'filename' ? 'active' : ''}>
              Name <SortIcon colKey="filename" />
            </button>
          </div>
        </div>
      </div>

      <div className="history-list">
        {processedData.length > 0 ? (
          processedData.map((item) => (
            <div key={item.id} className="history-item">
              <div className="history-info">
                <h4>{item.filename}</h4>
                <p className="history-date">
                  <i className="fas fa-calendar"></i> {new Date(item.uploaded_at).toLocaleString()}
                </p>
                <div className="history-stats">
                  <span className="stat">
                    <strong>Records:</strong> {item.total_records}
                  </span>
                  <span className="stat">
                    <strong>Avg Flowrate:</strong> {Number(item.avg_flowrate ?? 0).toFixed(2)}
                  </span>
                  <span className="stat">
                    <strong>Avg Pressure:</strong> {Number(item.avg_pressure ?? 0).toFixed(2)}
                  </span>
                  <span className="stat">
                    <strong>Avg Temp:</strong> {Number(item.avg_temperature ?? 0).toFixed(2)}°C
                  </span>
                </div>
              </div>
              <button
                className="btn btn-primary"
                onClick={() => onGeneratePDF(item.id)}
              >
                <i className="fas fa-download"></i> PDF
              </button>
            </div>
          ))
        ) : (
          <p className="no-match">No files match your search.</p>
        )}
      </div>
    </div>
  );
}

export default History;
