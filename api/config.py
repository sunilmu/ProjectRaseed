import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_CONFIG = {
    "google_cloud_api_key": os.getenv('GOOGLE_CLOUD_API_KEY'),
    "google_cloud_project": os.getenv('GOOGLE_CLOUD_PROJECT', 'project-raseed-467107'),
    "service_account_path": os.getenv('GOOGLE_APPLICATION_CREDENTIALS', r"C:\Users\sunil.t\Downloads\receiptwise-sowbs-firebase-adminsdk-fbsvc-00e76e04db.json")
}

# Check if required configuration is available
def check_config():
    missing_configs = []
    
    if not API_CONFIG["google_cloud_api_key"]:
        missing_configs.append("GOOGLE_CLOUD_API_KEY")
    
    if not os.path.exists(API_CONFIG["service_account_path"]):
        missing_configs.append("GOOGLE_APPLICATION_CREDENTIALS (file not found)")
    
    if missing_configs:
        print("⚠️ Missing configuration:")
        for config in missing_configs:
            print(f"   - {config}")
        print("\n📝 To fix this:")
        print("   1. Set GOOGLE_CLOUD_API_KEY environment variable")
        print("   2. Ensure service account file exists")
        return False
    
    return True 