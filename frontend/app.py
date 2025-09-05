from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import os
import logging
from werkzeug.utils import secure_filename
import time
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and analysis"""
    try:
        # Check if file is in request
        if 'resume' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not job_description.strip():
            return jsonify({'success': False, 'message': 'Job description is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False, 
                'message': 'Invalid file format. Please upload PDF or DOCX files only.'
            }), 400
        
        # Prepare file for backend
        files = {'resume_file': (file.filename, file.read(), file.content_type)}
        data = {'job_description': job_description}
        
        # Send to backend
        response = requests.post(
            f'{BACKEND_URL}/api/analyze-resume',
            files=files,
            data=data,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            logger.error(f"Backend error: {response.status_code} - {response.text}")
            return jsonify({
                'success': False, 
                'message': 'Analysis failed. Please try again.'
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False, 
            'message': 'Analysis timed out. Please try again with a smaller file.'
        }), 408
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False, 
            'message': 'Backend service unavailable. Please try again later.'
        }), 503
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'An unexpected error occurred. Please try again.'
        }), 500

@app.route('/api/analysis/<analysis_id>')
def get_analysis(analysis_id):
    """Get analysis result by ID"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/analysis/{analysis_id}', timeout=30)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({'success': False, 'message': 'Analysis not found'}), 404
        else:
            return jsonify({'success': False, 'message': 'Failed to retrieve analysis'}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False, 
            'message': 'Backend service unavailable'
        }), 503
    except Exception as e:
        logger.error(f"Get analysis error: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to retrieve analysis'}), 500

@app.route('/api/analysis/<analysis_id>/status')
def get_analysis_status(analysis_id):
    """Get analysis status"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/analysis/{analysis_id}/status', timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to get status'}), 500
            
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({'error': 'Status check failed'}), 500

@app.route('/api/analytics/summary')
def get_analytics_summary():
    """Get analytics summary from backend"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/analytics/summary', timeout=30)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to get analytics'}), 500
            
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({'error': 'Analytics unavailable'}), 500

@app.route('/results/<analysis_id>')
def results(analysis_id):
    """Results page"""
    return render_template('results.html', analysis_id=analysis_id)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False, 
        'message': 'File too large. Please upload a file smaller than 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

def create_app():
    """Create and configure Flask app"""
    return app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)