from typing import List, Dict
from utils.parish_data import get_parish_coordinates, calculate_distance
from services.firebase_service import firebase_service
import numpy as np

class MatchingService:
    def __init__(self):
        self.firebase = firebase_service
    
    def calculate_skill_match(self, user_skills: List[str], required_skills: List[str]) -> float:
        if not required_skills:
            return 1.0
        
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        matches = sum(1 for skill in required_skills_lower if skill in user_skills_lower)
        return matches / len(required_skills_lower)
    
    def calculate_match_score(
        self,
        user: Dict,
        job: Dict,
        max_distance_km: float = 50
    ) -> Dict:
        # Get coordinates
        user_coords = get_parish_coordinates(user['parish'])
        job_coords = get_parish_coordinates(job['parish'])
        
        if not user_coords or not job_coords:
            distance = 0
        else:
            distance = calculate_distance(
                user_coords['lat'], user_coords['lon'],
                job_coords['lat'], job_coords['lon']
            )
        
        # Calculate skill match
        skill_match = self.calculate_skill_match(
            user.get('skills', []),
            job.get('required_skills', [])
        )
        
        # Distance score (closer is better)
        distance_score = max(0, 1 - (distance / max_distance_km))
        
        # Combined score (weighted)
        final_score = (skill_match * 0.6) + (distance_score * 0.4)
        
        reasons = []
        if skill_match > 0.7:
            reasons.append(f"Strong skill match ({skill_match*100:.0f}%)")
        if distance < 20:
            reasons.append(f"Close proximity ({distance:.1f}km)")
        if user['parish'] == job['parish']:
            reasons.append("Same parish")
        
        return {
            'job_id': job['id'],
            'score': final_score,
            'distance_km': distance,
            'skill_match_percentage': skill_match * 100,
            'reasons': reasons,
            'job_title': job['title'],
            'parish': job['parish'],
            'pay': job['pay']
        }
    
    def get_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        # Get user data
        user = self.firebase.get_user(user_id)
        if not user:
            return []
        
        # Get all active jobs
        jobs = self.firebase.get_jobs({'status': 'active'}, limit=100)
        
        # Calculate scores for all jobs
        matches = []
        for job in jobs:
            match = self.calculate_match_score(user, job)
            matches.append(match)
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:limit]

matching_service = MatchingService()