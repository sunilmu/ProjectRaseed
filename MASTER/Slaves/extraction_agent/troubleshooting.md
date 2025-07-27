# Google Wallet API Troubleshooting Guide

## Error: "invalid_grant: Invalid grant: account not found"

This error occurs when the service account exists but doesn't have proper access to the Google Wallet API.

## Step-by-Step Fix

### 1. Enable Google Wallet API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: **project-raseed-467107**
3. Go to "APIs & Services" > "Library"
4. Search for "Google Wallet API"
5. Click on "Google Wallet API"
6. Click "Enable"

### 2. Verify Service Account Permissions
1. Go to "IAM & Admin" > "Service Accounts"
2. Find your service account (the one in your JSON file)
3. Click on it
4. Go to "Permissions" tab
5. Click "Grant Access"
6. Add these roles:
   - `Wallet Object Issuer`
   - `Service Account Token Creator`
   - `Wallet Object Admin` (if available)

### 3. Check Project Configuration
1. Go to [Google Wallet Console](https://pay.google.com/business/console/)
2. Sign in with your Google account
3. Make sure you're in the correct project: **project-raseed-467107**
4. Note your Issuer ID (should be: 3388000000022967206)

### 4. Verify Service Account JSON
1. Open your JSON file: `C:\Users\sunil.t\Downloads\project-raseed-467107-56cc27af6f23.json`
2. Check these fields:
   ```json
   {
     "project_id": "project-raseed-467107",
     "client_email": "your-service-account@project-raseed-467107.iam.gserviceaccount.com",
     "private_key_id": "...",
     "private_key": "..."
   }
   ```

### 5. Test API Access
Run this test in your agent:
- Say: "Test Google Wallet credentials"
- Check the detailed response

### 6. Common Issues and Solutions

#### Issue: "API not enabled"
**Solution**: Enable Google Wallet API in project-raseed-467107

#### Issue: "Service account not found"
**Solution**: 
1. Check if the service account exists in project-raseed-467107
2. Verify the JSON file is from the correct project
3. Recreate the service account if needed

#### Issue: "Insufficient permissions"
**Solution**:
1. Add `Wallet Object Issuer` role
2. Add `Service Account Token Creator` role
3. Make sure the service account is active

#### Issue: "Wrong project"
**Solution**:
1. Verify you're using project ID: **project-raseed-467107**
2. Check if the service account belongs to the right project
3. Update the issuer ID if needed

## Quick Test Commands

1. **Test credentials**: "Test Google Wallet credentials"
2. **Create sample**: "Create a sample receipt"
3. **Create pass**: "Create wallet pass from receipt ID: [id]"

## Expected Success Flow

1. ✅ Service account file found
2. ✅ Credentials loaded successfully
3. ✅ API connection successful
4. ✅ Class created successfully
5. ✅ Object created successfully
6. ✅ Wallet pass URL generated

## If Still Failing

1. **Check the console logs** for detailed error messages
2. **Verify the project ID** in your JSON file matches **project-raseed-467107**
3. **Recreate the service account** with fresh credentials
4. **Contact Google Support** if the issue persists

## Alternative Solution

If the API issues persist, you can:
1. Use a different Google Cloud project
2. Create a new service account with fresh permissions
3. Use a different Google account for the Wallet Console 