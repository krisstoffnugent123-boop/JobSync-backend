# Firestore Security Rules Setup

## How to Apply Security Rules

### Step 1: Access Firebase Console
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `jobsync-backend`
3. Go to "Firestore Database" in the left sidebar
4. Click on "Rules" tab

### Step 2: Apply Security Rules
Copy the rules from `firestore-security-rules.txt` and paste them into the rules editor.

### Step 3: Test Rules
1. Click "Publish" to apply the rules
2. Test with your API endpoints to ensure they work correctly

## Rule Explanations

### Users Collection (`/users/{userId}`)
- **Read/Write**: Users can only access their own data
- **Create**: Any authenticated user can create a profile

### Jobs Collection (`/jobs/{jobId}`)
- **Read**: All authenticated users can read job listings
- **Create**: Any authenticated user can create jobs
- **Update/Delete**: Only job owners or admins can modify jobs

### Micro Gigs Collection (`/micro_gigs/{gigId}`)
- **Read**: All authenticated users can read available gigs
- **Create**: Any authenticated user can create gigs
- **Update/Delete**: Only gig owners or admins can modify gigs

### Applications Collection (`/applications/{applicationId}`)
- **Read/Write**: Users can only access applications they created or received
- **Create**: Any authenticated user can create applications

### Analytics Collection (`/analytics/{document}`)
- **Read**: All authenticated users can read analytics
- **Write**: Only admins can write analytics data

## Testing Your Rules

### Test 1: User Registration
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'
```

### Test 2: Get Jobs
```bash
curl -X GET "http://localhost:8000/jobs/"
```

### Test 3: Get Gigs
```bash
curl -X GET "http://localhost:8000/gigs/available"
```

## Production Considerations

### Before Going Live:
1. **Enable Authentication**: Set up proper user authentication
2. **Admin Roles**: Implement admin role checking
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Data Validation**: Ensure all data is properly validated
5. **Backup Strategy**: Set up automated backups

### Monitoring:
1. **Firebase Console**: Monitor usage and errors
2. **Logs**: Check Firebase logs for security violations
3. **Analytics**: Track API usage and performance

## Troubleshooting

### Common Issues:
1. **Permission Denied**: Check if user is authenticated
2. **Rules Not Applied**: Ensure rules are published
3. **Token Issues**: Verify JWT tokens are valid

### Debug Mode:
Temporarily set rules to allow all access for testing:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**Remember to change back to secure rules before production!**
