import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import KeywordDisplay from './components/KeywordDisplay';
import AnalysisResults from './components/AnalysisResults';
import OptimizerPanel from './components/OptimizerPanel';
import { resumeService } from './services/api';
import './App.css';

function App() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [keywords, setKeywords] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await resumeService.checkHealth();
      setApiStatus(health);
    } catch (err) {
      console.error('API health check failed:', err);
      setApiStatus({ status: 'unhealthy' });
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError('');
    
    try {
      const result = await resumeService.uploadResume(file);
      
      if (result.success) {
        setResumeText(result.text);
        
        // Automatically extract keywords
        const keywordResult = await resumeService.extractKeywords(result.text);
        if (keywordResult.success) {
          setKeywords(keywordResult.keywords);
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload resume. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleAnalyze = async () => {
    if (!resumeText || !jobDescription) {
      setError('Please upload a resume and enter a job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await resumeService.analyzeResume(resumeText, jobDescription);
      
      if (result.success) {
        setAnalysis(result.analysis);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze resume. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async (section) => {
    if (!resumeText || !jobDescription) {
      setError('Please upload a resume and enter a job description');
      return null;
    }

    setLoading(true);
    setError('');

    try {
      if (section === 'suggestions') {
        const result = await resumeService.getSuggestions(resumeText, jobDescription);
        if (result.success) {
          return result.suggestions;
        }
      } else {
        const result = await resumeService.optimizeResume(resumeText, jobDescription, section);
        if (result.success) {
          return result.optimized_text;
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to optimize resume. Please check your OpenAI API key.');
      console.error('Optimization error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Resume AI Optimizer</h1>
        <p className="subtitle">Optimize your resume for ATS using AI-powered analysis</p>
        {apiStatus && (
          <div className={`api-status ${apiStatus.status === 'healthy' ? 'healthy' : 'unhealthy'}`}>
            API Status: {apiStatus.status || 'Unknown'}
            {apiStatus.spacy_loaded !== undefined && ` | spaCy: ${apiStatus.spacy_loaded ? '✓' : '✗'}`}
            {apiStatus.openai_configured !== undefined && ` | OpenAI: ${apiStatus.openai_configured ? '✓' : '✗'}`}
          </div>
        )}
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
            <button className="close-error" onClick={() => setError('')}>×</button>
          </div>
        )}

        <div className="content-grid">
          <div className="left-panel">
            <FileUpload onFileUpload={handleFileUpload} loading={loading} />

            {resumeText && (
              <div className="resume-preview">
                <h3>Resume Preview</h3>
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Your resume content will appear here..."
                  rows={10}
                />
              </div>
            )}

            {keywords.length > 0 && (
              <KeywordDisplay keywords={keywords} title="Extracted Keywords from Resume" />
            )}
          </div>

          <div className="right-panel">
            <div className="job-description-section">
              <h3>Job Description</h3>
              <textarea
                value={jobDescription}
                onChange={handleJobDescriptionChange}
                placeholder="Paste the job description here..."
                rows={10}
              />
              <button 
                onClick={handleAnalyze}
                disabled={!resumeText || !jobDescription || loading}
                className="btn btn-analyze"
              >
                {loading ? 'Analyzing...' : 'Analyze ATS Compatibility'}
              </button>
            </div>

            {analysis && <AnalysisResults analysis={analysis} />}

            <OptimizerPanel
              resumeText={resumeText}
              jobDescription={jobDescription}
              onOptimize={handleOptimize}
              loading={loading}
            />
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by OpenAI GPT, spaCy NLP, and Flask</p>
      </footer>
    </div>
  );
}

export default App;
