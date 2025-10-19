import firebase_admin
from firebase_admin import credentials, firestore, auth
from app.config import get_settings
from typing import Dict, List, Optional
from datetime import datetime, timezone
import os

settings = get_settings()

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            # Check if we're in development mode and credentials file doesn't exist
            if settings.environment == "development" and not os.path.exists(settings.firebase_credentials_path):
                print("⚠️  Firebase credentials not found. Running in development mode without Firebase.")
                self.db = None
                self._dev_mode = True
                return
            
            try:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self._dev_mode = False
            except Exception as e:
                print(f"⚠️  Firebase initialization failed: {e}")
                print("Running in development mode without Firebase.")
                self.db = None
                self._dev_mode = True
        else:
            self.db = firestore.client()
            self._dev_mode = False
    
    # User operations
    def create_user(self, user_data: Dict) -> str:
        if self._dev_mode:
            print(f"🔧 DEV MODE: Would create user with data: {user_data}")
            return "dev-user-id-123"
        
        user_ref = self.db.collection('users').document()
        user_data['created_at'] = datetime.now(timezone.utc)
        user_ref.set(user_data)
        return user_ref.id
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        if self._dev_mode:
            print(f"🔧 DEV MODE: Would get user with ID: {user_id}")
            return {"id": user_id, "email": "dev@example.com", "name": "Dev User"}
        
        user_ref = self.db.collection('users').document(user_id)
        user = user_ref.get()
        return user.to_dict() if user.exists else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        if self._dev_mode:
            print(f"🔧 DEV MODE: Would get user by email: {email}")
            # In dev mode, return None to allow registration
            return None
        
        users = self.db.collection('users').where('email', '==', email).limit(1).stream()
        for user in users:
            data = user.to_dict()
            data['id'] = user.id
            return data
        return None
    
    # Job operations
    def create_job(self, job_data: Dict) -> str:
        job_ref = self.db.collection('jobs').document()
        job_data['created_at'] = datetime.now(timezone.utc)
        job_data['status'] = 'active'
        job_data['applications_count'] = 0
        job_ref.set(job_data)
        return job_ref.id
    
    def get_jobs(self, filters: Dict = None, limit: int = 50) -> List[Dict]:
        if self._dev_mode:
            print(f"🔧 DEV MODE: Would get jobs with filters: {filters}")
            # Return mock jobs for development
            return [
                {
                    "id": "dev-job-1",
                    "title": "Software Developer",
                    "description": "Full-stack development role",
                    "parish": "Kingston",
                    "pay": 65000,
                    "required_skills": ["Python", "React"],
                    "job_type": "full_time",
                    "employer_id": "dev-employer-1",
                    "created_at": datetime.now(timezone.utc),
                    "status": "active",
                    "applications_count": 0
                },
                {
                    "id": "dev-job-2", 
                    "title": "Marketing Manager",
                    "description": "Digital marketing role",
                    "parish": "St. James",
                    "pay": 50000,
                    "required_skills": ["Marketing", "Social Media"],
                    "job_type": "full_time",
                    "employer_id": "dev-employer-2",
                    "created_at": datetime.now(timezone.utc),
                    "status": "active",
                    "applications_count": 0
                }
            ]
        
        query = self.db.collection('jobs')
        
        if filters:
            if filters.get('parish'):
                query = query.where('parish', '==', filters['parish'])
            if filters.get('status'):
                query = query.where('status', '==', filters['status'])
        
        jobs = query.limit(limit).stream()
        return [{'id': job.id, **job.to_dict()} for job in jobs]
    
    # Gig operations
    def create_gig(self, gig_data: Dict) -> str:
        gig_ref = self.db.collection('micro_gigs').document()
        gig_data['created_at'] = datetime.now(timezone.utc)
        gig_data['status'] = 'available'
        gig_ref.set(gig_data)
        return gig_ref.id
    
    def get_available_gigs(self, parish: str = None) -> List[Dict]:
        if self._dev_mode:
            print(f"🔧 DEV MODE: Would get available gigs for parish: {parish}")
            # Return mock gigs for development
            mock_gigs = [
                {
                    "id": "dev-gig-1",
                    "title": "Website Design",
                    "description": "Design a company website",
                    "parish": "Kingston",
                    "payment": 5000,
                    "estimated_time": "7 days",
                    "difficulty": "medium",
                    "agency_id": "dev-agency-1",
                    "created_at": datetime.now(timezone.utc),
                    "status": "available",
                    "claimed_by": None,
                    "completed_at": None
                },
                {
                    "id": "dev-gig-2",
                    "title": "Social Media Management",
                    "description": "Manage social media accounts",
                    "parish": "St. James",
                    "payment": 3000,
                    "estimated_time": "14 days",
                    "difficulty": "easy",
                    "agency_id": "dev-agency-2",
                    "created_at": datetime.now(timezone.utc),
                    "status": "available",
                    "claimed_by": None,
                    "completed_at": None
                }
            ]
            
            if parish:
                return [gig for gig in mock_gigs if gig['parish'] == parish]
            return mock_gigs
        
        query = self.db.collection('micro_gigs').where('status', '==', 'available')
        if parish:
            query = query.where('parish', '==', parish)
        gigs = query.stream()
        return [{'id': gig.id, **gig.to_dict()} for gig in gigs]
    
    def claim_gig(self, gig_id: str, user_id: str) -> bool:
        gig_ref = self.db.collection('micro_gigs').document(gig_id)
        gig_ref.update({
            'status': 'claimed',
            'claimed_by': user_id,
            'claimed_at': datetime.now(timezone.utc)
        })
        return True
    
    def complete_gig(self, gig_id: str, user_id: str) -> bool:
        # Update gig status
        gig_ref = self.db.collection('micro_gigs').document(gig_id)
        gig = gig_ref.get().to_dict()
        
        gig_ref.update({
            'status': 'completed',
            'completed_at': datetime.now(timezone.utc)
        })
        
        # Update user earnings
        user_ref = self.db.collection('users').document(user_id)
        user_ref.update({
            'completed_gigs': firestore.Increment(1),
            'total_earnings': firestore.Increment(gig['payment'])
        })
        
        return True
    
    # Analytics
    def get_analytics_data(self) -> Dict:
        if self._dev_mode:
            print("🔧 DEV MODE: Would get analytics data")
            # Return mock analytics data for development
            return {
                'total_gigs': 15,
                'gigs_by_parish': {
                    'Kingston': 8,
                    'St. James': 4,
                    'St. Andrew': 3
                },
                'skills_in_demand': [
                    {'skill': 'Python', 'demand': 85, 'jobs': 12},
                    {'skill': 'JavaScript', 'demand': 78, 'jobs': 10},
                    {'skill': 'Marketing', 'demand': 65, 'jobs': 8},
                    {'skill': 'Design', 'demand': 72, 'jobs': 9}
                ],
                'unemployment_by_parish': {
                    'Kingston': 8.2,
                    'St. James': 12.1,
                    'St. Andrew': 6.8,
                    'Clarendon': 15.3
                },
                'timestamp': datetime.now(timezone.utc)
            }
        
        # Get gigs per parish
        gigs = self.db.collection('micro_gigs').stream()
        parish_counts = {}
        total_gigs = 0
        
        for gig in gigs:
            data = gig.to_dict()
            parish = data.get('parish', 'unknown')
            parish_counts[parish] = parish_counts.get(parish, 0) + 1
            total_gigs += 1
        
        return {
            'total_gigs': total_gigs,
            'gigs_by_parish': parish_counts,
            'timestamp': datetime.now(timezone.utc)
        }

firebase_service = FirebaseService()