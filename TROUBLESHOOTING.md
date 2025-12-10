# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. ModuleNotFoundError: No module named 'spacy'
**Solution**: This is expected and normal. The application works without spaCy.
- The app will display: "Warning: spaCy not available. Using basic keyword extraction."
- To use advanced NLP features, install spaCy (requires Python < 3.12):
  ```bash
  pip install spacy
  python -m spacy download en_core_web_sm
  ```

#### 2. OpenAI API Error: "Invalid API key"
**Solution**: Check your OpenAI API key configuration.
- Ensure `.env` file exists in `backend/` directory
- Verify OPENAI_API_KEY is set correctly
- Test your key at: https://platform.openai.com/api-keys
- Make sure there are no extra spaces or quotes

#### 3. FileNotFoundError: uploads directory
**Solution**: The uploads directory should be created automatically.
```bash
cd backend
mkdir uploads
```

#### 4. Port 5000 already in use
**Solution**: Another application is using port 5000.
- Kill the process: `lsof -ti:5000 | xargs kill -9` (Mac/Linux)
- Or change the port in `backend/app.py` and update frontend API URL

### Frontend Issues

#### 1. npm install fails
**Solution**: Clear npm cache and retry.
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### 2. "proxy" error or CORS issues
**Solution**: Ensure backend is running on port 5000.
- Check backend is running: `curl http://localhost:5000/api/health`
- Restart both frontend and backend
- Check CORS configuration in `backend/app.py`

#### 3. React Scripts version warning
**Solution**: This is addressed in package.json with version 5.0.2.
- If still seeing warnings, update: `npm install react-scripts@latest`

### Upload Issues

#### 4. File upload fails
**Possible causes**:
- File size > 16MB (increase `MAX_CONTENT_LENGTH` in `backend/app.py`)
- Unsupported file format (only PDF, DOCX, TXT allowed)
- File corrupted or empty

**Solution**:
```python
# In backend/app.py, increase limit if needed:
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

#### 5. PDF text extraction returns empty
**Solution**: PDF may be image-based or encrypted.
- Try converting to text-based PDF
- Use OCR tool first if PDF contains only images
- Test with a different PDF

### API Issues

#### 6. OpenAI rate limit exceeded
**Solution**: You've hit OpenAI API rate limits.
- Wait a few minutes before retrying
- Upgrade your OpenAI plan
- Implement request queuing/throttling

#### 7. OpenAI timeout errors
**Solution**: Request taking too long or network issues.
- Check your internet connection
- Try reducing the text length
- Increase timeout in API call if needed

### Docker Issues

#### 8. Docker build fails
**Solution**: Check Docker is installed and running.
```bash
docker --version
docker-compose --version
```

#### 9. Container can't connect to backend
**Solution**: Update service names in docker-compose.yml
- Backend should be accessible at `http://backend:5000`
- Check network configuration

### Development Issues

#### 10. Changes not reflecting in browser
**Solution**: Clear cache and restart dev server.
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Clear browser cache
- Restart `npm start`

#### 11. Hot reload not working
**Solution**: 
```bash
# Create .env in frontend directory with:
echo "FAST_REFRESH=true" > frontend/.env
```

## Getting Help

If you're still experiencing issues:

1. Check the logs:
   - Backend: Check terminal where Flask is running
   - Frontend: Check browser console (F12)

2. Verify prerequisites:
   - Python 3.8-3.11 installed
   - Node.js 14+ installed
   - OpenAI API key is valid

3. Test components independently:
   - Test backend: `curl http://localhost:5000/api/health`
   - Test frontend: Check for errors in browser console

4. Review environment variables:
   - Backend: `backend/.env` file exists and configured
   - Frontend: API URL matches backend port

5. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, Node version)

## Performance Tips

1. **Large Resume Files**: 
   - Keep resumes under 5MB for best performance
   - Use text-based PDFs rather than scanned images

2. **OpenAI Response Time**:
   - Full resume optimization takes 10-30 seconds
   - Section optimization is faster (5-15 seconds)
   - Depends on resume length and OpenAI API load

3. **Memory Usage**:
   - Backend uses ~100-200MB without spaCy
   - With spaCy: ~500MB-1GB
   - Frontend dev server: ~200-300MB

## Security Notes

- Never commit `.env` files
- Rotate OpenAI API keys periodically
- Use environment variables in production
- Set `FLASK_ENV=production` in production
- Use HTTPS in production (setup nginx or similar)
