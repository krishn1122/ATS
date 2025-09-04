# 🚀 Railway Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Generate SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Get Google API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Run validation: `python test_setup.py`
- [ ] Run Railway test: `python test_railway.py`

### 2. Security Check
- [ ] Remove real API keys from `.env` and `.env.railway`
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Verify no sensitive data in commit history

### 3. Repository Preparation
- [ ] Commit all changes
- [ ] Push to GitHub repository: `https://github.com/krishn1122/ATS`
- [ ] Verify all files are pushed

### 4. Railway Setup
- [ ] Create Railway account at [railway.app](https://railway.app)
- [ ] Connect GitHub account
- [ ] Create new project from GitHub repo

### 5. Environment Variables (Set in Railway Dashboard)
```
GOOGLE_API_KEY=<your-actual-google-api-key>
SECRET_KEY=<your-generated-secret-key>
DEPLOYMENT_MODE=frontend
PORT=5000
BACKEND_PORT=8001
```

### 6. Deployment Verification
- [ ] Monitor build logs in Railway
- [ ] Wait for successful deployment
- [ ] Test the public URL
- [ ] Upload test resume and verify analysis

## 🔧 Quick Commands

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Generate Secret Key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run Validation:
```bash
python test_setup.py
python test_railway.py
```

### Git Commands:
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

## 📋 Railway Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini AI API Key | ✅ Yes |
| `SECRET_KEY` | Flask secret key (32+ chars) | ✅ Yes |
| `DEPLOYMENT_MODE` | Set to `frontend` | ✅ Yes |
| `PORT` | Application port (Railway sets this) | ⚠️ Auto |
| `BACKEND_PORT` | Backend service port | 🔧 Optional |

## 🎯 Success Criteria

- ✅ Application builds without errors
- ✅ Public URL is accessible
- ✅ File upload works (PDF/DOCX)
- ✅ AI analysis completes successfully
- ✅ Results display correctly
- ✅ No console errors

## 🐛 Common Issues

1. **Build Fails**: Check dependencies in `requirements.txt`
2. **API Errors**: Verify `GOOGLE_API_KEY` is set correctly
3. **500 Errors**: Check `SECRET_KEY` is generated properly
4. **File Upload Fails**: Ensure file size < 16MB and format is PDF/DOCX

## 📞 Support

If deployment fails:
1. Check Railway build/deployment logs
2. Verify all environment variables are set
3. Test locally with `python main.py`
4. Check GitHub repository has latest code