# Resume AI Optimizer - Example Configuration
# Copy this to backend/.env and update with your values

# Flask Backend Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# OpenAI Configuration (REQUIRED)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Notes:
# - The OpenAI API key is required for optimization and suggestions features
# - Use FLASK_ENV=production for production deployments
# - Generate a secure SECRET_KEY for production: python -c "import secrets; print(secrets.token_hex(32))"
