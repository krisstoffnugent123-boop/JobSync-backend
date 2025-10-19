# Firebase Setup Guide for LinkWorkJA Backend

## Quick Setup Steps

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Name: `linkworkja` (or your choice)
4. Enable Google Analytics (optional)

### 2. Enable Required Services

#### Firestore Database
1. Go to "Firestore Database" in sidebar
2. Click "Create database"
3. Choose "Start in test mode"
4. Select location (closest to Jamaica)

#### Authentication (Optional)
1. Go to "Authentication" → "Sign-in method"
2. Enable "Email/Password" provider

### 3. Get Service Account Credentials
1. Go to Project Settings (gear icon)
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file

### 4. Configure Backend
1. Rename downloaded file to `dev-firebase-credentials.json`
2. Place it in the project root directory
3. Update `dev.env` with your project details

### 5. Update Configuration
Edit `dev.env`:
```env
FIREBASE_CREDENTIALS_PATH=./dev-firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
```

### 6. Test Connection
Run the backend:
```bash
python -m uvicorn app.main:app --reload
```

## Security Rules (Production)

### Firestore Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Jobs are readable by all authenticated users
    match /jobs/{jobId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // Gigs are readable by all authenticated users
    match /micro_gigs/{gigId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

## Environment Variables

### Development (.env)
```env
ENVIRONMENT=development
FIREBASE_CREDENTIALS_PATH=./dev-firebase-credentials.json
FIREBASE_DATABASE_URL=https://linkworkja-dev.firebaseio.com
```

### Production
```env
ENVIRONMENT=production
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
```

## Troubleshooting

### Common Issues:
1. **Credentials not found**: Ensure file is named exactly `dev-firebase-credentials.json`
2. **Permission denied**: Check Firestore security rules
3. **Connection timeout**: Verify project ID and region

### Testing Connection:
```python
from app.services.firebase_service import firebase_service
print("Development mode:", firebase_service._dev_mode)
```

## Next Steps
1. Set up Firestore collections structure
2. Configure security rules
3. Set up monitoring and alerts
4. Configure backup strategies
