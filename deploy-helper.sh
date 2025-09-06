#!/bin/bash
# Deployment helper script for Vercel + Railway setup

echo "🚀 Smart ATS Deployment Helper"
echo "================================"

# Generate SECRET_KEY
echo "1. Generating SECRET_KEY..."
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
echo ""

# Check required files
echo "2. Checking deployment files..."
FILES=("Dockerfile.backend-only" "vercel.json" "backend-requirements.txt" "frontend-requirements.txt")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Environment variables checklist
echo "3. Environment Variables Needed:"
echo ""
echo "🚂 Railway (Backend):"
echo "- GOOGLE_API_KEY=your_google_api_key"
echo "- SECRET_KEY=your_generated_secret_key"
echo ""
echo "🔺 Vercel (Frontend):"
echo "- BACKEND_URL=https://your-backend.railway.app"
echo "- SECRET_KEY=your_generated_secret_key"
echo "- FLASK_ENV=production"
echo ""

echo "4. Deployment URLs:"
echo "- Google API Studio: https://makersuite.google.com/app/apikey"
echo "- Railway: https://railway.app"
echo "- Vercel: https://vercel.com"
echo ""

echo "5. Deployment Order:"
echo "1️⃣ Deploy backend to Railway first"
echo "2️⃣ Get Railway backend URL"
echo "3️⃣ Deploy frontend to Vercel with backend URL"
echo "4️⃣ Update backend CORS with Vercel URL"
echo ""

echo "✅ Deployment files are ready!"
echo "Follow the guide in VERCEL_RAILWAY_DEPLOYMENT.md"