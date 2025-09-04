# Smart ATS - Professional Resume Analysis System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A commercial-grade AI-powered Application Tracking System (ATS) that analyzes resumes against job descriptions using Google's Gemini AI. The system provides comprehensive analysis including grammar checking, keyword matching, format evaluation, and readability scoring with professional UI and animations.

## 🚀 Features

### Core Analysis Features
- **AI-Powered Analysis**: Uses Google Gemini AI for intelligent resume evaluation
- **Multi-Format Support**: Supports both PDF and DOCX resume formats
- **Comprehensive Scoring**: 4-tier analysis system with detailed metrics
- **Real-time Processing**: Background analysis with status polling
- **Professional Dashboard**: Analytics and insights visualization

### Analysis Components
1. **Percentage Score (0-100%)**: Overall resume alignment with job description
2. **Grammar Analysis**: Identifies and suggests fixes for grammatical errors
3. **Word Repetition**: Detects overused words and suggests improvements
4. **Format & Readability**: Evaluates structure, formatting, and readability score
5. **Keyword Matching**: Identifies missing keywords from job requirements
6. **Profile Summary**: AI-generated insights and recommendations

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
│   │   └── main.py         # Main FastAPI application
│   ├── models/
│   │   └── ats_models.py   # Pydantic data models
│   ├── services/
│   │   └── ai_service.py   # AI analysis service
│   └── utils/
│       └── document_parser.py # PDF/DOCX parsing utilities
├── frontend/                # Flask Frontend
│   ├── app.py              # Main Flask application
│   ├── static/
│   │   ├── css/style.css   # Custom styles and animations
│   │   └── js/main.js      # Frontend JavaScript
│   └── templates/          # Jinja2 templates
│       ├── base.html       # Base template
│       ├── index.html      # Home page
│       ├── results.html    # Results page
│       └── dashboard.html  # Analytics dashboard
├── logs/                   # Application logs
├── uploads/                # Temporary file storage
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker deployment
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

- Python 3.8 or higher
- Google Gemini AI API key
- pip (Python package installer)
- Git (for cloning the repository)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-ats.git
cd smart-ats
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

#### Option A: Use Startup Script (Recommended)

**Windows:**
```bash
./start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### Option B: Manual Startup

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
| `SECRET_KEY` | Flask secret key | - | Yes |
| `BACKEND_URL` | Backend API URL | http://localhost:8000 | No |
| `MAX_CONTENT_LENGTH` | Max file size in bytes | 16777216 (16MB) | No |
| `RATE_LIMIT` | API rate limit per minute | 60 | No |
| `ANALYSIS_TIMEOUT` | Analysis timeout in seconds | 300 | No |

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
git clone https://github.com/your-username/smart-ats.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8
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
1. Check the [Issues](https://github.com/your-username/smart-ats/issues) page
2. Create a new issue with detailed information
3. Join our [Discussions](https://github.com/your-username/smart-ats/discussions)

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

