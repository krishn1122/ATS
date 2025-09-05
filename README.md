# Smart ATS - Professional Resume Analysis System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)](https://flask.palletsprojects.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A commercial-grade AI-powered Application Tracking System (ATS) that analyzes resumes against job descriptions using Google's Gemini AI. The system provides comprehensive analysis including percentage scoring, grammar checking, keyword matching, format evaluation, and readability assessment with a professional UI and smooth animations.

## 🚀 Live Demo

[**Deploy on Railway**](https://railway.app/template/HjCfBt) 🚀

> **Note**: Click above to deploy your own instance on Railway

## 🌐 Quick Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/HjCfBt)

### Quick Deploy Steps:
1. Click the Railway button above
2. Connect your GitHub repository: `https://github.com/krishn1122/ATS`
3. Set environment variables:
   - `GOOGLE_API_KEY` (from [Google AI Studio](https://makersuite.google.com/app/apikey))
   - `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DEPLOYMENT_MODE=frontend` (for integrated deployment)
4. Deploy and get your public URL!

For detailed deployment instructions, see [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

## 🚀 Features

### Core Analysis Features
- **AI-Powered Analysis**: Uses Google Gemini AI for intelligent resume evaluation
- **Multi-Format Support**: Supports both PDF and DOCX resume formats
- **Comprehensive Scoring**: 4-tier analysis system with detailed metrics
- **Real-time Processing**: Background analysis with status polling
- **Professional Dashboard**: Analytics and insights visualization

### Analysis Components
1. **Overall ATS Score (0-100%)**: Comprehensive resume-job description alignment
2. **Job Description Match**: Keyword alignment and relevance scoring
3. **Grammar Analysis**: ATS-critical formatting and structure issues
4. **Word Repetition**: Detection of overused terms with improvement suggestions
5. **Format & Readability**: Document structure and ATS parsing compatibility
6. **Missing Keywords**: Critical job requirement terms absent from resume
7. **Profile Summary**: AI-generated career insights and recommendations

### Technical Features
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Flask Frontend**: Professional UI with Bootstrap 5 and custom animations
- **Responsive Design**: Mobile-friendly interface with modern animations
- **Caching System**: Intelligent caching for improved performance
- **Error Handling**: Comprehensive error handling and user feedback
- **File Security**: Secure file upload with type and size validation

## 🏗️ Architecture

```
Smart ATS/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py         # Main FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── ats_models.py   # Pydantic data models
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py   # AI analysis service
│   └── utils/
│       ├── __init__.py
│       └── document_parser.py # PDF/DOCX parsing utilities
├── frontend/                # Flask Frontend
│   ├── app.py              # Main Flask application
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Custom styles and animations
│   │   └── js/
│   │       └── main.js      # Frontend JavaScript
│   └── templates/          # Jinja2 templates
│       ├── base.html       # Base template
│       ├── index.html      # Home page
│       ├── results.html    # Results page
│       ├── dashboard.html  # Analytics dashboard
│       ├── about.html      # About page
│       ├── 404.html        # Error pages
│       └── 500.html
├── logs/                   # Application logs
├── uploads/                # Temporary file storage
├── config.py               # Configuration management
├── main.py                 # Railway-compatible launcher
├── requirements.txt        # Python dependencies
├── Dockerfile              # Railway deployment
├── railway.json            # Railway configuration
├── docker-compose.yml      # Docker deployment
├── start.bat               # Windows startup script
├── start.sh                # Linux/Mac startup script
├── test_setup.py           # Setup validation
├── test_railway.py         # Railway deployment test
├── RAILWAY_DEPLOYMENT.md   # Deployment guide
├── RAILWAY_CHECKLIST.md    # Deployment checklist
└── README.md              # This file
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Google Gemini AI**: Advanced language model for resume analysis
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **Flask**: Lightweight WSGI web application framework
- **Bootstrap 5**: CSS framework for responsive design
- **Chart.js**: Data visualization for analytics dashboard
- **AOS**: Animate On Scroll library for smooth animations
- **Font Awesome**: Icon library

### Infrastructure
- **Docker**: Containerization for easy deployment
- **Nginx**: Reverse proxy and load balancer (optional)
- **Redis**: Caching layer (optional)

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini AI API key ([Get yours here](https://makersuite.google.com/app/apikey))
- pip (Python package installer)
- Git (for cloning the repository)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/krishn1122/ATS.git
cd ATS
```

### 2. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Google API key
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Use Main Launcher (Recommended)

```bash
# Run integrated mode (both frontend + backend)
python main.py
```

#### Option B: Use Startup Script

**Windows:**
```bash
.\start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### Option C: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python app.py
```

### 5. Access the Application
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Analytics Dashboard**: http://localhost:5000/dashboard

## 🚀 Railway Deployment

### Automated Deployment

1. **Fork Repository**: Fork this repository to your GitHub account
2. **Deploy on Railway**: Click the button below

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/HjCfBt)

3. **Set Environment Variables** in Railway dashboard:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   SECRET_KEY=your_generated_secret_key_here
   DEPLOYMENT_MODE=frontend
   ```

4. **Access Your App**: Railway will provide a public URL

### Manual Railway Setup

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Push to GitHub
git add .
git commit -m "Railway deployment"
git push origin main

# Create Railway project and set environment variables
# Deploy from GitHub repository
```

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions.

## 🐳 Docker Deployment

### Quick Docker Setup
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Build and start production services
docker-compose -f docker-compose.yml up -d

# Scale services (if needed)
docker-compose up -d --scale backend=3
```

## 📖 API Documentation

### Main Endpoints

#### Resume Analysis
```
POST /api/analyze-resume
- Upload resume file (PDF/DOCX) and job description
- Returns analysis ID for polling

GET /api/analysis/{analysis_id}
- Get complete analysis results

GET /api/analysis/{analysis_id}/status
- Check analysis status
```

#### Analytics
```
GET /api/analytics/summary
- Get system analytics and statistics

GET /api/supported-formats
- Get supported file formats and restrictions
```

### Example Usage

```python
import requests

# Upload resume for analysis
files = {'resume_file': open('resume.pdf', 'rb')}
data = {'job_description': 'Your job description here...'}
response = requests.post('http://localhost:8000/api/analyze-resume', 
                        files=files, data=data)

result = response.json()
analysis_id = result['data']['analysis_id']

# Poll for results
while True:
    status = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}/status')
    if status.json()['status'] == 'completed':
        results = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}')
        print(results.json())
        break
    time.sleep(5)
```

## 🎨 Frontend Usage

### Home Page Features
- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support
- **Real-time Validation**: Instant feedback on file format and size
- **Professional UI**: Modern design with smooth animations
- **Responsive Design**: Works on desktop, tablet, and mobile

### Results Page Features
- **Overall Score Display**: Visual score representation with color coding
- **Detailed Metrics**: Individual scores for different analysis components
- **Tabbed Analysis**: Organized display of grammar, repetition, and format issues
- **Actionable Insights**: Specific recommendations for improvement
- **Export Options**: Print and download results

### Analytics Dashboard
- **Score Distribution**: Visual representation of score patterns
- **Common Issues**: Analysis of frequent problems
- **Performance Insights**: Trends and improvements over time
- **Quick Actions**: Easy access to common tasks

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google Gemini AI API key | - | Yes |
| `SECRET_KEY` | Flask secret key (64+ chars) | - | Yes |
| `DEPLOYMENT_MODE` | Deployment mode (`frontend` for Railway) | `frontend` | Railway |
| `BACKEND_URL` | Backend API URL | http://localhost:8000 | No |
| `FRONTEND_URL` | Frontend URL | http://localhost:5000 | No |
| `MAX_CONTENT_LENGTH` | Max file size in bytes | 16777216 (16MB) | No |
| `RATE_LIMIT` | API rate limit per minute | 60 | No |
| `ANALYSIS_TIMEOUT` | Analysis timeout in seconds | 300 | No |
| `LOG_LEVEL` | Logging level | INFO | No |

### File Upload Limits
- **Supported Formats**: PDF, DOCX
- **Maximum File Size**: 16MB
- **File Validation**: Automatic type and size checking
- **Security**: Files are processed in memory and not permanently stored

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_api.py -v
```

### Test Coverage
- Unit tests for AI analysis service
- Integration tests for API endpoints
- Frontend JavaScript testing
- File upload and parsing tests

## 🚀 Production Deployment

### Security Checklist
- [ ] Set strong `SECRET_KEY` in production
- [ ] Use HTTPS for all communications
- [ ] Implement rate limiting
- [ ] Set up proper logging and monitoring
- [ ] Configure CORS properly
- [ ] Use environment variables for sensitive data
- [ ] Set up database for persistent storage (optional)
- [ ] Configure backup and recovery

### Performance Optimization
- **Caching**: Implement Redis for response caching
- **Load Balancing**: Use Nginx for load balancing
- **CDN**: Serve static files from CDN
- **Database**: Use PostgreSQL for persistent storage
- **Monitoring**: Set up application monitoring

### Scaling Considerations
- **Horizontal Scaling**: Use Docker Swarm or Kubernetes
- **Database**: Implement proper database with connection pooling
- **File Storage**: Use cloud storage for file handling
- **Queue System**: Implement job queue for heavy processing

## 🔧 Troubleshooting

### Common Issues

**Issue**: `GOOGLE_API_KEY not found`
- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: File upload fails
- **Solution**: Check file format (PDF/DOCX) and size (<16MB)

**Issue**: Backend connection error
- **Solution**: Ensure backend is running on port 8000

**Issue**: Analysis timeout
- **Solution**: Check internet connection and API key validity

### Logs
- **Backend logs**: Check FastAPI console output
- **Frontend logs**: Check Flask console output
- **Application logs**: Check `logs/app.log` file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/krishn1122/ATS.git
cd ATS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt

# Run setup validation
python test_setup.py

# Run Railway deployment test
python test_railway.py

# Start development server
python main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- FastAPI team for the excellent web framework
- Flask team for the lightweight framework
- Bootstrap team for the responsive CSS framework
- All contributors and the open-source community

## 📞 Support

For support, please:
1. Check the [Issues](https://github.com/krishn1122/ATS/issues) page
2. Create a new issue with detailed information
3. Join our [Discussions](https://github.com/krishn1122/ATS/discussions)
4. Review [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for deployment help

## 🗺️ Roadmap

- [ ] **Database Integration**: PostgreSQL for persistent storage
- [ ] **User Authentication**: Multi-user support with accounts
- [ ] **Batch Processing**: Analyze multiple resumes simultaneously
- [ ] **Template Library**: Pre-built job description templates
- [ ] **Integration APIs**: Connect with job boards and ATS systems
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Mobile App**: Native mobile applications
- [ ] **Collaborative Features**: Team sharing and collaboration

---

**Built with ❤️ for the job-seeking community**

