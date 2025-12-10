import React, { useState } from 'react';
import './OptimizerPanel.css';

function OptimizerPanel({ resumeText, jobDescription, onOptimize, loading }) {
  const [section, setSection] = useState('full');
  const [optimizedText, setOptimizedText] = useState('');
  const [suggestions, setSuggestions] = useState('');

  const handleOptimize = async () => {
    const result = await onOptimize(section);
    if (result) {
      setOptimizedText(result);
    }
  };

  const handleGetSuggestions = async () => {
    const result = await onOptimize('suggestions');
    if (result) {
      setSuggestions(result);
    }
  };

  const canOptimize = resumeText && jobDescription && !loading;

  return (
    <div className="optimizer-panel">
      <h3>AI-Powered Optimization</h3>
      
      <div className="optimizer-controls">
        <div className="section-selector">
          <label htmlFor="section-select">Optimize Section:</label>
          <select 
            id="section-select"
            value={section} 
            onChange={(e) => setSection(e.target.value)}
            disabled={loading}
          >
            <option value="full">Full Resume</option>
            <option value="summary">Professional Summary</option>
            <option value="experience">Work Experience</option>
            <option value="skills">Skills</option>
          </select>
        </div>

        <div className="action-buttons">
          <button 
            onClick={handleOptimize}
            disabled={!canOptimize}
            className="btn btn-primary"
          >
            {loading ? 'Optimizing...' : 'Optimize Resume'}
          </button>
          <button 
            onClick={handleGetSuggestions}
            disabled={!canOptimize}
            className="btn btn-secondary"
          >
            {loading ? 'Getting Suggestions...' : 'Get Suggestions'}
          </button>
        </div>
      </div>

      {optimizedText && (
        <div className="result-section">
          <div className="result-header">
            <h4>Optimized Content</h4>
            <button 
              onClick={() => navigator.clipboard.writeText(optimizedText)}
              className="btn btn-small"
            >
              Copy to Clipboard
            </button>
          </div>
          <div className="result-content">
            <pre>{optimizedText}</pre>
          </div>
        </div>
      )}

      {suggestions && (
        <div className="result-section suggestions-section">
          <h4>AI Suggestions</h4>
          <div className="result-content">
            <pre>{suggestions}</pre>
          </div>
        </div>
      )}

      {!canOptimize && (
        <div className="info-message">
          <p>Please upload a resume and enter a job description to use optimization features.</p>
        </div>
      )}
    </div>
  );
}

export default OptimizerPanel;
