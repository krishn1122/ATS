// Smart ATS Frontend JavaScript

class SmartATS {
    constructor() {
        this.initializeEventListeners();
        this.initializeFileUpload();
        this.initializeFormValidation();
    }

    initializeEventListeners() {
        // Form submission
        const uploadForm = document.getElementById('uploadForm');
        if (uploadForm) {
            uploadForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // File upload zone
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('resumeFile');
        
        if (uploadZone && fileInput) {
            uploadZone.addEventListener('click', () => fileInput.click());
            uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
            uploadZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
            uploadZone.addEventListener('drop', (e) => this.handleFileDrop(e));
            
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        // Remove file button
        const removeFileBtn = document.getElementById('removeFile');
        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', () => this.removeFile());
        }
    }

    initializeFileUpload() {
        this.allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        this.maxFileSize = 16 * 1024 * 1024; // 16MB
    }

    initializeFormValidation() {
        // Real-time validation
        const jobDescription = document.getElementById('jobDescription');
        if (jobDescription) {
            jobDescription.addEventListener('input', () => this.validateJobDescription());
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }

        this.showLoading();
        this.uploadResume();
    }

    validateForm() {
        const jobDescription = document.getElementById('jobDescription').value.trim();
        const fileInput = document.getElementById('resumeFile');
        
        if (!jobDescription) {
            this.showError('Please enter a job description');
            return false;
        }

        if (jobDescription.length < 50) {
            this.showError('Job description should be at least 50 characters long');
            return false;
        }

        if (!fileInput.files.length) {
            this.showError('Please select a resume file');
            return false;
        }

        return true;
    }

    validateJobDescription() {
        const jobDescription = document.getElementById('jobDescription');
        const length = jobDescription.value.trim().length;
        
        if (length > 0 && length < 50) {
            jobDescription.classList.add('is-invalid');
        } else {
            jobDescription.classList.remove('is-invalid');
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        const uploadZone = document.getElementById('uploadZone');
        uploadZone.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        const uploadZone = document.getElementById('uploadZone');
        uploadZone.classList.remove('dragover');
    }

    handleFileDrop(e) {
        e.preventDefault();
        const uploadZone = document.getElementById('uploadZone');
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        if (!this.validateFile(file)) {
            return;
        }

        const fileInput = document.getElementById('resumeFile');
        const uploadZone = document.getElementById('uploadZone');
        const uploadContent = uploadZone.querySelector('.upload-content');
        const fileInfo = uploadZone.querySelector('.file-info');
        const fileName = fileInfo.querySelector('.file-name');
        const fileSize = fileInfo.querySelector('.file-size');

        // Update file input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // Show file info
        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        
        uploadContent.classList.add('d-none');
        fileInfo.classList.remove('d-none');
    }

    validateFile(file) {
        if (!this.allowedTypes.includes(file.type)) {
            this.showError('Please upload only PDF or DOCX files');
            return false;
        }

        if (file.size > this.maxFileSize) {
            this.showError('File size must be less than 16MB');
            return false;
        }

        return true;
    }

    removeFile() {
        const fileInput = document.getElementById('resumeFile');
        const uploadZone = document.getElementById('uploadZone');
        const uploadContent = uploadZone.querySelector('.upload-content');
        const fileInfo = uploadZone.querySelector('.file-info');

        fileInput.value = '';
        uploadContent.classList.remove('d-none');
        fileInfo.classList.add('d-none');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async uploadResume() {
        const form = document.getElementById('uploadForm');
        const formData = new FormData(form);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                if (result.data && result.data.analysis_id) {
                    // Analysis started, poll for results
                    this.pollAnalysisResult(result.data.analysis_id);
                } else {
                    // Analysis completed immediately
                    this.hideLoading();
                    this.redirectToResults(result.data);
                }
            } else {
                this.hideLoading();
                this.showError(result.message || 'Upload failed');
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Network error. Please check your connection and try again.');
            console.error('Upload error:', error);
        }
    }

    async pollAnalysisResult(analysisId) {
        const maxAttempts = 60; // 5 minutes timeout
        let attempts = 0;

        const poll = async () => {
            try {
                attempts++;
                
                const response = await fetch(`/api/analysis/${analysisId}/status`);
                const status = await response.json();

                if (status.status === 'completed') {
                    // Get full results
                    const resultResponse = await fetch(`/api/analysis/${analysisId}`);
                    const result = await resultResponse.json();
                    
                    this.hideLoading();
                    if (result.success) {
                        this.redirectToResults(result.data);
                    } else {
                        this.showError('Failed to get analysis results');
                    }
                } else if (status.status === 'failed') {
                    this.hideLoading();
                    this.showError('Analysis failed. Please try again.');
                } else if (attempts < maxAttempts) {
                    // Continue polling
                    setTimeout(poll, 5000); // Poll every 5 seconds
                } else {
                    this.hideLoading();
                    this.showError('Analysis timed out. Please try again.');
                }
            } catch (error) {
                this.hideLoading();
                this.showError('Error checking analysis status');
                console.error('Polling error:', error);
            }
        };

        poll();
    }

    redirectToResults(data) {
        // Store results in sessionStorage for the results page
        sessionStorage.setItem('analysisResult', JSON.stringify(data));
        window.location.href = `/results/${data.id}`;
    }

    showLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('d-none');
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.add('d-none');
        }
    }

    showError(message) {
        // Create error alert
        const alertContainer = document.querySelector('.container.mt-3') || document.querySelector('.container');
        if (alertContainer) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-danger alert-dismissible fade show';
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            alertContainer.insertBefore(alert, alertContainer.firstChild);

            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        } else {
            alert(message);
        }
    }

    showSuccess(message) {
        const alertContainer = document.querySelector('.container.mt-3') || document.querySelector('.container');
        if (alertContainer) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-success alert-dismissible fade show';
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            alertContainer.insertBefore(alert, alertContainer.firstChild);

            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        }
    }
}

// Results page functionality
class ResultsPage {
    constructor() {
        this.initializeResults();
    }

    async initializeResults() {
        const analysisId = this.getAnalysisIdFromUrl();
        if (!analysisId) {
            this.showError('Invalid analysis ID');
            return;
        }

        // Try to get results from sessionStorage first
        const storedResults = sessionStorage.getItem('analysisResult');
        if (storedResults) {
            const data = JSON.parse(storedResults);
            this.displayResults(data);
            sessionStorage.removeItem('analysisResult');
            return;
        }

        // Fetch from API
        try {
            const response = await fetch(`/api/analysis/${analysisId}`);
            const result = await response.json();

            if (result.success) {
                this.displayResults(result.data);
            } else {
                this.showError('Failed to load analysis results');
            }
        } catch (error) {
            this.showError('Error loading results');
            console.error('Results error:', error);
        }
    }

    getAnalysisIdFromUrl() {
        const path = window.location.pathname;
        const parts = path.split('/');
        return parts[parts.length - 1];
    }

    displayResults(data) {
        // Update score display
        this.updateScoreDisplay(data.percentage_score);
        
        // Update individual metrics
        this.updateMetrics(data);
        
        // Display analysis details
        this.displayAnalysisDetails(data);
        
        // Show missing keywords
        this.displayMissingKeywords(data.missing_keywords);
        
        // Show grammar issues
        this.displayGrammarIssues(data.grammar_mistakes);
        
        // Show repetition issues
        this.displayRepetitionIssues(data.word_repetitions);
        
        // Show format issues
        this.displayFormatIssues(data.format_issues);
    }

    updateScoreDisplay(score) {
        const scoreElement = document.getElementById('overallScore');
        const scoreCircle = document.getElementById('scoreCircle');
        
        if (scoreElement) {
            scoreElement.textContent = score + '%';
        }
        
        if (scoreCircle) {
            // Add appropriate class based on score
            const scoreClass = this.getScoreClass(score);
            scoreCircle.className = `score-circle ${scoreClass}`;
        }
    }

    getScoreClass(score) {
        if (score >= 80) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 40) return 'score-average';
        return 'score-poor';
    }

    updateMetrics(data) {
        const metrics = {
            'jdMatch': data.jd_match,
            'readabilityScore': data.readability_score,
            'grammarIssues': data.grammar_mistakes.length,
            'repetitionIssues': data.word_repetitions.length
        };

        Object.entries(metrics).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = typeof value === 'number' ? 
                    (id.includes('Score') || id.includes('Match') ? value + '%' : value) : value;
            }
        });
    }

    displayAnalysisDetails(data) {
        const summaryElement = document.getElementById('profileSummary');
        if (summaryElement) {
            summaryElement.textContent = data.profile_summary;
        }
    }

    displayMissingKeywords(keywords) {
        const container = document.getElementById('missingKeywords');
        if (container && keywords.length > 0) {
            container.innerHTML = keywords.map(keyword => 
                `<span class="badge bg-warning text-dark me-2 mb-2">${keyword}</span>`
            ).join('');
        }
    }

    displayGrammarIssues(issues) {
        const container = document.getElementById('grammarIssues');
        if (container) {
            if (issues.length === 0) {
                container.innerHTML = '<p class="text-success"><i class="fas fa-check"></i> No grammar issues found!</p>';
            } else {
                container.innerHTML = issues.map(issue => `
                    <div class="issue-card grammar">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <strong>Line ${issue.line_number}:</strong> ${issue.text}
                                <div class="text-muted small mt-1">${issue.suggestion}</div>
                            </div>
                            <span class="badge bg-danger">${issue.severity}</span>
                        </div>
                    </div>
                `).join('');
            }
        }
    }

    displayRepetitionIssues(issues) {
        const container = document.getElementById('repetitionIssues');
        if (container) {
            if (issues.length === 0) {
                container.innerHTML = '<p class="text-success"><i class="fas fa-check"></i> No excessive word repetition found!</p>';
            } else {
                container.innerHTML = issues.map(issue => `
                    <div class="issue-card repetition">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>"${issue.word}"</strong> appears <strong>${issue.count}</strong> times
                            </div>
                            <span class="badge bg-warning">Repetition</span>
                        </div>
                    </div>
                `).join('');
            }
        }
    }

    displayFormatIssues(issues) {
        const container = document.getElementById('formatIssues');
        if (container) {
            if (issues.length === 0) {
                container.innerHTML = '<p class="text-success"><i class="fas fa-check"></i> No format issues found!</p>';
            } else {
                container.innerHTML = issues.map(issue => `
                    <div class="issue-card format">
                        <div>
                            <strong>${issue.issue_type}:</strong> ${issue.description}
                            <div class="text-muted small mt-1">${issue.suggestion}</div>
                        </div>
                    </div>
                `).join('');
            }
        }
    }

    showError(message) {
        const container = document.querySelector('.container');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger text-center">
                    <h4>Error</h4>
                    <p>${message}</p>
                    <a href="/" class="btn btn-primary">Try Again</a>
                </div>
            `;
        }
    }
}

// Dashboard functionality
class Dashboard {
    constructor() {
        this.initializeDashboard();
    }

    async initializeDashboard() {
        try {
            const response = await fetch('/api/analytics/summary');
            const data = await response.json();
            
            this.updateStats(data);
            this.createCharts(data);
        } catch (error) {
            console.error('Dashboard error:', error);
            this.showDashboardError();
        }
    }

    updateStats(data) {
        const stats = {
            'totalAnalyses': data.total_analyses,
            'averageScore': data.average_score + '%',
            'successRate': data.success_rate + '%',
            'completedAnalyses': data.completed_analyses
        };

        Object.entries(stats).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    createCharts(data) {
        // Create score distribution chart
        this.createScoreChart(data);
        
        // Create issues chart
        this.createIssuesChart(data);
    }

    createScoreChart(data) {
        const ctx = document.getElementById('scoreChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Excellent (80-100%)', 'Good (60-79%)', 'Average (40-59%)', 'Poor (0-39%)'],
                datasets: [{
                    data: [25, 35, 25, 15], // Example data
                    backgroundColor: ['#059669', '#0891b2', '#d97706', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createIssuesChart(data) {
        const ctx = document.getElementById('issuesChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Grammar', 'Format', 'Repetition'],
                datasets: [{
                    label: 'Common Issues',
                    data: [
                        data.common_grammar_issues?.length || 0,
                        data.common_format_issues?.length || 0,
                        5 // Example repetition data
                    ],
                    backgroundColor: ['#dc2626', '#2563eb', '#d97706']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    showDashboardError() {
        const container = document.querySelector('.dashboard-content');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-warning text-center">
                    <h4>Dashboard Unavailable</h4>
                    <p>Unable to load analytics data. Please try again later.</p>
                </div>
            `;
        }
    }
}

// Initialize based on current page
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index') {
        new SmartATS();
    } else if (path.includes('/results/')) {
        new ResultsPage();
    } else if (path === '/dashboard') {
        new Dashboard();
    }
});

// Export for global access
window.SmartATS = SmartATS;
window.ResultsPage = ResultsPage;
window.Dashboard = Dashboard;