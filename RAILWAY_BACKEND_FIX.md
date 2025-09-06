# Railway Backend Deployment Instructions

## ⚠️ Railway Deployment Fix for "No module named 'uvicorn'" Error

### Problem:
Railway is not finding uvicorn because it's using the wrong requirements file or Dockerfile.

### Solution:

#### Option 1: Use Dockerfile (Recommended)
1. **Ensure Railway uses the correct Dockerfile**:
   - In Railway dashboard, go to Settings → Deploy
   - Make sure "Dockerfile" is selected as the build method
   - The Dockerfile should reference `backend-requirements.txt`

#### Option 2: Set Custom Start Command
1. **In Railway dashboard**:
   - Go to Settings → Deploy
   - Set **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - Set **Build Command**: `pip install -r backend-requirements.txt`

#### Option 3: Use main.py launcher
1. **In Railway dashboard**:
   - Go to Settings → Deploy  
   - Set **Start Command**: `python main.py`
   - Make sure environment variable `DEPLOYMENT_MODE=backend` is set

### Required Environment Variables:
```
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_generated_secret_key_here
DEPLOYMENT_MODE=backend
```

### Files Required for Railway Backend:
- ✅ `Dockerfile` (copied from Dockerfile.backend-only)
- ✅ `backend-requirements.txt` (contains uvicorn[standard]==0.24.0)
- ✅ `main.py` (updated with proper error handling)
- ✅ `backend/` directory with FastAPI code

### Verification:
After deployment, check:
1. Railway logs show "uvicorn backend.app.main:app" starting
2. Backend responds at: `https://your-backend.railway.app/api/health`
3. API docs available at: `https://your-backend.railway.app/api/docs`

### If Still Getting Errors:
1. Check Railway build logs for the exact error
2. Ensure `backend-requirements.txt` is being used
3. Verify the Dockerfile is copying the correct requirements file
4. Force a clean rebuild by making a small change to Dockerfile