import React from 'react';
import './KeywordDisplay.css';

function KeywordDisplay({ keywords, title }) {
  if (!keywords || keywords.length === 0) {
    return null;
  }

  return (
    <div className="keyword-display">
      <h3>{title || 'Keywords'}</h3>
      <div className="keyword-grid">
        {keywords.map((keyword, index) => (
          <span key={index} className="keyword-tag">
            {keyword}
          </span>
        ))}
      </div>
    </div>
  );
}

export default KeywordDisplay;
