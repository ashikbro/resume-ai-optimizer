import React, { useState } from 'react';
import './FileUpload.css';

function FileUpload({ onFileUpload, loading }) {
  const [dragActive, setDragActive] = useState(false);
  const [fileName, setFileName] = useState('');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF, DOCX, or TXT file');
      return;
    }

    setFileName(file.name);
    onFileUpload(file);
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Your Resume</h2>
      <form 
        className={`upload-form ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          type="file"
          id="file-input"
          accept=".pdf,.docx,.txt"
          onChange={handleChange}
          disabled={loading}
        />
        <label htmlFor="file-input" className="file-label">
          <div className="upload-icon">📄</div>
          <p>
            {loading ? 'Uploading...' : fileName || 'Drag and drop your resume here or click to browse'}
          </p>
          <p className="file-types">Supported formats: PDF, DOCX, TXT</p>
        </label>
      </form>
      {fileName && !loading && (
        <div className="file-info">
          <span className="file-name">Selected: {fileName}</span>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
