import React, { useState } from 'react';
import { equipmentAPI } from '../api';
import './CSVUpload.css';

function CSVUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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

    try {
      const response = await equipmentAPI.uploadCSV(file);
      setFile(null);
      // Pass success message to parent component
      onUploadSuccess('Upload successful', response.data.total_records);
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

      <form onSubmit={handleUpload}>
        <div className="upload-steps">
          <div className="step-indicator">
            <span className={`step-number ${file ? 'completed' : 'active'}`}>1</span>
            <span className="step-label">Choose File</span>
          </div>
          <div className="step-connector"></div>
          <div className="step-indicator">
            <span className={`step-number ${file ? 'active' : ''}`}>2</span>
            <span className="step-label">Upload</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="file-input" className="file-input-label">
            <i className="fas fa-folder-open"></i>
            <span className="button-text">
              <strong>Choose File from Computer</strong>
              <small>Click here to browse and select your CSV file</small>
            </span>
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
            <div className="file-info">
              <i className="fas fa-file-csv"></i>
              <div>
                <p>
                  <strong>Selected file:</strong> {file.name}
                </p>
                <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
              </div>
              <button
                type="button"
                className="btn-remove"
                onClick={() => setFile(null)}
                title="Remove file"
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
          </div>
        )}

        <button
          type="submit"
          className={`btn btn-primary ${!file ? 'btn-disabled-hint' : ''}`}
          disabled={loading || !file}
          title={!file ? 'Please select a file first' : 'Click to upload the selected file'}
        >
          <i className="fas fa-cloud-upload-alt"></i>
          {loading ? 'Uploading...' : file ? 'Upload File to Server' : 'Select a file first'}
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
