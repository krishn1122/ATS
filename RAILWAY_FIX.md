# 🔧 Railway Deployment Fix Guide

## Issue Diagnosis
Your Railway deployment at `https://ats-production-47d6.up.railway.app/` shows:
- ✅ Frontend loads correctly
- ❌ Backend API requests fail with "Backend service unavailable"

## Root Cause Analysis
1. **Deployment Mode Issue**: `DEPLOYMENT_MODE=frontend` means only frontend starts
2. **Port Conflict**: Backend trying to use port 8001, but Railway only exposes main `$PORT`
3. **API URL Issue**: Frontend pointing to wrong backend URL

## 🎯 Quick Fix Solutions

### **Solution 1: Backend-Only Deployment (Recommended)**

**Update Railway Environment Variables:**
```bash
DEPLOYMENT_MODE=backend
```

This will:
- Start FastAPI backend on Railway's main port
- Serve backend API endpoints on your Railway URL
- Frontend can access API at same domain

### **Solution 2: Separate Frontend/Backend Services**

If you want separate services:

1. **Create 2 Railway Services:**
   - Service 1: Backend (`DEPLOYMENT_MODE=backend`)
   - Service 2: Frontend (`DEPLOYMENT_MODE=frontend`)

2. **Configure Frontend Service:**
   ```bash
   BACKEND_URL=https://your-backend-service.railway.app
   ```

### **Solution 3: Integrated Single Service**

For a true monolith approach:

1. **Use Unified Server:**
   ```bash
   DEPLOYMENT_MODE=integrated
   ```

2. **Update main.py startup command in Railway:**
   - Change CMD to: `["python", "unified_server.py"]`

## 🛠️ Step-by-Step Fix Instructions

### **Quick Fix (5 minutes):**

1. **Go to Railway Dashboard**
   - Open your project: `ats-production-47d6`
   - Click on "Variables" tab

2. **Update Environment Variable:**
   - Find `DEPLOYMENT_MODE`
   - Change value from `frontend` to `backend`
   - Save changes

3. **Redeploy:**
   - Railway will automatically redeploy
   - Wait 2-3 minutes for deployment

4. **Test Backend API:**
   - Visit: `https://ats-production-47d6.up.railway.app/api/health`
   - Should return: `{"status": "healthy", "timestamp": "..."}`

5. **Update Frontend (if needed):**
   - Frontend requests should now work
   - API calls will go to same domain/port

### **Detailed Fix (15 minutes):**

1. **Check Current Configuration:**
   ```bash
   # Current problematic setup
   DEPLOYMENT_MODE=frontend  # ❌ Only starts frontend
   BACKEND_PORT=8001         # ❌ Railway doesn't expose this
   ```

2. **Apply Correct Configuration:**
   ```bash
   # Fixed setup
   DEPLOYMENT_MODE=backend   # ✅ Starts backend on main port
   # Remove BACKEND_PORT      # ✅ Use Railway's $PORT
   ```

3. **Verify API Endpoints:**
   - Health Check: `/api/health`
   - API Docs: `/api/docs`  
   - Resume Analysis: `/api/analyze-resume`

## 🧪 Testing Your Fix

### **1. Test Backend API:**
```bash
curl https://ats-production-47d6.up.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy", 
  "timestamp": "2025-01-05T..."
}
```

### **2. Test Frontend-to-Backend Communication:**
```bash
curl -X POST https://ats-production-47d6.up.railway.app/api/analyze-resume \
  -F "resume_file=@test-resume.pdf" \
  -F "job_description=Test job description"
```

### **3. Full UI Test:**
1. Visit: `https://ats-production-47d6.up.railway.app/`
2. Upload a test resume
3. Add job description
4. Click "Analyze Resume"
5. Verify analysis completes successfully

## 🎯 Expected Results After Fix

### **Before Fix:**
- ❌ Frontend: Works
- ❌ Backend API: "Service unavailable"
- ❌ Resume analysis: Fails

### **After Fix:**
- ✅ Frontend: Works (if using frontend mode)
- ✅ Backend API: Returns proper responses
- ✅ Resume analysis: Completes successfully
- ✅ All features: Fully functional

## 📋 Alternative Deployment Architectures

### **Option A: Backend-Only (Recommended for MVP)**
```bash
DEPLOYMENT_MODE=backend
# Serves API only, build separate frontend later
```

### **Option B: Monolith with API**
```bash
DEPLOYMENT_MODE=integrated  
# Serves both frontend UI and backend API
```

### **Option C: Microservices**
```bash
# Service 1: Backend
DEPLOYMENT_MODE=backend

# Service 2: Frontend  
DEPLOYMENT_MODE=frontend
BACKEND_URL=https://backend-service.railway.app
```

## 🚨 Important Notes

1. **Railway Free Tier**: 500 hours/month
2. **Domain**: Your current URL will remain the same
3. **Environment Variables**: Changes trigger automatic redeployment
4. **Logs**: Monitor Railway logs during redeployment
5. **API Keys**: Keep `GOOGLE_API_KEY` and `SECRET_KEY` secure

## ✅ Deployment Status Checklist

After applying the fix:

- [ ] Railway deployment completes without errors
- [ ] `/api/health` returns healthy status
- [ ] `/api/docs` shows FastAPI documentation
- [ ] Frontend can communicate with backend
- [ ] Resume upload and analysis works
- [ ] All UI features are functional

---

**Need help?** The fix should resolve your "Backend service unavailable" issue within 5 minutes of updating the environment variable.