# Render Deployment Fix

## The Issue
Render is looking for `requirements.txt` in the wrong directory due to the nested folder structure.

## Solution Options

### Option 1: Use Root Directory (Recommended)
Your current structure is already correct:
```
linkworkja-backend/
├── app/
├── requirements.txt
├── .gitignore
└── other files...
```

**Render Configuration:**
- **Root Directory**: Leave empty (use root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Option 2: Specify Subdirectory
If you want to keep the nested structure:

**Render Configuration:**
- **Root Directory**: `linkworkja-backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Quick Fix Steps

1. **In Render Dashboard:**
   - Go to your service settings
   - **Root Directory**: Leave empty (or set to `linkworkja-backend` if using nested structure)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables:**
   ```
   ENVIRONMENT=production
   FIREBASE_DATABASE_URL=https://jobsync-backend.firebaseio.com
   SECRET_KEY=your-secure-secret-key
   ALLOWED_ORIGINS=["https://your-frontend-domain.com"]
   DEBUG=false
   ```

3. **Firebase Credentials:**
   - Upload `dev-firebase-credentials.json` as `firebase-credentials.json`
   - Or use environment variable `FIREBASE_CREDENTIALS_JSON`

## Test Locally
```bash
# Test the exact command Render will use
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Common Issues & Solutions

### Issue: "Could not open requirements file"
**Solution**: Ensure `requirements.txt` is in the root directory that Render is looking in.

### Issue: "Module not found: app"
**Solution**: Ensure the `app` directory is in the same directory as `requirements.txt`.

### Issue: "Firebase credentials not found"
**Solution**: Upload your Firebase credentials file or set the `FIREBASE_CREDENTIALS_JSON` environment variable.

## File Structure for Deployment
```
your-repo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── requirements.txt
├── .gitignore
├── render.yaml (optional)
└── README.md
```

This structure should work perfectly with Render!
