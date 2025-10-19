# LinkWorkJA Backend Setup Guide

## 🚀 Quick Start (Development Mode)

The application is now configured to run in development mode without requiring Firebase credentials.

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Run Tests
```bash
python3 -m pytest tests/test_api.py -v
```

### 3. Start Development Server
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Development Configuration
The app uses `dev.env` for development settings. Current defaults:
- **Environment**: development
- **Firebase**: Runs in mock mode (no credentials required)
- **CORS**: Allows localhost:3000 and localhost:3001
- **Debug**: Enabled

### Production Configuration
For production, create a `.env` file with:
```env
ENVIRONMENT=production
DEBUG=false
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
GOOGLE_AI_API_KEY=your-actual-api-key
SECRET_KEY=your-production-secret-key
```

## 🔥 Firebase Setup (Optional for Development)

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database
4. Generate service account credentials

### 2. Download Credentials
1. Go to Project Settings → Service Accounts
2. Generate new private key
3. Save as `firebase-credentials.json` in project root

### 3. Update Configuration
Update `dev.env` with your Firebase project URL:
```env
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
```

## 🧪 Testing

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Specific Test
```bash
python3 -m pytest tests/test_api.py::test_root -v
```

### Test Coverage
```bash
pip3 install pytest-cov
python3 -m pytest tests/ --cov=app --cov-report=html
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Development Features

### Development Mode
- Firebase runs in mock mode (no credentials required)
- All database operations are logged but not executed
- CORS allows localhost origins
- Debug logging enabled

### Available Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /docs` - API documentation
- Authentication routes (under `/auth/`)
- Job management routes (under `/jobs/`)
- Gig management routes (under `/gigs/`)
- Matching routes (under `/matching/`)
- Analytics routes (under `/analytics/`)

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root directory
2. **Port Already in Use**: Change the port in the uvicorn command
3. **Firebase Errors**: The app will run in development mode without Firebase
4. **CORS Issues**: Check `allowed_origins` in configuration

### Development Mode Indicators
Look for these messages in the console:
- `⚠️ Firebase credentials not found. Running in development mode without Firebase.`
- `🔧 DEV MODE: Would create user with data: {...}`

## 📝 Next Steps

1. **Set up Firebase** (optional for development)
2. **Configure Google AI API** for AI features
3. **Add more tests** for specific endpoints
4. **Set up CI/CD** pipeline
5. **Configure production environment**

## 🔗 Useful Commands

```bash
# Start server with auto-reload
python3 -m uvicorn app.main:app --reload

# Run tests with coverage
python3 -m pytest tests/ --cov=app

# Check code formatting
python3 -m black app/

# Type checking
python3 -m mypy app/
```

