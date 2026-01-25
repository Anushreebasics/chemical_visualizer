import React, { useState } from 'react';
import { equipmentAPI } from '../api';
import './CSVUpload.css';

function CSVUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.csv')) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please select a valid CSV file');
      setFile(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await equipmentAPI.uploadCSV(file);
      setSuccess(`CSV uploaded successfully! ${response.data.total_records} records added.`);
      setFile(null);
      setTimeout(() => {
        setSuccess('');
        onUploadSuccess();
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="csv-upload">
      <h2>Upload CSV File</h2>
      <p className="description">
        Upload a CSV file with the following columns: Equipment Name, Type, Flowrate, Pressure, Temperature
      </p>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleUpload}>
        <div className="form-group">
          <label htmlFor="file-input" className="file-input-label">
            <i className="fas fa-cloud-upload-alt"></i> Select CSV File
          </label>
          <input
            type="file"
            id="file-input"
            accept=".csv"
            onChange={handleFileChange}
            disabled={loading}
            required
          />
        </div>

        {file && (
          <div className="file-selected">
            <p>
              <strong>Selected file:</strong> {file.name}
            </p>
            <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
          </div>
        )}

        <button type="submit" className="btn btn-primary" disabled={loading || !file}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      <div className="example-csv">
        <h3>Example CSV Format:</h3>
        <pre>Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,100.5,10.2,25.3
Reactor B,Reactor,50.2,15.8,60.5
Heat Exchanger C,Heat Exchanger,75.3,8.9,45.2</pre>
      </div>
    </div>
  );
}

export default CSVUpload;
