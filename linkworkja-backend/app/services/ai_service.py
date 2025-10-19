import google.generativeai as genai
from app.config import get_settings
from typing import List, Dict

settings = get_settings()
genai.configure(api_key=settings.google_ai_api_key)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_job_description(self, title: str, parish: str, skills: List[str]) -> str:
        prompt = f"""
        Generate a professional job description for a position in Jamaica.
        
        Job Title: {title}
        Location: {parish}, Jamaica
        Required Skills: {', '.join(skills)}
        
        Create a detailed description that includes:
        - Job overview
        - Key responsibilities
        - Required qualifications
        - What makes this opportunity unique for Jamaican workers
        
        Keep it concise (150-200 words) and culturally relevant.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def suggest_skills_for_job(self, title: str, description: str) -> List[str]:
        prompt = f"""
        Based on this job posting, suggest 5-7 relevant skills required:
        
        Title: {title}
        Description: {description}
        
        Return only a comma-separated list of skills, no explanations.
        """
        
        response = self.model.generate_content(prompt)
        skills = [skill.strip() for skill in response.text.split(',')]
        return skills[:7]
    
    def generate_micro_gigs(self, count: int = 5) -> List[Dict]:
        prompt = f"""
        Generate {count} micro-gig ideas suitable for government-backed digital work in Jamaica.
        Each gig should be:
        - Completable in 1-4 hours
        - Require basic digital skills
        - Pay between $500-$2000 JMD
        
        Return as a JSON array with this structure:
        [
          {{
            "title": "Task name",
            "description": "What needs to be done",
            "estimated_time": "2 hours",
            "payment": 1000,
            "difficulty": "easy"
          }}
        ]
        
        Focus on realistic tasks like data entry, document digitization, survey collection, etc.
        """
        
        response = self.model.generate_content(prompt)
        # Parse response and return structured data
        import json
        try:
            gigs = json.loads(response.text)
            return gigs
        except:
            return []
    
    def generate_analytics_insights(self, data: Dict) -> str:
        prompt = f"""
        Analyze this employment data from Jamaica and provide 3 key insights:
        
        Data: {data}
        
        Focus on:
        - Regional employment trends
        - Growth opportunities
        - Policy recommendations
        
        Keep response under 100 words.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

ai_service = AIService()