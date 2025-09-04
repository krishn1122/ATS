# Railway Deployment Guide

## Prerequisites
1. GitHub account with your project pushed
2. Railway account (free at railway.app)
3. Google Gemini API key

## Deployment Steps

### 1. Prepare Repository
Ensure these files are in your repository:
- `Dockerfile` (for Railway deployment)
- `railway.json` (Railway configuration)
- `main.py` (updated for Railway)
- `.env.railway` (environment variables template)

### 2. Deploy on Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your ATS repository

3. **Set Environment Variables**
   Go to your project → Variables tab and add:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key
   SECRET_KEY=your_generated_secret_key
   DEPLOYMENT_MODE=frontend
   PORT=5000
   BACKEND_PORT=8001
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Wait for deployment to complete
   - You'll get a public URL

### 3. Generate SECRET_KEY
Run this command to generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to Railway environment variables

### 5. Test Deployment
- Visit your Railway URL
- Upload a test resume
- Verify the analysis works

## Troubleshooting

### Common Issues:
1. **Missing Environment Variables**: Ensure all required variables are set in Railway dashboard
2. **Build Failures**: Check Railway build logs for specific errors
3. **Runtime Errors**: Check Railway deployment logs

### Environment Variables Checklist:
- [ ] GOOGLE_API_KEY (from Google AI Studio)
- [ ] SECRET_KEY (generated securely)
- [ ] DEPLOYMENT_MODE=frontend
- [ ] PORT=5000
- [ ] BACKEND_PORT=8001

## Project Structure for Railway
```
ATS/
├── Dockerfile              # Railway deployment container
├── railway.json           # Railway configuration
├── main.py                # Railway-compatible launcher
├── requirements.txt       # Python dependencies
├── backend/               # FastAPI backend
├── frontend/              # Flask frontend
└── .env.railway          # Environment variables template
```

## Monitoring
- Monitor resource usage in Railway dashboard
- Free tier provides 500 hours/month
- Check logs for any errors or performance issues

## Custom Domain (Optional)
- Add custom domain in Railway dashboard
- Configure DNS settings as instructed
- SSL certificates are automatically provided