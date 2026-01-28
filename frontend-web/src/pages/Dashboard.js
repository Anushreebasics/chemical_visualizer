import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { equipmentAPI, authAPI } from '../api';
import CSVUpload from '../components/CSVUpload';
import DataSummary from '../components/DataSummary';
import Charts from '../components/Charts';
import History from '../components/History';
import './Dashboard.css';
import ThemeToggle from '../components/ThemeToggle';

function Dashboard({ setIsAuthenticated }) {
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [activeTab, setActiveTab] = useState('summary');
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [summaryRes, historyRes] = await Promise.all([
        equipmentAPI.getSummary(),
        equipmentAPI.getHistory(),
      ]);
      setSummary(summaryRes.data);
      const historyData = Array.isArray(historyRes.data)
        ? historyRes.data
        : (historyRes.data && Array.isArray(historyRes.data.results)
          ? historyRes.data.results
          : []);
      setHistory(historyData);
      setError('');
    } catch (err) {
      setError('Failed to load data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (message, recordCount) => {
    fetchData();
    // Show success message at the top of the page
    setSuccessMessage(`CSV uploaded successfully! ${recordCount} records added. Redirecting to summary...`);
    // Automatically navigate to summary page after successful upload
    setTimeout(() => {
      setActiveTab('summary');
      // Clear success message after navigation
      setTimeout(() => setSuccessMessage(''), 3000);
    }, 2000);
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.error(err);
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    navigate('/login');
  };

  const handleGeneratePDF = async (uploadId = null) => {
    try {
      const response = await equipmentAPI.generatePDF(uploadId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentElement.removeChild(link);
    } catch (err) {
      setError('Failed to generate PDF. Please try again.');
    }
  };

  if (loading) {
    return <div className="loader">Loading...</div>;
  }

  const NavItem = ({ id, icon, label }) => (
    <button
      className={`nav-item ${activeTab === id ? 'active' : ''}`}
      onClick={() => setActiveTab(id)}
      aria-current={activeTab === id ? 'page' : undefined}
    >
      <i className={`fa-solid ${icon}`}></i>
      <span>{label}</span>
    </button>
  );

  return (
    <div className="dashboard">
      <header className="header">
        <div className="header-content">
          <div className="brand">
            <div className="logo">CE</div>
            <div>
              <h1>Chemical Equipment Visualizer</h1>
              {user && <p className="user-info">Welcome, {user.first_name || user.username}!</p>}
            </div>
          </div>
          <div className="header-actions">
            <ThemeToggle />
            <button className="btn btn-danger" onClick={handleLogout}>
              <i className="fa-solid fa-right-from-bracket"></i>
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="layout">
        <aside className="sidebar" aria-label="Primary">
          <nav className="nav">
            <NavItem id="summary" icon="fa-gauge" label="Summary" />
            <NavItem id="charts" icon="fa-chart-line" label="Charts" />
            <NavItem id="upload" icon="fa-file-arrow-up" label="Upload CSV" />
            <NavItem id="history" icon="fa-clock-rotate-left" label="History" />
          </nav>

          <div className="sidebar-footer">
            <div className="user-chip">
              <div className="avatar">{(user?.first_name || user?.username || '?').charAt(0).toUpperCase()}</div>
              <div className="meta">
                <span className="name">{user?.first_name || user?.username || 'User'}</span>
                <span className="role">Signed in</span>
              </div>
            </div>
          </div>
        </aside>

        <section className="content">
          {error && <div className="alert alert-error">{error}</div>}
          {successMessage && <div className="alert alert-success">{successMessage}</div>}

          {activeTab === 'upload' && (
            <div className="panel card">
              <h2 className="panel-title"><i className="fa-solid fa-file-arrow-up"></i> Upload CSV</h2>
              <CSVUpload onUploadSuccess={handleUploadSuccess} />
            </div>
          )}

          {activeTab === 'summary' && summary && (
            <div className="panel card">
              <h2 className="panel-title"><i className="fa-solid fa-gauge"></i> Summary</h2>
              <DataSummary
                data={summary}
                onGeneratePDF={handleGeneratePDF}
                onUploadClick={() => setActiveTab('upload')}
              />
            </div>
          )}

          {activeTab === 'charts' && summary && (
            <div className="panel card">
              <h2 className="panel-title"><i className="fa-solid fa-chart-line"></i> Charts</h2>
              <Charts data={summary} />
            </div>
          )}

          {activeTab === 'history' && (
            <div className="panel card">
              <h2 className="panel-title"><i className="fa-solid fa-clock-rotate-left"></i> History</h2>
              <History history={history} onGeneratePDF={handleGeneratePDF} />
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
