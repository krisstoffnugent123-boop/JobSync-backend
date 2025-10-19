# Render.com Deployment Guide for LinkWorkJA Backend

## Quick Deployment Steps

### 1. **Prepare Your Repository**
- Push your code to GitHub
- Ensure all files are committed
- Make sure `requirements.txt` is up to date

### 2. **Create Render Service**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `linkworkja-backend` repository

### 3. **Configure Service Settings**

#### **Basic Settings:**
- **Name**: `linkworkja-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### **Environment Variables:**
Add these in the Render dashboard:

```
ENVIRONMENT=production
FIREBASE_DATABASE_URL=https://jobsync-backend.firebaseio.com
SECRET_KEY=your-super-secure-production-secret-key-here
GOOGLE_AI_API_KEY=your-actual-google-ai-key
ALLOWED_ORIGINS=["https://your-frontend-domain.com"]
DEBUG=false
```

### 4. **Firebase Credentials Setup**

#### **Option A: Environment Variable (Recommended)**
Add the entire JSON content as an environment variable:
```
FIREBASE_CREDENTIALS_JSON={"type":"service_account","project_id":"jobsync-backend",...}
```

Then update your `config.py`:
```python
import json
import os

# In your Settings class, add:
firebase_credentials_json: str = ""

# In your FirebaseService.__init__():
if os.getenv("FIREBASE_CREDENTIALS_JSON"):
    cred_dict = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
    cred = credentials.Certificate(cred_dict)
```

#### **Option B: File Upload**
- Upload `firebase-credentials.json` to your Render service
- Set `FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json`

### 5. **Deploy**
1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Your API will be available at: `https://your-service-name.onrender.com`

## Production Checklist

### ✅ **Before Deployment:**
- [ ] Update `SECRET_KEY` to a secure random string
- [ ] Set `DEBUG=false`
- [ ] Configure proper `ALLOWED_ORIGINS`
- [ ] Test Firebase connection
- [ ] Apply Firestore security rules

### ✅ **After Deployment:**
- [ ] Test API endpoints
- [ ] Verify Firebase connection
- [ ] Check logs for errors
- [ ] Test CORS with frontend

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment | `production` |
| `FIREBASE_DATABASE_URL` | Firebase project URL | `https://jobsync-backend.firebaseio.com` |
| `SECRET_KEY` | JWT secret key | `your-secure-secret-key` |
| `GOOGLE_AI_API_KEY` | Google AI API key | `your-google-ai-key` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `["https://yourdomain.com"]` |
| `DEBUG` | Debug mode | `false` |

## API Endpoints After Deployment

Your deployed API will be available at:
- **Base URL**: `https://your-service-name.onrender.com`
- **Health Check**: `GET /health`
- **API Docs**: `GET /docs`
- **Jobs**: `GET /jobs/`
- **Gigs**: `GET /gigs/available`

## Monitoring & Logs

### **View Logs:**
1. Go to your Render service dashboard
2. Click on "Logs" tab
3. Monitor for errors and performance

### **Common Issues:**
1. **Build Failures**: Check `requirements.txt` dependencies
2. **Runtime Errors**: Check environment variables
3. **Firebase Errors**: Verify credentials and permissions
4. **CORS Issues**: Update `ALLOWED_ORIGINS`

## Security Considerations

### **Production Security:**
1. **Never commit credentials** to your repository
2. **Use environment variables** for sensitive data
3. **Apply Firestore security rules** before going live
4. **Enable HTTPS** (automatic with Render)
5. **Monitor API usage** and set up alerts

### **Firestore Security Rules:**
Apply the rules from `firestore-security-rules.txt` in your Firebase Console before production use.

## Scaling Considerations

### **Render Free Tier:**
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid plan for always-on service

### **Upgrade Options:**
- **Starter Plan**: $7/month - Always on, better performance
- **Standard Plan**: $25/month - More resources, better scaling

## Troubleshooting

### **Common Deployment Issues:**

1. **Import Errors**: Check Python version compatibility
2. **Firebase Connection**: Verify credentials and project settings
3. **CORS Errors**: Update `ALLOWED_ORIGINS` environment variable
4. **Build Timeouts**: Optimize `requirements.txt` dependencies

### **Debug Commands:**
```bash
# Test locally with production settings
ENVIRONMENT=production python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Next Steps After Deployment

1. **Test all endpoints** with your deployed URL
2. **Configure your frontend** to use the new API URL
3. **Set up monitoring** and alerts
4. **Apply Firestore security rules**
5. **Plan for scaling** as your user base grows

Your LinkWorkJA backend will be production-ready! 🚀
