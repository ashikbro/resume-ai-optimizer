import React from 'react';
import './AnalysisResults.css';

function AnalysisResults({ analysis }) {
  if (!analysis) {
    return null;
  }

  const getScoreColor = (score) => {
    if (score >= 80) return '#48bb78';
    if (score >= 60) return '#ed8936';
    return '#f56565';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    return 'Needs Improvement';
  };

  return (
    <div className="analysis-results">
      <h3>ATS Compatibility Analysis</h3>
      
      <div className="score-container">
        <div className="score-circle" style={{ borderColor: getScoreColor(analysis.score) }}>
          <div className="score-value">{analysis.score}%</div>
          <div className="score-label">{getScoreLabel(analysis.score)}</div>
        </div>
      </div>

      <div className="analysis-details">
        {analysis.matched_keywords && analysis.matched_keywords.length > 0 && (
          <div className="detail-section matched">
            <h4>✓ Matched Keywords ({analysis.matched_keywords.length})</h4>
            <div className="keyword-list">
              {analysis.matched_keywords.map((keyword, index) => (
                <span key={index} className="keyword matched-keyword">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        {analysis.missing_keywords && analysis.missing_keywords.length > 0 && (
          <div className="detail-section missing">
            <h4>⚠ Missing Keywords ({analysis.missing_keywords.length})</h4>
            <div className="keyword-list">
              {analysis.missing_keywords.map((keyword, index) => (
                <span key={index} className="keyword missing-keyword">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        {analysis.suggestions && analysis.suggestions.length > 0 && (
          <div className="detail-section suggestions">
            <h4>💡 Suggestions</h4>
            <ul className="suggestion-list">
              {analysis.suggestions.map((suggestion, index) => (
                <li key={index}>{suggestion}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalysisResults;
