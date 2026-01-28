import React, { useState, useMemo } from 'react';
import { equipmentAPI } from '../api';
import './History.css';

function History({ history, onGeneratePDF }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'uploaded_at', direction: 'desc' });
  const [viewingData, setViewingData] = useState(null);
  const [modalData, setModalData] = useState([]);
  const [loadingModal, setLoadingModal] = useState(false);

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

  const handleViewData = async (upload) => {
    setViewingData(upload);
    setLoadingModal(true);
    try {
      // Fetch all equipment for this user (filtered by backend)
      const response = await equipmentAPI.getAll();

      // Handle both array and paginated response formats
      const equipmentData = Array.isArray(response.data)
        ? response.data
        : (response.data?.results || []);

      console.log('Equipment data:', equipmentData);
      console.log('Looking for upload ID:', upload.id);

      // Filter client-side for this specific upload
      const uploadEquipment = equipmentData.filter(eq => {
        return eq.upload === upload.id;
      });

      console.log('Filtered equipment:', uploadEquipment);
      setModalData(uploadEquipment);
    } catch (err) {
      console.error('Failed to load equipment data:', err);
      setModalData([]);
    } finally {
      setLoadingModal(false);
    }
  };

  const closeModal = () => {
    setViewingData(null);
    setModalData([]);
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
            <div key={item.id} className="history-card">
              <div className="card-top">
                <div className="title-row">
                  <h4>{item.filename}</h4>
                  <span className="history-date">
                    {new Date(item.uploaded_at).toLocaleString('en-US', {
                      month: 'short', day: 'numeric', year: 'numeric',
                      hour: 'numeric', minute: '2-digit', hour12: true
                    })}
                  </span>
                </div>
                <div className="meta-row">
                  <span className="main-stat">Total: {item.total_records}</span>
                  <span className="divider">|</span>
                  <span>Avg Flow: {Number(item.avg_flowrate ?? 0).toFixed(2)}</span>
                  <span className="divider">|</span>
                  <span>Avg Pressure: {Number(item.avg_pressure ?? 0).toFixed(2)}</span>
                  <span className="divider">|</span>
                  <span>Avg Temp: {Number(item.avg_temperature ?? 0).toFixed(2)}</span>
                </div>
              </div>

              <div className="distribution-bar">
                {Object.entries(item.equipment_distribution || {}).map(([type, count], idx) => (
                  <div
                    key={type}
                    className={`bar-segment seg-${idx % 6}`}
                    style={{ flex: count }}
                    title={`${type}: ${count}`}
                  >
                    {type.charAt(0).toUpperCase() + type.slice(1)} — {count}
                  </div>
                ))}
              </div>

              <div className="card-actions">
                <button className="btn-view-data" onClick={() => handleViewData(item)}>
                  View original data
                </button>
                <button
                  className="btn-download-pdf"
                  onClick={() => onGeneratePDF(item.id)}
                  title="Download PDF Report"
                >
                  <i className="fas fa-file-pdf"></i>
                </button>
              </div>
            </div>
          ))
        ) : (
          <p className="no-match">No files match your search.</p>
        )}
      </div>

      {/* Modal for viewing original data */}
      {viewingData && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Original Data: {viewingData.filename}</h3>
              <button className="modal-close" onClick={closeModal}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            <div className="modal-body">
              {loadingModal ? (
                <div className="modal-loading">Loading data...</div>
              ) : modalData.length > 0 ? (
                <div className="data-table-wrapper">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Equipment Name</th>
                        <th>Type</th>
                        <th>Flowrate</th>
                        <th>Pressure</th>
                        <th>Temperature</th>
                      </tr>
                    </thead>
                    <tbody>
                      {modalData.map((item, idx) => (
                        <tr key={idx}>
                          <td>{item.equipment_name}</td>
                          <td>{item.equipment_type}</td>
                          <td>{Number(item.flowrate).toFixed(2)}</td>
                          <td>{Number(item.pressure).toFixed(2)}</td>
                          <td>{Number(item.temperature).toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="modal-no-data">No equipment data found</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default History;
