# Production Deployment Configuration

## Railway Backend Environment Variables
# Set these in Railway dashboard -> Variables tab:
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_generated_secret_key_here

## Vercel Frontend Environment Variables  
# Set these in Vercel dashboard -> Settings -> Environment Variables:
BACKEND_URL=https://your-backend.railway.app
SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=production

## Instructions:
# 1. Generate SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
# 2. Get GOOGLE_API_KEY from: https://makersuite.google.com/app/apikey
# 3. Replace your-backend.railway.app with actual Railway URL
# 4. Never commit real API keys to version control