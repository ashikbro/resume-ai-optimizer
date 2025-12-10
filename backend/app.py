import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import openai
import PyPDF2
import docx
import re
from collections import Counter

# Try to import spacy, but make it optional
try:
    import spacy
    from spacy.matcher import PhraseMatcher
    SPACY_AVAILABLE = True
except ImportError:
    print("Warning: spaCy not available. Using basic keyword extraction.")
    SPACY_AVAILABLE = False
    spacy = None
    PhraseMatcher = None

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY', '')

# Check OpenAI version and set up compatibility
OPENAI_V1 = hasattr(openai, '__version__') and openai.__version__.startswith('1.')
if OPENAI_V1:
    from openai import OpenAI
    openai_client = OpenAI(api_key=openai.api_key) if openai.api_key else None
else:
    openai_client = None

# Initialize spaCy if available
nlp = None
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load('en_core_web_sm')
    except:
        print("Warning: spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
        nlp = None


def call_openai_chat(system_message, user_message, max_tokens=1500, temperature=0.7):
    """Helper function to call OpenAI API with compatibility for different versions"""
    if not openai.api_key:
        raise Exception("OpenAI API key not configured")
    
    if OPENAI_V1 and openai_client:
        # Use new OpenAI v1+ API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    else:
        # Use old OpenAI v0.x API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    ext = file_path.rsplit('.', 1)[1].lower()
    
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ""


def extract_keywords_with_spacy(text):
    """Extract keywords using spaCy NLP"""
    if not nlp:
        return []
    
    doc = nlp(text.lower())
    
    # Extract nouns, proper nouns, and relevant entities
    keywords = []
    
    # Extract named entities
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'LANGUAGE', 'SKILL']:
            keywords.append(ent.text)
    
    # Extract noun chunks and key phrases
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Limit to 3-word phrases
            keywords.append(chunk.text)
    
    # Extract important nouns and proper nouns
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
            keywords.append(token.text)
    
    # Count and return most common keywords
    keyword_freq = Counter(keywords)
    return [kw for kw, _ in keyword_freq.most_common(30)]


def extract_keywords_basic(text):
    """Basic keyword extraction without spaCy"""
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Common stop words to exclude
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                      'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                      'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                      'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your'])
    
    # Filter words
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count and return most common
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(30)]


def analyze_ats_score(resume_text, job_description):
    """Analyze ATS compatibility score"""
    if not nlp:
        return analyze_ats_score_basic(resume_text, job_description)
    
    resume_doc = nlp(resume_text.lower())
    job_doc = nlp(job_description.lower())
    
    # Extract keywords from both
    resume_keywords = set(extract_keywords_with_spacy(resume_text))
    job_keywords = set(extract_keywords_with_spacy(job_description))
    
    # Calculate match percentage
    if len(job_keywords) == 0:
        return {
            'score': 0,
            'matched_keywords': [],
            'missing_keywords': [],
            'suggestions': []
        }
    
    matched = resume_keywords.intersection(job_keywords)
    missing = job_keywords - resume_keywords
    
    score = int((len(matched) / len(job_keywords)) * 100)
    
    suggestions = []
    if score < 70:
        suggestions.append("Consider adding more relevant keywords from the job description")
    if len(missing) > 5:
        suggestions.append(f"You're missing {len(missing)} important keywords")
    
    return {
        'score': score,
        'matched_keywords': list(matched)[:10],
        'missing_keywords': list(missing)[:10],
        'suggestions': suggestions
    }


def analyze_ats_score_basic(resume_text, job_description):
    """Basic ATS analysis without spaCy"""
    resume_keywords = set(extract_keywords_basic(resume_text))
    job_keywords = set(extract_keywords_basic(job_description))
    
    if len(job_keywords) == 0:
        return {
            'score': 0,
            'matched_keywords': [],
            'missing_keywords': [],
            'suggestions': []
        }
    
    matched = resume_keywords.intersection(job_keywords)
    missing = job_keywords - resume_keywords
    
    score = int((len(matched) / len(job_keywords)) * 100)
    
    return {
        'score': score,
        'matched_keywords': list(matched)[:10],
        'missing_keywords': list(missing)[:10],
        'suggestions': ["Add more relevant keywords from the job description"]
    }


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'spacy_available': SPACY_AVAILABLE,
        'spacy_loaded': nlp is not None,
        'openai_configured': bool(openai.api_key)
    })


@app.route('/api/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        text = extract_text_from_file(filepath)
        
        # Clean up file after extraction
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'text': text,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/keywords', methods=['POST'])
def extract_keywords():
    """Extract keywords from resume text"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    try:
        # Extract keywords using spaCy if available, otherwise use basic extraction
        if nlp:
            keywords = extract_keywords_with_spacy(text)
        else:
            keywords = extract_keywords_basic(text)
        
        return jsonify({
            'success': True,
            'keywords': keywords
        })
    
    except Exception as e:
        return jsonify({'error': f'Error extracting keywords: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description for ATS compatibility"""
    data = request.get_json()
    
    if not data or 'resume' not in data or 'job_description' not in data:
        return jsonify({'error': 'Resume and job description required'}), 400
    
    resume_text = data['resume']
    job_description = data['job_description']
    
    try:
        analysis = analyze_ats_score(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """Optimize resume content using OpenAI GPT"""
    data = request.get_json()
    
    if not data or 'resume' not in data or 'job_description' not in data:
        return jsonify({'error': 'Resume and job description required'}), 400
    
    if not openai.api_key:
        return jsonify({'error': 'OpenAI API key not configured'}), 500
    
    resume_text = data['resume']
    job_description = data['job_description']
    section = data.get('section', 'full')  # full, summary, experience, skills
    
    try:
        # Create prompt based on section
        if section == 'full':
            prompt = f"""You are a professional resume writer. Optimize the following resume to better match this job description. 
Keep the same structure but enhance the content with relevant keywords and stronger action verbs.
Make it ATS-friendly while maintaining authenticity.

Job Description:
{job_description}

Current Resume:
{resume_text}

Provide an optimized version of the resume:"""
        elif section == 'summary':
            prompt = f"""Create a compelling professional summary (3-4 sentences) that highlights relevant skills and experience for this job:

Job Description:
{job_description}

Current Resume Content:
{resume_text}

Professional Summary:"""
        elif section == 'experience':
            prompt = f"""Rewrite the work experience section to better align with this job description. 
Use strong action verbs and quantifiable achievements where possible.

Job Description:
{job_description}

Current Experience:
{resume_text}

Optimized Experience:"""
        else:  # skills or other
            prompt = f"""Based on this job description, suggest relevant skills that should be highlighted in the resume:

Job Description:
{job_description}

Current Resume:
{resume_text}

Suggested Skills:"""
        
        # Call OpenAI API using helper function
        system_message = "You are a professional resume writer and career coach with expertise in ATS optimization."
        optimized_text = call_openai_chat(system_message, prompt, max_tokens=1500, temperature=0.7)
        
        return jsonify({
            'success': True,
            'optimized_text': optimized_text,
            'section': section
        })
    
    except Exception as e:
        return jsonify({'error': f'Error optimizing resume: {str(e)}'}), 500


@app.route('/api/suggest-improvements', methods=['POST'])
def suggest_improvements():
    """Get AI-powered suggestions for resume improvement"""
    data = request.get_json()
    
    if not data or 'resume' not in data or 'job_description' not in data:
        return jsonify({'error': 'Resume and job description required'}), 400
    
    if not openai.api_key:
        return jsonify({'error': 'OpenAI API key not configured'}), 500
    
    resume_text = data['resume']
    job_description = data['job_description']
    
    try:
        prompt = f"""Analyze this resume against the job description and provide specific, actionable suggestions for improvement.

Job Description:
{job_description}

Resume:
{resume_text}

Provide 5-7 specific suggestions to improve this resume for the job, focusing on:
1. Missing keywords or skills
2. Content improvements
3. Formatting suggestions
4. ATS optimization tips

Format your response as a numbered list."""
        
        system_message = "You are an expert career coach and resume consultant."
        suggestions = call_openai_chat(system_message, prompt, max_tokens=800, temperature=0.7)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({'error': f'Error generating suggestions: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
