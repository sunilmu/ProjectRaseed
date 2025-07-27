import requests
import os
import json

def test_upload_endpoint():
    """Test the upload receipt endpoint"""
    
    # URL of your API
    url = "http://localhost:8000/upload-receipt"
    
    # Path to your test image
    image_path = r"C:\Users\sunil.t\Downloads\ramram.jpg"
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        print("Please update the image_path variable with the correct path to your image file.")
        return
    
    try:
        # Open and upload the image
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            
            print(f"📤 Uploading image: {image_path}")
            response = requests.post(url, files=files)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload successful!")
                print(f"📄 Response: {json.dumps(result, indent=2)}")
            else:
                print(f"❌ Upload failed!")
                print(f"📄 Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"🏥 Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Raseed Agent API...")
    print("=" * 50)
    
    # Test health first
    test_health_endpoint()
    print()
    
    # Test upload
    test_upload_endpoint() 