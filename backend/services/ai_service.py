import google.generativeai as genai
import os
import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from ..utils.document_parser import TextAnalyzer
    from ..models.ats_models import AnalysisResult, GrammarIssue, RepetitionIssue, FormatIssue, AnalysisStatus
except ImportError:
    # For running standalone or tests
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.document_parser import TextAnalyzer
    from models.ats_models import AnalysisResult, GrammarIssue, RepetitionIssue, FormatIssue, AnalysisStatus

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalysisService:
    """Enhanced AI service for comprehensive ATS analysis"""
    
    def __init__(self):
        """Initialize the AI service with Gemini API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.text_analyzer = TextAnalyzer()
    
    def analyze_resume_comprehensive(self, resume_text: str, job_description: str) -> AnalysisResult:
        """Perform comprehensive ATS analysis including AI evaluation and text analysis"""
        analysis_id = str(uuid.uuid4())
        
        try:
            # 1. AI-based analysis
            ai_result = self._get_ai_analysis(resume_text, job_description)
            
            # 2. Grammar analysis
            grammar_issues = self._analyze_grammar_enhanced(resume_text)
            
            # 3. Word repetition analysis
            repetition_issues = self._analyze_repetitions(resume_text)
            
            # 4. Format and readability analysis
            format_issues = self._analyze_format(resume_text)
            readability_score = self.text_analyzer.calculate_readability_score(resume_text)
            
            # 5. Calculate overall percentage score
            overall_score = self._calculate_overall_score(
                ai_result.get('jd_match', 0),
                grammar_issues,
                repetition_issues,
                format_issues,
                readability_score
            )
            
            # Create comprehensive result
            result = AnalysisResult(
                id=analysis_id,
                percentage_score=overall_score,
                jd_match=ai_result.get('jd_match', 0),
                missing_keywords=ai_result.get('missing_keywords', []),
                profile_summary=ai_result.get('profile_summary', ''),
                grammar_mistakes=grammar_issues,
                word_repetitions=repetition_issues,
                format_issues=format_issues,
                readability_score=readability_score,
                timestamp=datetime.now(),
                status=AnalysisStatus.COMPLETED
            )
            
            logger.info(f"Analysis completed for ID: {analysis_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            return AnalysisResult(
                id=analysis_id,
                percentage_score=0,
                jd_match=0,
                missing_keywords=[],
                profile_summary="Analysis failed due to an error",
                grammar_mistakes=[],
                word_repetitions=[],
                format_issues=[],
                readability_score=0,
                timestamp=datetime.now(),
                status=AnalysisStatus.FAILED
            )
    
    def _get_ai_analysis(self, resume_text: str, job_description: str) -> Dict:
        """Get AI-based analysis from Gemini with fallback"""
        prompt = self._create_enhanced_prompt(resume_text, job_description)
        
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                result = self._parse_ai_response(response.text)
                # If AI analysis succeeds but returns 0, provide a basic fallback score
                if result.get('jd_match', 0) == 0:
                    logger.warning("AI returned 0% match, applying fallback scoring")
                    fallback_score = self._calculate_fallback_score(resume_text, job_description)
                    result['jd_match'] = fallback_score
                return result
            else:
                logger.error("AI response was empty")
                raise Exception("Empty AI response")
        except Exception as e:
            logger.error(f"AI analysis error: {str(e)}")
            # Fallback to keyword-based analysis
            fallback_score = self._calculate_fallback_score(resume_text, job_description)
            return {
                'jd_match': fallback_score,
                'missing_keywords': self._extract_missing_keywords(resume_text, job_description),
                'profile_summary': 'Analysis completed with fallback method due to AI service issue'
            }
    
    def _calculate_fallback_score(self, resume_text: str, job_description: str) -> float:
        """Calculate basic keyword matching score as fallback"""
        try:
            # Extract keywords from job description
            jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower()))
            # Remove common words
            common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
            jd_keywords = jd_words - common_words
            
            # Count matches in resume
            resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
            matches = len(jd_keywords.intersection(resume_words))
            total_keywords = max(len(jd_keywords), 1)
            
            # Calculate percentage with some baseline
            base_score = min(85, max(35, (matches / total_keywords) * 100))  # 35-85% range
            
            logger.info(f"Fallback scoring: {matches}/{total_keywords} keywords matched = {base_score}%")
            return round(base_score, 2)
            
        except Exception as e:
            logger.error(f"Fallback scoring error: {str(e)}")
            return 45.0  # Default reasonable score
    
    def _extract_missing_keywords(self, resume_text: str, job_description: str) -> List[str]:
        """Extract missing keywords for fallback analysis"""
        try:
            jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower()))
            resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
            
            # Find important missing words (longer words are usually more important)
            missing = [word for word in jd_words if word not in resume_words and len(word) > 5]
            return sorted(missing, key=len, reverse=True)[:8]  # Return top 8 missing keywords
            
        except Exception:
            return ['skills', 'experience', 'requirements']
    
    def _create_enhanced_prompt(self, resume_text: str, job_description: str) -> str:
        """Create enhanced prompt for comprehensive analysis"""
        return f"""
        Act as an expert ATS (Application Tracking System) with deep knowledge in recruitment, 
        HR analytics, and professional resume evaluation. Analyze the provided resume against 
        the job description with the highest accuracy and professional insight.

        **ANALYSIS REQUIREMENTS:**
        1. Calculate precise percentage match (0-100) based on skills, experience, and requirements alignment
        2. Focus primarily on technical skills, experience relevance, and job requirement matches
        3. Identify specific missing keywords that are critical for the role
        4. Provide constructive career-focused recommendations and avoid detailed grammar analysis
        5. Consider industry standards and current job market competitiveness
        6. Emphasize content substance, skill alignment, and career development over writing mechanics
        7. Prioritize ATS compatibility and keyword optimization over linguistic perfection

        **RESUME:**
        {resume_text}

        **JOB DESCRIPTION:**
        {job_description}

        **REQUIRED OUTPUT FORMAT (JSON):**
        Return ONLY a valid JSON object with these exact fields:
        {{
            "jd_match": 75,
            "missing_keywords": ["Python", "Machine Learning", "SQL"],
            "profile_summary": "Professional analysis focusing on career alignment and skill gaps with actionable career advice",
            "strengths": ["Strong technical background", "Relevant experience"],
            "weaknesses": ["Missing cloud experience", "Limited leadership background"],
            "recommendations": ["Add cloud certifications", "Highlight team collaboration"]
        }}
        
        CRITICAL REQUIREMENTS:
        - jd_match must be a single number between 0-100 (not a list or string)
        - missing_keywords must be an array of strings
        - All fields are required
        - Return only the JSON object, no additional text

        **IMPORTANT:** Focus exclusively on career development, skill gaps, and ATS optimization. 
        Do NOT analyze grammar, writing style, or linguistic elements.
        Provide actionable insights for improving job match percentage and career advancement.
        """
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response with error handling"""
        try:
            # Log the raw response for debugging
            logger.info(f"AI Raw Response: {response_text[:500]}...")  # First 500 chars
            
            # Clean the response to extract JSON
            cleaned_response = self._clean_json_response(response_text)
            logger.info(f"Cleaned JSON: {cleaned_response[:300]}...")  # First 300 chars
            
            result = json.loads(cleaned_response)
            logger.info(f"Parsed JSON result: {result}")
            
            # Validate and sanitize the result
            jd_match_value = result.get('jd_match', 0)
            
            # Handle cases where AI returns a list or other non-numeric types
            if isinstance(jd_match_value, list):
                jd_match_value = jd_match_value[0] if jd_match_value else 0
            elif isinstance(jd_match_value, str):
                try:
                    jd_match_value = float(jd_match_value)
                except ValueError:
                    jd_match_value = 0
            elif not isinstance(jd_match_value, (int, float)):
                jd_match_value = 0
            
            processed_result = {
                'jd_match': min(100, max(0, float(jd_match_value))),
                'missing_keywords': result.get('missing_keywords', [])[:10],  # Limit to 10
                'profile_summary': result.get('profile_summary', '')[:1000],  # Limit length
                'strengths': result.get('strengths', [])[:5],
                'weaknesses': result.get('weaknesses', [])[:5],
                'recommendations': result.get('recommendations', [])[:5]
            }
            
            logger.info(f"Final processed result: {processed_result}")
            return processed_result
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            logger.error(f"Full response text: {response_text}")
            return {'jd_match': 0, 'missing_keywords': [], 'profile_summary': 'Failed to parse AI response'}
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean and extract JSON from AI response"""
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)
        
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json_match.group()
        
        return response_text.strip()
    
    def _analyze_grammar_enhanced(self, text: str) -> List[GrammarIssue]:
        """Minimal grammar analysis focused only on ATS-critical formatting"""
        issues = []
        
        # Only check for ATS-critical issues that affect parsing (not linguistic grammar)
        # Focus on formatting consistency that impacts ATS readability
        
        # Check for severely inconsistent bullet point formatting only
        lines = text.split('\n')
        bullet_formats = []
        
        for line in lines:
            if re.match(r'^\s*[-*•]', line.strip()):
                bullet_formats.append(line.strip()[0:3])
        
        # Only flag if there are more than 2 different bullet formats (major inconsistency)
        if len(set(bullet_formats)) > 2 and len(bullet_formats) > 5:
            issues.append({
                'text': 'Multiple bullet point formats detected',
                'line_number': 1,
                'suggestion': 'Use consistent bullet point formatting for better ATS parsing',
                'severity': 'low'
            })
        
        # Limit to maximum 2 issues and only if they truly impact ATS parsing
        return [
            GrammarIssue(
                text=issue['text'],
                line_number=issue['line_number'],
                suggestion=issue['suggestion'],
                severity=issue['severity']
            )
            for issue in issues[:2]  # Maximum 2 issues, only ATS-critical formatting
        ]
    
    def _get_critical_grammar_suggestion(self, issue_type: str) -> str:
        """Get suggestions for ATS-critical formatting only"""
        suggestions = {
            'bullet_formatting': 'Use consistent bullet point formatting for better ATS parsing',
        }
        return suggestions.get(issue_type, 'Consider reviewing for ATS compatibility')
    
    def _analyze_repetitions(self, text: str) -> List[RepetitionIssue]:
        """Very lenient repetition analysis - only flag extreme overuse"""
        words = re.findall(r'\b[a-zA-Z]{6,}\b', text.lower())  # Only words 6+ chars
        word_count = {}
        word_positions = {}
        
        for i, word in enumerate(words):
            if word not in word_count:
                word_count[word] = 0
                word_positions[word] = []
            word_count[word] += 1
            word_positions[word].append(i)
        
        # Only flag words repeated more than 8 times (very lenient)
        repetitions = []
        for word, count in word_count.items():
            if count > 8 and len(word) > 6:  # Very strict thresholds
                repetitions.append({
                    'word': word,
                    'count': count,
                    'positions': word_positions[word]
                })
        
        # Limit to top 2 most repeated words only
        repetitions = sorted(repetitions, key=lambda x: x['count'], reverse=True)[:2]
        
        return [
            RepetitionIssue(
                word=rep['word'],
                count=rep['count'],
                positions=rep['positions']
            )
            for rep in repetitions
        ]
    
    def _analyze_format(self, text: str) -> List[FormatIssue]:
        """Minimal format analysis focusing only on ATS-critical parsing issues"""
        issues = []
        
        # Only check for the most critical ATS parsing issues
        
        # Check for missing contact information (critical for ATS)
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        
        if not has_email:
            issues.append({
                'issue_type': 'ats_critical',
                'description': 'Email address not clearly identifiable by ATS',
                'suggestion': 'Ensure email address is clearly visible for ATS parsing'
            })
        
        # Check for basic section structure (only if severely lacking)
        has_experience_section = bool(re.search(r'\b(experience|work|employment|professional)\b', text, re.IGNORECASE))
        has_skills_section = bool(re.search(r'\b(skills|competencies|technical)\b', text, re.IGNORECASE))
        
        if not (has_experience_section or has_skills_section):
            issues.append({
                'issue_type': 'ats_structure',
                'description': 'Missing clear section identifiers',
                'suggestion': 'Add section headers like "Experience" or "Skills" for better ATS parsing'
            })
        
        # Only return 1 most critical issue to minimize emphasis on formatting
        return [
            FormatIssue(
                issue_type=issue['issue_type'],
                description=issue['description'],
                suggestion=issue['suggestion']
            )
            for issue in issues[:1]  # Maximum 1 issue to minimize format emphasis
        ]
    
    def _calculate_overall_score(self, 
                               jd_match: float, 
                               grammar_issues: List[GrammarIssue],
                               repetition_issues: List[RepetitionIssue],
                               format_issues: List[FormatIssue],
                               readability_score: float) -> float:
        """Calculate overall ATS score based on all factors"""
        
        # Debug logging to identify scoring issues
        logger.info(f"Scoring Debug - JD Match: {jd_match}")
        logger.info(f"Scoring Debug - Grammar Issues: {len(grammar_issues)}")
        logger.info(f"Scoring Debug - Repetition Issues: {len(repetition_issues)}")
        logger.info(f"Scoring Debug - Format Issues: {len(format_issues)}")
        logger.info(f"Scoring Debug - Readability Score: {readability_score}")
        
        # Weight distribution - heavily emphasizing content relevance over language mechanics
        weights = {
            'jd_match': 0.70,     # 70% - Primary focus on job alignment
            'grammar': 0.05,      # 5% - Minimal emphasis on grammar
            'repetition': 0.05,   # 5% - Minimal emphasis on repetition
            'format': 0.15,       # 15% - Structure remains important for ATS
            'readability': 0.05   # 5% - Basic readability only
        }
        
        # Calculate component scores with very lenient penalties for language mechanics
        grammar_score = max(0, 100 - len(grammar_issues) * 3)  # Very minimal penalty: 3 per issue
        repetition_score = max(0, 100 - len(repetition_issues) * 5)  # Very minimal penalty: 5 per issue
        format_score = max(0, 100 - len(format_issues) * 8)  # Reduced penalty: 8 per issue
        
        logger.info(f"Component Scores - Grammar: {grammar_score}, Repetition: {repetition_score}, Format: {format_score}")
        
        # Calculate weighted average
        overall_score = (
            jd_match * weights['jd_match'] +
            grammar_score * weights['grammar'] +
            repetition_score * weights['repetition'] +
            format_score * weights['format'] +
            readability_score * weights['readability']
        )
        
        logger.info(f"Final calculated score: {overall_score}")
        
        return round(min(100, max(0, overall_score)), 2)

class AnalysisCache:
    """Simple in-memory cache for analysis results"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[AnalysisResult]:
        """Get cached analysis result"""
        return self._cache.get(key)
    
    def set(self, key: str, result: AnalysisResult) -> None:
        """Cache analysis result"""
        self._cache[key] = result
    
    def generate_cache_key(self, resume_text: str, job_description: str) -> str:
        """Generate cache key from resume and job description"""
        import hashlib
        content = f"{resume_text}{job_description}"
        return hashlib.md5(content.encode()).hexdigest()