# Frontend Integration Guide for LinkWorkJA Backend

## 🚀 Quick Start

Your backend is **ready for frontend integration**! Here's everything you need to know:

### ✅ **Backend Status**
- **Server**: Running on `http://localhost:8000`
- **API Documentation**: Available at `http://localhost:8000/docs`
- **CORS**: Configured for `http://localhost:3000` and `http://localhost:3001`
- **Health Check**: `http://localhost:8000/health`

## 🔗 **API Base Configuration**

### For React/Next.js
```javascript
// config/api.js
export const API_BASE_URL = 'http://localhost:8000';

// Example API client
export const apiClient = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};
```

### For Vue.js
```javascript
// config/api.js
export const API_BASE_URL = 'http://localhost:8000';

// Axios configuration
import axios from 'axios';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## 📋 **Available API Endpoints**

### 🔐 **Authentication** (`/auth/`)
```javascript
// User Registration
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "parish": "Kingston",
  "role": "job_seeker", // or "business" or "government"
  "skills": ["Python", "JavaScript"]
}

// User Login
POST /auth/login
{
  "username": "user@example.com", // Note: uses 'username' field
  "password": "password123"
}

// Get Current User (requires token)
GET /auth/me
Headers: { "Authorization": "Bearer <token>" }
```

### 💼 **Jobs** (`/jobs/`)
```javascript
// Get all jobs (public)
GET /jobs/

// Get jobs with filters
GET /jobs/?parish=Kingston&min_pay=50000&skills=Python

// Create job (requires auth)
POST /jobs/
Headers: { "Authorization": "Bearer <token>" }
{
  "title": "Software Developer",
  "description": "Full-stack development role",
  "company": "Tech Corp",
  "location": "Kingston",
  "parish": "Kingston",
  "salary_min": 50000,
  "salary_max": 80000,
  "required_skills": ["Python", "React"],
  "job_type": "full_time"
}

// Get job by ID
GET /jobs/{job_id}

// Apply for job (requires auth)
POST /jobs/{job_id}/apply
Headers: { "Authorization": "Bearer <token>" }
```

### 🎯 **Gigs** (`/gigs/`)
```javascript
// Get available gigs
GET /gigs/available

// Get gigs by parish
GET /gigs/available?parish=Kingston

// Create gig (requires auth)
POST /gigs/
Headers: { "Authorization": "Bearer <token>" }
{
  "title": "Website Design",
  "description": "Design a company website",
  "location": "Kingston",
  "parish": "Kingston",
  "budget": 5000,
  "duration_days": 7,
  "required_skills": ["Design", "HTML", "CSS"]
}

// Claim gig (requires auth)
POST /gigs/{gig_id}/claim
Headers: { "Authorization": "Bearer <token>" }

// Complete gig (requires auth)
POST /gigs/complete
Headers: { "Authorization": "Bearer <token>" }
{
  "gig_id": "gig123",
  "completion_notes": "Project completed successfully"
}
```

### 🤝 **Matching** (`/matching/`)
```javascript
// Get job matches for user (requires auth)
GET /matching/jobs
Headers: { "Authorization": "Bearer <token>" }

// Get gig matches for user (requires auth)
GET /matching/gigs
Headers: { "Authorization": "Bearer <token>" }

// Get AI-powered recommendations (requires auth)
GET /matching/recommendations
Headers: { "Authorization": "Bearer <token>" }
```

### 📊 **Analytics** (`/analytics/`)
```javascript
// Get dashboard data (requires auth)
GET /analytics/dashboard
Headers: { "Authorization": "Bearer <token>" }

// Get user statistics (requires auth)
GET /analytics/user-stats
Headers: { "Authorization": "Bearer <token>" }
```

## 🔧 **Frontend Integration Examples**

### **React/Next.js Example**
```javascript
// hooks/useAuth.js
import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        return data;
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const register = async (userData) => {
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });
      
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  return { user, token, login, register };
};
```

### **Vue.js Example**
```javascript
// composables/useApi.js
import { ref } from 'vue';
import axios from 'axios';

export const useApi = () => {
  const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Add token to requests
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  const getJobs = async (filters = {}) => {
    try {
      const response = await api.get('/jobs/', { params: filters });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
      return [];
    }
  };

  const getGigs = async (parish = null) => {
    try {
      const params = parish ? { parish } : {};
      const response = await api.get('/gigs/available', { params });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch gigs:', error);
      return [];
    }
  };

  return { getJobs, getGigs };
};
```

## 🛠️ **Development Mode Features**

### **Current Status**
- ✅ **Basic endpoints working**: Root, health, docs
- ✅ **CORS configured**: Ready for frontend on localhost:3000
- ✅ **API documentation**: Available at `/docs`
- ⚠️ **Authentication**: Some endpoints may need Firebase setup
- ⚠️ **Database operations**: Running in development mode (mocked)

### **Development Mode Indicators**
When the backend runs in development mode, you'll see:
```
⚠️ Firebase credentials not found. Running in development mode without Firebase.
🔧 DEV MODE: Would create user with data: {...}
```

This means:
- Database operations are logged but not persisted
- Authentication works with mock data
- All endpoints are accessible for testing

## 🚨 **Troubleshooting**

### **Common Issues**

1. **CORS Errors**
   - Ensure your frontend is running on `localhost:3000` or `localhost:3001`
   - Check that the backend is running on `localhost:8000`

2. **Authentication Errors**
   - Make sure to include the `Authorization: Bearer <token>` header
   - Check that the token is valid and not expired

3. **Connection Refused**
   - Verify the backend server is running: `curl http://localhost:8000/health`
   - Check the port is not being used by another process

### **Testing Your Integration**

```bash
# Test basic connectivity
curl http://localhost:8000/

# Test CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:8000/

# Test API documentation
open http://localhost:8000/docs
```

## 📚 **Next Steps**

1. **Start with basic endpoints**: Test `/`, `/health`, `/docs`
2. **Implement authentication**: Register/login flow
3. **Add protected endpoints**: Jobs, gigs, matching
4. **Handle errors**: Implement proper error handling
5. **Add loading states**: Show loading indicators for API calls

## 🔗 **Useful Links**

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Backend Setup Guide**: See `SETUP.md` in the backend directory

Your backend is ready for frontend integration! 🎉

