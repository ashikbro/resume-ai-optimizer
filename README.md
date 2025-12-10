# 🎯 Resume AI Optimizer

A powerful platform that dynamically optimizes resumes using AI based on job descriptions. Leverages GPT APIs, spaCy NLP, and Flask backend to provide ATS-optimized resume content with keyword suggestions and intelligent rewriting.

## ✨ Features

- **Resume Upload**: Support for PDF, DOCX, and TXT formats
- **Keyword Extraction**: Automatic keyword extraction using spaCy NLP
- **ATS Analysis**: Compatibility score and keyword matching against job descriptions
- **AI-Powered Optimization**: GPT-based resume rewriting for better job matches
- **Smart Suggestions**: Actionable recommendations for resume improvement
- **Interactive UI**: Modern React interface with real-time feedback

## 🏗️ Architecture

### Backend (Flask)
- **Flask REST API**: Handles resume processing and optimization
- **spaCy Integration**: NLP-powered keyword extraction and analysis
- **OpenAI GPT**: Intelligent content rewriting and suggestions
- **File Processing**: Supports multiple resume formats

### Frontend (React)
- **Modern UI**: Clean, responsive interface
- **Real-time Analysis**: Instant feedback on ATS compatibility
- **Multi-section Optimization**: Optimize full resume or specific sections
- **Copy-to-Clipboard**: Easy integration of optimized content

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Download spaCy language model for advanced NLP features:
```bash
# Note: spaCy may have compatibility issues with Python 3.12+
# The application works without it using basic keyword extraction
pip install spacy
python -m spacy download en_core_web_sm
```

5. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

6. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

7. Run the Flask server:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The React app will open at `http://localhost:3000`

## 📖 API Documentation

### Endpoints

#### `GET /api/health`
Check API health and configuration status.

**Response:**
```json
{
  "status": "healthy",
  "spacy_loaded": true,
  "openai_configured": true
}
```

#### `POST /api/upload`
Upload and parse a resume file.

**Request:**
- Form data with `file` field (PDF, DOCX, or TXT)

**Response:**
```json
{
  "success": true,
  "text": "Resume content...",
  "filename": "resume.pdf"
}
```

#### `POST /api/keywords`
Extract keywords from resume text.

**Request:**
```json
{
  "text": "Resume content..."
}
```

**Response:**
```json
{
  "success": true,
  "keywords": ["python", "machine learning", "data analysis", ...]
}
```

#### `POST /api/analyze`
Analyze resume against job description for ATS compatibility.

**Request:**
```json
{
  "resume": "Resume content...",
  "job_description": "Job description..."
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "score": 75,
    "matched_keywords": ["python", "sql", ...],
    "missing_keywords": ["kubernetes", "docker", ...],
    "suggestions": ["Add more relevant keywords..."]
  }
}
```

#### `POST /api/optimize`
Optimize resume content using GPT.

**Request:**
```json
{
  "resume": "Resume content...",
  "job_description": "Job description...",
  "section": "full" // Options: "full", "summary", "experience", "skills"
}
```

**Response:**
```json
{
  "success": true,
  "optimized_text": "Optimized resume content...",
  "section": "full"
}
```

#### `POST /api/suggest-improvements`
Get AI-powered improvement suggestions.

**Request:**
```json
{
  "resume": "Resume content...",
  "job_description": "Job description..."
}
```

**Response:**
```json
{
  "success": true,
  "suggestions": "1. Add more quantifiable achievements...\n2. Include relevant keywords..."
}
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **spaCy**: Natural Language Processing
- **OpenAI API**: GPT-3.5 for text generation
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing

### Frontend
- **React**: UI framework
- **Axios**: HTTP client
- **CSS3**: Styling

## 📝 Usage Guide

1. **Upload Resume**: Click or drag-and-drop your resume (PDF, DOCX, or TXT)
2. **Enter Job Description**: Paste the target job description in the right panel
3. **Analyze**: Click "Analyze ATS Compatibility" to see your match score
4. **Optimize**: Choose a section to optimize and click "Optimize Resume"
5. **Get Suggestions**: Click "Get Suggestions" for specific improvement tips
6. **Copy & Use**: Copy the optimized content to your clipboard

## 🔒 Security Notes

- Never commit your `.env` file or API keys
- The backend sanitizes file uploads and validates file types
- File size is limited to 16MB
- Uploaded files are deleted after processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

- OpenAI for GPT API
- spaCy for NLP capabilities
- React community for excellent documentation
