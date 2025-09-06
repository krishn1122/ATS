# 🚀 Vercel (Frontend) + Railway (Backend) Deployment Guide

## 📋 **Overview**
This guide will help you deploy your Smart ATS application with:
- **Frontend**: Vercel (Flask app serving HTML/CSS/JS)
- **Backend**: Railway (FastAPI serving REST API)

## 🔧 **Prerequisites**

### Required API Keys:
1. **Google Gemini API Key**: [Get from Google AI Studio](https://makersuite.google.com/app/apikey)
2. **SECRET_KEY**: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`

## 🎯 **Step-by-Step Deployment**

### Phase 1: Deploy Backend on Railway

#### 1. Create Backend Repository Structure
```bash
# Create a separate backend repository or use the same repo with backend focus
git checkout -b backend-deploy
```

#### 2. Deploy to Railway
1. Visit [railway.app](https://railway.app) and sign up with GitHub
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Choose **Root Directory**: `/` (or create separate backend repo)

#### 3. Configure Railway Environment Variables
In Railway dashboard → Variables tab, add:
```
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_generated_secret_key_here
```

#### 4. Railway Build Configuration
Railway will automatically use the `Dockerfile.backend-only` if present, or create a custom build:

**Option A: Use Backend-Only Dockerfile**
- Rename `Dockerfile.backend-only` to `Dockerfile`
- Railway will build automatically

**Option B: Custom Start Command**
- Set Railway start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

#### 5. Test Backend Deployment
- Railway will provide a URL like: `https://your-backend.railway.app`
- Test API: `https://your-backend.railway.app/api/health`
- Check API docs: `https://your-backend.railway.app/api/docs`

### Phase 2: Deploy Frontend on Vercel

#### 1. Update CORS in Backend
✅ Already updated in your backend to allow Vercel domains

#### 2. Prepare Frontend for Vercel
1. Update `vercel.json` with your Railway backend URL:
```json
{
  "env": {
    "BACKEND_URL": "https://your-backend.railway.app"
  }
}
```

#### 3. Deploy to Vercel
1. Visit [vercel.com](https://vercel.com) and sign up with GitHub
2. Click "New Project"
3. Import your repository
4. **Root Directory**: Leave as `/` or set to `/frontend` if using subdirectory
5. **Framework Preset**: Other
6. **Build Command**: `pip install -r frontend-requirements.txt`
7. **Output Directory**: Leave empty
8. **Install Command**: `pip install -r frontend-requirements.txt`

#### 4. Configure Vercel Environment Variables
In Vercel dashboard → Settings → Environment Variables:
```
BACKEND_URL=https://your-backend.railway.app
SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=production
```

#### 5. Update Vercel Build Settings
**Advanced Build Settings:**
- Python Version: `3.9.x`
- Install Command: `pip install -r frontend-requirements.txt`
- Build Command: (leave empty)
- Output Directory: (leave empty)

### Phase 3: Connect Frontend and Backend

#### 1. Update CORS in Backend
Replace the placeholder in your backend CORS configuration:
```python
allow_origins=[
    "https://your-frontend-app.vercel.app",  # Replace with actual Vercel URL
    "https://*.vercel.app",  # Allow all Vercel subdomains
]
```

#### 2. Update Frontend Backend URL
Update your Vercel environment variables with the actual Railway URL.

## 🧪 **Testing Your Deployment**

### Backend Testing (Railway):
- [ ] Health check: `GET https://your-backend.railway.app/api/health`
- [ ] API docs available: `https://your-backend.railway.app/api/docs`
- [ ] CORS working for Vercel domain

### Frontend Testing (Vercel):
- [ ] Homepage loads: `https://your-frontend.vercel.app`
- [ ] File upload works
- [ ] Resume analysis completes
- [ ] Results display correctly

### Integration Testing:
- [ ] Frontend can communicate with backend
- [ ] No CORS errors in browser console
- [ ] Complete upload → analysis → results flow works

## 🔍 **Troubleshooting**

### Common Issues:

#### Backend (Railway) Issues:
- **Build fails**: Check `backend-requirements.txt` has all dependencies
- **Port issues**: Railway automatically sets `$PORT` environment variable
- **Memory issues**: Upgrade Railway plan if needed

#### Frontend (Vercel) Issues:
- **Build fails**: Ensure `frontend-requirements.txt` is correct
- **404 errors**: Check Vercel routing configuration
- **Environment variables**: Ensure all vars are set in Vercel dashboard

#### Integration Issues:
- **CORS errors**: Update backend CORS to include your Vercel domain
- **Connection refused**: Check backend URL in frontend environment variables
- **Timeout errors**: Increase timeout settings or optimize backend performance

## 💰 **Cost Breakdown**

### Free Tier Limits:
- **Railway**: $5/month free credit, then pay-as-you-use
- **Vercel**: 100GB bandwidth, 100 deployments/month free

### Estimated Costs:
- **Development/Testing**: Completely free
- **Light production use**: $0-10/month
- **Heavy usage**: Monitor and scale as needed

## 🔄 **Alternative Configurations**

### Option A: Single Repository
Keep both frontend and backend in the same repo:
- Railway: Set root directory to `/backend`
- Vercel: Set root directory to `/frontend`

### Option B: Separate Repositories
Create separate repositories for cleaner deployment:
- `smart-ats-backend` → Railway
- `smart-ats-frontend` → Vercel

## 📊 **Performance Optimization**

### Backend (Railway):
- Enable Railway's edge caching
- Use Railway's database for persistent storage if needed
- Monitor API response times

### Frontend (Vercel):
- Vercel automatically optimizes static assets
- Use Vercel's edge functions for additional performance
- Enable Vercel Analytics

## 🚀 **Next Steps After Deployment**

1. **Custom Domains**: Add custom domains in both platforms
2. **Monitoring**: Set up error tracking and performance monitoring
3. **SSL**: Both platforms provide automatic SSL certificates
4. **Scaling**: Monitor usage and scale as needed
5. **CI/CD**: Set up automatic deployments on git push

## 🔐 **Security Checklist**

- [ ] Environment variables properly set (not in code)
- [ ] CORS configured for production domains only
- [ ] SSL certificates active on both services
- [ ] API rate limiting configured
- [ ] No sensitive data in logs

## ✅ **Success Criteria**

Your deployment is successful when:
- [ ] Backend API is accessible and responding
- [ ] Frontend loads and renders correctly
- [ ] Complete file upload → analysis → results workflow works
- [ ] No CORS or connection errors
- [ ] Both services are secured with HTTPS

---

**Estimated Total Setup Time**: 30-45 minutes
**Difficulty Level**: Intermediate
**Cost**: Free tier covers most use cases