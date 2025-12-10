# Contributing to Resume AI Optimizer

Thank you for your interest in contributing to Resume AI Optimizer! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.8+ (3.11 recommended, avoid 3.12+ due to spaCy compatibility)
- Node.js 14+
- OpenAI API key

### Getting Started

1. Fork and clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Run tests (if any are added)

## Architecture

### Backend (Flask)
- **app.py**: Main Flask application with all API endpoints
- **Requirements**: Optional spaCy for advanced NLP, falls back to basic extraction
- **OpenAI**: Compatible with both v0.x and v1+ through `call_openai_chat()` helper

### Frontend (React)
- **Component-based architecture**: Separate components for each feature
- **API Service**: Centralized API calls in `src/services/api.js`
- **State Management**: React hooks (useState, useEffect)

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions focused and single-purpose

### JavaScript/React
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable and component names
- Keep components small and reusable

## Important Conventions

### Security
- **NEVER** commit API keys or secrets
- Always use `secure_filename()` for file uploads
- Validate and sanitize all user inputs
- Debug mode must be controlled by environment variable

### Error Handling
- Use try-except blocks for external API calls
- Return meaningful error messages to users
- Log errors for debugging

### Optional Dependencies
- spaCy is optional - maintain fallback functionality
- Check `SPACY_AVAILABLE` flag before using spaCy features
- Test with and without spaCy installed

### OpenAI Integration
- Always use `call_openai_chat()` helper function
- Don't call OpenAI API directly
- Handle both v0.x and v1+ library versions

## Testing

When adding new features:
1. Test with minimal dependencies (without spaCy)
2. Test with OpenAI API key configured
3. Test without OpenAI API key (should show appropriate errors)
4. Test file upload with various formats (PDF, DOCX, TXT)
5. Test with invalid inputs

## Pull Request Process

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly (both backend and frontend)
4. Update documentation if needed
5. Ensure no security vulnerabilities (run CodeQL if possible)
6. Submit pull request with clear description

## Key Files to Review

- `backend/app.py` - Main Flask application
- `frontend/src/App.js` - Main React component
- `README.md` - User-facing documentation
- `requirements.txt` - Python dependencies
- `package.json` - Node dependencies

## Common Issues

### spaCy Installation Fails
- This is expected on Python 3.12+
- The app works without spaCy using basic keyword extraction
- Don't make spaCy a hard requirement

### OpenAI API Errors
- Check if API key is set in `.env`
- Verify the key is valid
- Check OpenAI API rate limits

### CORS Errors
- Ensure backend is running on port 5000
- Ensure frontend is running on port 3000
- Check CORS configuration in Flask

## Adding New Features

### New API Endpoint
1. Add route in `backend/app.py`
2. Add service method in `frontend/src/services/api.js`
3. Update API documentation in README
4. Add error handling

### New React Component
1. Create component in `frontend/src/components/`
2. Create corresponding CSS file
3. Import and use in `App.js`
4. Ensure responsive design

## Questions?

Feel free to open an issue for questions or discussions!
