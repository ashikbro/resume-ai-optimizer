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

## 📁 Project Structure

```
resume-ai-optimizer/
├── backend/                 # Flask REST API
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container config
│   └── .env.example        # Environment template
│
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── FileUpload.js       # Resume upload
│   │   │   ├── KeywordDisplay.js   # Keywords display
│   │   │   ├── AnalysisResults.js  # ATS analysis
│   │   │   └── OptimizerPanel.js   # AI optimization
│   │   ├── services/
│   │   │   └── api.js      # API integration
│   │   └── App.js          # Main application
│   ├── public/
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container config
│
├── docker-compose.yml      # Multi-container setup
├── start.sh               # Quick start script
├── README.md              # This file
├── CONTRIBUTING.md        # Developer guide
└── TROUBLESHOOTING.md     # Common issues
```

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

### Quick Start

Use the provided startup script to run both frontend and backend:

```bash
chmod +x start.sh
./start.sh
```

### Docker Deployment

For production deployment using Docker:

```bash
# Set your OpenAI API key in environment
export OPENAI_API_KEY=your-api-key-here

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application at `http://localhost:3000`

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

### Workflow

```
1. Upload Resume → 2. Parse Text → 3. Extract Keywords
                              ↓
4. Enter Job Description → 5. Analyze ATS Score → 6. View Matched/Missing Keywords
                              ↓
7. Select Optimization Type → 8. AI Generates Optimized Content → 9. Copy & Use
```

### Step-by-Step

1. **Upload Resume**: Click or drag-and-drop your resume (PDF, DOCX, or TXT)
2. **Review Extracted Keywords**: See important keywords automatically identified
3. **Enter Job Description**: Paste the target job description in the right panel
4. **Analyze ATS Compatibility**: Click to see your match score and gaps
5. **Choose Optimization**:
   - Full Resume: Complete rewrite optimized for the job
   - Summary: Professional summary tailored to position
   - Experience: Enhanced work experience section
   - Skills: Relevant skills recommendations
6. **Get AI Suggestions**: Click for specific, actionable improvement tips
7. **Copy & Apply**: Use the copy button to get optimized content

### Tips for Best Results

- Use detailed job descriptions for better matching
- Review AI suggestions critically - they're recommendations, not rules
- Maintain authenticity - don't add skills you don't have
- Optimize for specific job postings rather than generic resumes
- Test different optimization sections to find what works best

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
