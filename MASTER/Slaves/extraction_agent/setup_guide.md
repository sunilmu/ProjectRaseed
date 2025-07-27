# Google Wallet API Setup Guide

## Prerequisites
1. Google Cloud Project
2. Google Wallet API enabled
3. Service Account with proper permissions

## Step 1: Enable Google Wallet API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to "APIs & Services" > "Library"
4. Search for "Google Wallet API"
5. Click "Enable"

## Step 2: Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: `wallet-issuer`
4. Description: `Service account for Google Wallet passes`
5. Click "Create and Continue"

## Step 3: Assign Permissions
1. Add these roles to your service account:
   - `Wallet Object Issuer`
   - `Service Account Token Creator`
2. Click "Done"

## Step 4: Create and Download Key
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON"
5. Download the JSON file
6. Place it in your project directory

## Step 5: Update Configuration
Update the service account file path in `createpass.py`:

```python
self.service_account_file = "path/to/your/service-account.json"
```

## Step 6: Set Environment Variables
Create a `.env` file in your project root:

```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
WALLET_ISSUER_ID=your_issuer_id
```

## Step 7: Get Your Issuer ID
1. Go to [Google Wallet Console](https://pay.google.com/business/console/)
2. Sign in with your Google account
3. Note your Issuer ID (found in the URL or settings)

## Step 8: Test the Setup
1. Run your agent
2. Create a sample receipt
3. Try to create a Google Wallet pass
4. Check if the URL works and adds to your wallet

## Troubleshooting

### "Invalid grant: account not found"
- Check if service account JSON is valid
- Ensure the service account has proper permissions
- Verify the Google Wallet API is enabled

### "Service account file not found"
- Check the file path in your code
- Ensure the JSON file exists in the specified location

### "Permission denied"
- Add the `Wallet Object Issuer` role to your service account
- Make sure you're using the correct project

## File Structure
```
MASTER/Slaves/extraction_agent/
├── createpass.py
├── agent.py
├── extract.py
├── receipts/
└── service-account.json  # Your downloaded key
```

## Testing
1. Create a sample receipt: "Create a sample receipt"
2. Create wallet pass: "Create wallet pass from receipt ID: [id]"
3. Click the generated URL to add to your Google Wallet 