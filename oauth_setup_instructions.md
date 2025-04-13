# Google OAuth Setup Instructions for SnowNavi Admin

This document explains how to set up Google OAuth to secure the course_admin.html page so that only authorized users (specifically okboy2008@gmail.com) can access it.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "OAuth consent screen"
4. Select "External" user type and click "Create"
5. Fill in the required information:
   - App name: "SnowNavi Admin"
   - User support email: Your email
   - Developer contact information: Your email
6. Click "Save and Continue"
7. Skip adding scopes and click "Save and Continue"
8. Add your test user email (okboy2008@gmail.com) and click "Save and Continue"
9. Review your settings and click "Back to Dashboard"

## Step 2: Create OAuth Credentials

1. Navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Web application" as the application type
4. Name: "SnowNavi Admin Web Client"
5. Add Authorized JavaScript origins:
   - Add your website's domain (e.g., https://snownavi.ski)
   - For local testing, add http://localhost and http://127.0.0.1
6. Add Authorized redirect URIs:
   - Add your callback URL (e.g., https://snownavi.ski/auth_callback.html)
   - For local testing, add http://localhost/auth_callback.html and http://127.0.0.1/auth_callback.html
7. Click "Create"
8. Note your Client ID and Client Secret (you'll need the Client ID)

## Step 3: Update the Login Page

1. Open the `login.html` file
2. Replace `YOUR_GOOGLE_CLIENT_ID` with the actual Client ID you obtained in Step 2
3. Make sure the `REDIRECT_URI` matches one of the authorized redirect URIs you configured

```javascript
// Your Google OAuth client ID
const CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID_HERE';
const REDIRECT_URI = window.location.origin + '/auth_callback.html';
```

## Step 4: Testing the Authentication

1. Upload all files to your web server:
   - login.html
   - auth_callback.html
   - course_admin.html
2. Navigate to login.html
3. Click "Sign in with Google"
4. You should be redirected to Google's authentication page
5. After signing in, you should be redirected back to course_admin.html if you used okboy2008@gmail.com
6. If you use a different email, you should see an "Access denied" message

## Security Considerations

- This implementation uses the OAuth 2.0 Implicit Flow, which is suitable for client-side applications
- Authentication state is stored in localStorage, which means it will persist until explicitly cleared or expired
- The access token expires after 1 hour, after which the user will need to log in again
- Only the email okboy2008@gmail.com is authorized to access the admin page
- For production use, consider implementing additional security measures such as:
  - Server-side validation of tokens
  - HTTPS for all communications
  - Regular rotation of OAuth credentials

## Troubleshooting

- If you see "Authentication failed. No access token found" error, check that your redirect URI is correctly configured
- If you see "Authentication error" messages, check the browser console for more details
- If you're testing locally, make sure you've added localhost to your authorized JavaScript origins and redirect URIs
