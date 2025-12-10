import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const resumeService = {
  // Health check
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Upload resume file
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Extract keywords from resume
  extractKeywords: async (text) => {
    const response = await api.post('/keywords', { text });
    return response.data;
  },

  // Analyze resume against job description
  analyzeResume: async (resume, jobDescription) => {
    const response = await api.post('/analyze', {
      resume,
      job_description: jobDescription,
    });
    return response.data;
  },

  // Optimize resume content
  optimizeResume: async (resume, jobDescription, section = 'full') => {
    const response = await api.post('/optimize', {
      resume,
      job_description: jobDescription,
      section,
    });
    return response.data;
  },

  // Get improvement suggestions
  getSuggestions: async (resume, jobDescription) => {
    const response = await api.post('/suggest-improvements', {
      resume,
      job_description: jobDescription,
    });
    return response.data;
  },
};
