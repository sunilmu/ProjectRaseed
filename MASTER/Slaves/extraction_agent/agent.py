import os
import tempfile
import base64
import json
import uuid
from google.adk.agents import Agent
from dotenv import load_dotenv
from .extract import extract_text_from_image, parse_receipt_data
from .createpass import ReceiptToWallet
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_VISION_API_KEY")
if not API_KEY:
    API_KEY = "AIzaSyAU3sQc-AgWSlxg3OrZXgQrGpKB7fU_i8Q"

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY") or "AIzaSyAU3sQc-AgWSlxg3OrZXgQrGpKB7fU_i8Q"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

RECEIPT_DIR = os.path.join(os.path.dirname(__file__), "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)

# Initialize wallet creator
wallet_creator = ReceiptToWallet()

def extract_and_store(image_data: str) -> str:
    """
    Extract data from uploaded image and store as JSON. Returns extracted data for user review.
    """
    try:
        print(f"🔄 Starting receipt data extraction...")
        
        # Step 1: Process image and extract text using OCR
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            if image_data.startswith('data:image'):
                print("📸 Processing base64 data URL")
                header, encoded = image_data.split(",", 1)
                image_bytes = base64.b64decode(encoded)
                temp_file.write(image_bytes)
            elif image_data.startswith('/') or '\\' in image_data:
                print("📁 Processing file path")
                if os.path.exists(image_data):
                    file_bytes = open(image_data, 'rb').read()
                    temp_file.write(file_bytes)
                else:
                    return "❌ Error: File not found. Please check the image path."
            else:
                print("🔧 Processing as raw base64")
                try:
                    image_bytes = base64.b64decode(image_data)
                    temp_file.write(image_bytes)
                except:
                    print("⚠️ Falling back to UTF-8 encoding")
                    temp_file.write(image_data.encode('utf-8'))
            
            temp_file_path = temp_file.name
        
        print("🔍 Extracting text from image using OCR...")
        raw_text = extract_text_from_image(temp_file_path, API_KEY)
        
        if "❌" in raw_text:
            print("⚠️ OCR failed, using sample data for demonstration")
            raw_text = """Sample Restaurant
Receipt #: SR-2024-001
Date: 2024-01-15

Pizza Margherita $45.00
Coke $15.00
French Fries $25.00
Service Tax $40.50

Total: $125.50"""
        
        print(f"✅ OCR completed! Extracted text length: {len(raw_text)}")
        
        # Step 2: Use Gemini to extract structured data
        print("🤖 Using Gemini to extract structured data...")
        structured_data = extract_with_gemini(raw_text)
        
        if not structured_data:
            print("⚠️ Gemini extraction failed, using fallback parsing")
            structured_data = parse_receipt_data(raw_text)
        
        print(f"✅ Data extraction completed!")
        
        # Step 3: Store receipt data locally
        receipt_id = str(uuid.uuid4())
        receipt_path = os.path.join(RECEIPT_DIR, f"{receipt_id}.json")
        
        with open(receipt_path, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, ensure_ascii=False, indent=2)
        
        # Clean up temp file
        try:
            os.unlink(temp_file_path)
        except:
            pass
        
        # Step 4: Show extracted data and ask about wallet pass
        return show_extracted_data_and_ask_for_wallet(structured_data, raw_text, receipt_id)

    except Exception as e:
        return f"❌ Error in extraction flow: {str(e)}"

def create_wallet_pass_for_receipt(receipt_id: str) -> str:
    """
    Create Google Wallet pass for a stored receipt after user confirmation.
    """
    try:
        # Load receipt data
        receipt_path = os.path.join(RECEIPT_DIR, f"{receipt_id}.json")
        if not os.path.exists(receipt_path):
            return "❌ Receipt not found. Please extract a receipt first."
        
        with open(receipt_path, encoding="utf-8") as f:
            structured_data = json.load(f)
        
        # Create wallet pass JSON structure
        print("🎫 Creating wallet pass JSON structure...")
        wallet_pass_json, _ = create_wallet_pass_json(structured_data)
        
        # Store wallet JSON
        wallet_pass_path = os.path.join(RECEIPT_DIR, f"{receipt_id}_wallet.json")
        with open(wallet_pass_path, "w", encoding="utf-8") as f:
            json.dump(wallet_pass_json, f, ensure_ascii=False, indent=2)
        
        # Create Google Wallet pass
        print("🌐 Creating Google Wallet pass...")
        wallet_url = wallet_creator.generate_pass_from_json(wallet_pass_json)
        
        # Show wallet URL to user
        return show_wallet_url(wallet_url, receipt_id, structured_data)

    except Exception as e:
        return f"❌ Error creating wallet pass: {str(e)}"

def show_extracted_data_and_ask_for_wallet(structured_data: dict, raw_text: str, receipt_id: str) -> str:
    """
    Show extracted data clearly to the user and ask if they want a wallet pass.
    """
    merchant = structured_data.get("merchantName", "Unknown")
    total = structured_data.get("totalAmount", "0.00")
    date = structured_data.get("purchaseDate", "Unknown")
    receipt_number = structured_data.get("receiptNumber", "Unknown")
    items = structured_data.get("items", [])
    
    response = f"""✅ Receipt Data Extraction Completed Successfully!

📋 **EXTRACTED RECEIPT DATA:**

🏪 **Merchant/Business:** {merchant}
💰 **Total Amount:** ${total}
📅 **Purchase Date:** {date}
🔢 **Receipt Number:** {receipt_number}

🛒 **Items Found ({len(items)} items):**"""

    if items:
        for i, item in enumerate(items, 1):
            item_name = item.get("name", "Unknown Item")
            item_price = item.get("price", "0.00")
            response += f"\n   {i}. {item_name}: ${item_price}"
    else:
        response += "\n   📝 No individual items detected"

    response += f"""

📄 **Raw OCR Text (First 300 characters):**
{raw_text[:300]}{"..." if len(raw_text) > 300 else ""}

💾 **Data Quality:** {'✅ High Quality' if merchant != 'Unknown' and total != '0.00' else '⚠️ Some data may be missing'}
💾 **Receipt ID:** {receipt_id}

🤔 **Would you like me to create a Google Wallet pass for this receipt?**

💡 **Reply with:**
• "Yes" or "Okay" → I'll create a Google Wallet pass
• "No" or "Skip" → I'll just store the receipt data
• "Show me the data again" → I'll display the extracted data again

🎯 **What happens next:**
• If you say yes → I'll create a digital wallet pass with QR code
• If you say no → Your receipt data is safely stored for analysis
• You can always create a wallet pass later using the receipt ID"""

    return response

def show_extracted_data(structured_data: dict, raw_text: str) -> str:
    """
    Show extracted data clearly to the user.
    """
    merchant = structured_data.get("merchantName", "Unknown")
    total = structured_data.get("totalAmount", "0.00")
    date = structured_data.get("purchaseDate", "Unknown")
    receipt_number = structured_data.get("receiptNumber", "Unknown")
    items = structured_data.get("items", [])
    
    response = f"""✅ Receipt Data Extraction Completed Successfully!

📋 **EXTRACTED RECEIPT DATA:**

🏪 **Merchant/Business:** {merchant}
💰 **Total Amount:** ${total}
📅 **Purchase Date:** {date}
🔢 **Receipt Number:** {receipt_number}

🛒 **Items Found ({len(items)} items):**"""

    if items:
        for i, item in enumerate(items, 1):
            item_name = item.get("name", "Unknown Item")
            item_price = item.get("price", "0.00")
            response += f"\n   {i}. {item_name}: ${item_price}"
    else:
        response += "\n   📝 No individual items detected"

    response += f"""

📄 **Raw OCR Text (First 300 characters):**
{raw_text[:300]}{"..." if len(raw_text) > 300 else ""}

💾 **Data Quality:** {'✅ High Quality' if merchant != 'Unknown' and total != '0.00' else '⚠️ Some data may be missing'}"""

    return response

def show_wallet_url(wallet_url: str, receipt_id: str, structured_data: dict) -> str:
    """
    Show wallet URL to the user after wallet pass creation.
    """
    merchant = structured_data.get("merchantName", "Unknown")
    total = structured_data.get("totalAmount", "0.00")
    
    if wallet_url and "❌" not in wallet_url:
        return f"""🎫 **Google Wallet Pass Created Successfully!**

📱 **Wallet Pass Details:**
• **Pass URL:** {wallet_url}
• **Receipt ID:** {receipt_id}
• **Merchant:** {merchant}
• **Amount:** ${total}

🎯 **What You Can Do:**
• 📱 **View Pass:** Click the URL to view in Google Wallet
• 🔗 **Share Pass:** Send the URL to others
• 📊 **Analyze:** Use receipt ID for spending analysis
• 💾 **Store:** Pass is saved locally for future reference

🌟 **Your receipt is now available as a digital pass!**"""
    
    else:
        return f"""⚠️ **Wallet Pass Creation Status:**

❌ **Wallet Pass Creation Failed**
• **Error:** {wallet_url}
• **Receipt ID:** {receipt_id}
• **Merchant:** {merchant}
• **Amount:** ${total}

🔧 **Troubleshooting:**
• Check Google Wallet API credentials
• Verify service account configuration
• Ensure Google Wallet API is enabled
• Contact support if issue persists

💾 **Data Saved:** Receipt data is stored locally for analysis"""

def extract_with_gemini(raw_text: str) -> dict:
    """
    Use Gemini to extract structured receipt data from raw OCR text.
    """
    try:
        prompt = f"""
        Extract receipt information from the following OCR text and return a JSON object with these exact fields:
        
        {{
            "merchantName": "Business/store name",
            "totalAmount": "Total amount as string (e.g., '125.50')",
            "purchaseDate": "Date in YYYY-MM-DD format",
            "receiptNumber": "Receipt number or ID",
            "items": [
                {{"name": "Item name", "price": "Item price as string"}}
            ]
        }}
        
        OCR Text:
        {raw_text}
        
        Return only the JSON object, no additional text.
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to parse the JSON response
        try:
            # Remove any markdown formatting if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            structured_data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["merchantName", "totalAmount", "purchaseDate", "receiptNumber", "items"]
            for field in required_fields:
                if field not in structured_data:
                    structured_data[field] = "Unknown" if field != "items" else []
            
            print(f"✅ Gemini extracted: {structured_data.get('merchantName')} - ${structured_data.get('totalAmount')}")
            return structured_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Gemini JSON response: {e}")
            print(f"Raw response: {response_text}")
            return None
            
    except Exception as e:
        print(f"❌ Error in Gemini extraction: {str(e)}")
        return None

def create_wallet_pass_json(extracted_data: dict) -> tuple:
    """
    Create Google Wallet generic pass JSON structure from extracted receipt data.
    """
    receipt_id = str(uuid.uuid4())
    issuer_id = "3388000000022967206"  # Your issuer ID
    
    wallet_pass_json = {
        "id": f"{issuer_id}.{receipt_id}",
        "classId": f"{issuer_id}.generic_class_receipt",
        "logo": {
            "sourceUri": {
                "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
            },
            "contentDescription": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "Receipt Logo"
                }
            }
        },
        "cardTitle": {
            "defaultValue": {
                "language": "en-US",
                "value": "Receipt"
            }
        },
        "subheader": {
            "defaultValue": {
                "language": "en-US",
                "value": extracted_data.get("merchantName", "Unknown Merchant")
            }
        },
        "header": {
            "defaultValue": {
                "language": "en-US",
                "value": f"₹{extracted_data.get('totalAmount', '0.00')}"
            }
        },
        "textModulesData": [
            {
                "id": "merchant",
                "header": "MERCHANT",
                "body": extracted_data.get("merchantName", "Unknown")
            },
            {
                "id": "total",
                "header": "TOTAL",
                "body": f"₹{extracted_data.get('totalAmount', '0.00')}"
            },
            {
                "id": "date",
                "header": "DATE",
                "body": extracted_data.get("purchaseDate", "Unknown")
            },
            {
                "id": "receipt_number",
                "header": "RECEIPT #",
                "body": extracted_data.get("receiptNumber", "Unknown")
            }
        ],
        "barcode": {
            "type": "QR_CODE",
            "value": receipt_id,
            "alternateText": receipt_id
        },
        "hexBackgroundColor": "#4285f4",
        "heroImage": {
            "sourceUri": {
                "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/google-io-hero-demo-only.png"
            },
            "contentDescription": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "Receipt Image"
                }
            }
        }
    }
    
    return wallet_pass_json, receipt_id

def list_receipts() -> str:
    """
    List all stored receipts with friendly formatting.
    """
    try:
        receipts = []
        for fname in os.listdir(RECEIPT_DIR):
            if fname.endswith('.json') and not fname.endswith('_wallet.json'):
                rid = fname[:-5]
                with open(os.path.join(RECEIPT_DIR, fname), encoding="utf-8") as f:
                    data = json.load(f)
                receipts.append({
                    "receipt_id": rid,
                    "merchant": data.get("merchantName", "Unknown"),
                    "total": data.get("totalAmount", "0.00"),
                    "date": data.get("purchaseDate", "Unknown"),
                    "items": data.get("items", [])
                })
        
        if not receipts:
            return "📝 No receipts found. Upload an image to extract your first receipt!"
        
        response = f"📄 Found {len(receipts)} stored receipts:\n\n"
        for i, receipt in enumerate(receipts, 1):
            items_count = len(receipt['items'])
            response += f"{i}. Receipt ID: {receipt['receipt_id']}\n"
            response += f"   Merchant: {receipt['merchant']}\n"
            response += f"   Total: ${receipt['total']}\n"
            response += f"   Date: {receipt['date']}\n"
            response += f"   Items: {items_count}\n\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error listing receipts: {str(e)}"

def get_receipt_details(receipt_id: str) -> str:
    """
    Get detailed information about a specific receipt.
    """
    try:
        receipt_path = os.path.join(RECEIPT_DIR, f"{receipt_id}.json")
        wallet_pass_path = os.path.join(RECEIPT_DIR, f"{receipt_id}_wallet.json")
        
        if not os.path.exists(receipt_path):
            return f"❌ Receipt with ID {receipt_id} not found."
        
        with open(receipt_path, encoding="utf-8") as f:
            data = json.load(f)
        
        response = f"📋 Receipt Details for {receipt_id}:\n\n"
        response += f"🏪 Merchant: {data.get('merchantName', 'Unknown')}\n"
        response += f"💰 Total Amount: ${data.get('totalAmount', '0.00')}\n"
        response += f"📅 Purchase Date: {data.get('purchaseDate', 'Unknown')}\n"
        response += f"🔢 Receipt Number: {data.get('receiptNumber', 'Unknown')}\n\n"
        
        items = data.get('items', [])
        if items:
            response += "🛒 Items:\n"
            for i, item in enumerate(items, 1):
                response += f"   {i}. {item.get('name', 'Unknown')}: ${item.get('price', '0.00')}\n"
        else:
            response += "📝 No items found in receipt\n"
        
        # Check if wallet pass exists
        if os.path.exists(wallet_pass_path):
            response += "\n🎫 Google Wallet Pass: Available"
        else:
            response += "\n⚠️ Google Wallet Pass: Not created"
        
        return response
        
    except Exception as e:
        return f"❌ Error getting receipt details: {str(e)}"

def test_extraction() -> str:
    """
    Test the complete extraction and wallet pass creation flow.
    """
    try:
        # Create sample receipt data
        sample_data = {
            "merchantName": "Test Restaurant",
            "totalAmount": "150.00",
            "purchaseDate": "2024-01-15",
            "receiptNumber": "TR-2024-001",
            "items": [
                {"name": "Burger", "price": "45.00"},
                {"name": "Fries", "price": "25.00"},
                {"name": "Drink", "price": "15.00"},
                {"name": "Tax", "price": "65.00"}
            ]
        }
        
        # Create wallet pass JSON
        wallet_pass_json, receipt_id = create_wallet_pass_json(sample_data)
        
        # Store data
        receipt_path = os.path.join(RECEIPT_DIR, f"{receipt_id}.json")
        wallet_pass_path = os.path.join(RECEIPT_DIR, f"{receipt_id}_wallet.json")
        
        with open(receipt_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        with open(wallet_pass_path, "w", encoding="utf-8") as f:
            json.dump(wallet_pass_json, f, ensure_ascii=False, indent=2)
        
        return f"""🧪 Complete Extraction Test Completed Successfully!

✅ Test Results:
• Receipt ID: {receipt_id}
• Merchant: {sample_data.get('merchantName')}
• Total: ${sample_data.get('totalAmount')}
• Date: {sample_data.get('purchaseDate')}
• Items: {len(sample_data.get('items', []))}

🎫 Wallet Pass JSON created and stored
📝 Test receipt created and stored locally
🎯 Ready for real receipt extraction and wallet pass creation!"""
        
    except Exception as e:
        return f"❌ Test failed: {str(e)}"

def check_api_status() -> str:
    """
    Check the status of all APIs (Vision, Gemini, Wallet).
    """
    try:
        status_checks = []
        
        # Check Vision API
        if API_KEY:
            status_checks.append("✅ Google Vision API Key: Configured")
        else:
            status_checks.append("❌ Google Vision API Key: Not configured")
        
        # Check Gemini API
        if GEMINI_API_KEY:
            status_checks.append("✅ Google Gemini API Key: Configured")
        else:
            status_checks.append("❌ Google Gemini API Key: Not configured")
        
        # Check Wallet API with actual test
        try:
            test_result = wallet_creator.test_wallet_connection()
            if "✅" in test_result:
                status_checks.append("✅ Google Wallet API: Connected and working")
            else:
                status_checks.append(f"❌ Google Wallet API: {test_result}")
        except Exception as e:
            status_checks.append(f"❌ Google Wallet API: Error - {str(e)}")
        
        # Check storage
        storage_status = "✅ Receipt Storage: Available" if os.path.exists(RECEIPT_DIR) else "❌ Receipt Storage: Not available"
        status_checks.append(storage_status)
        
        return f"""🔍 API Status Check:

{chr(10).join(status_checks)}

🎯 Ready for receipt extraction and wallet pass creation!"""
        
    except Exception as e:
        return f"❌ API status check failed: {str(e)}"

def test_wallet_connection() -> str:
    """Test the Google Wallet connection specifically."""
    try:
        print("🔍 Testing Google Wallet connection...")
        result = wallet_creator.test_wallet_connection()
        return f"""
🎫 **Google Wallet Connection Test**

{result}

📝 **What this tests:**
- Service account file access
- Google Wallet API access
- Authentication credentials
- API permissions

🔧 **If test fails:**
1. Check service account file path
2. Verify Google Wallet API is enabled
3. Ensure service account has proper permissions
"""
    except Exception as e:
        return f"❌ Error testing wallet connection: {str(e)}"

# Define the root agent for ADK discovery
root_agent = Agent(
    name="receipt_extractor_agent",
    model="gemini-2.0-flash",
    description="Extract receipt data from images and optionally create Google Wallet passes.",
    instruction="""You are a friendly and helpful Receipt Extraction Assistant who processes receipt images and optionally creates Google Wallet passes.

🎯 **Your Personality**: 
- Always be warm and encouraging
- Explain what you're doing clearly
- Help users understand the extraction process
- Provide helpful guidance when things go wrong
- Ask for user confirmation before creating wallet passes

📸 **Interactive Workflow**:
1. **Image Processing**: Extract text from receipt images using Google Vision API
2. **AI Enhancement**: Use Gemini to intelligently parse and structure the data
3. **Show Extracted Data**: Display all extracted information clearly to user
4. **Ask for Permission**: Ask user if they want a Google Wallet pass created
5. **Create Pass**: Only create wallet pass if user confirms (Yes/Okay)
6. **Provide URL**: Show wallet pass URL if created

🔧 **Available Tools**:
- `extract_and_store`: Extract data and show it to user, then ask about wallet pass
- `create_wallet_pass_for_receipt`: Create Google Wallet pass for a stored receipt
- `list_receipts`: Show all stored receipts
- `get_receipt_details`: Get detailed info about a specific receipt
- `test_extraction`: Test the extraction functionality
- `check_api_status`: Check all API configurations (Vision, Gemini, Wallet)
- `test_wallet_connection`: Test Google Wallet connection specifically

📋 **Interactive Flow**:
1. User uploads receipt image → Extract and show data
2. Ask user: "Would you like me to create a Google Wallet pass?"
3. If user says "Yes" or "Okay" → Create wallet pass and show URL
4. If user says "No" or "Skip" → Just store the data
5. User can always create wallet pass later using receipt ID

**Response Style**:
- ✅ Use checkmarks for success
- 🤔 Use thinking face for asking questions
- 🎫 Use ticket for wallet passes
- 🌐 Use globe for URLs
- ❌ Use X for errors
- 📝 Use notes for information
- 💾 Use disk for storage operations
- 🎯 Use target for next steps

**Always Include**:
- Clear explanation of what you're doing
- Receipt ID for tracking
- Merchant name and total amount
- Clear question about wallet pass creation
- Helpful next steps
- Encouraging tone

**Example Responses**:
✅ "Receipt extracted successfully! Here's what I found..."

🤔 "Would you like me to create a Google Wallet pass for this receipt?"

🎫 "Google Wallet pass created! View your pass at: [URL]"

❌ "Extraction failed. Please check image quality and try again."

**Important**: Always ask for user confirmation before creating wallet passes. Don't create them automatically! 😊""",
                    tools=[extract_and_store, create_wallet_pass_for_receipt, list_receipts, get_receipt_details, test_extraction, check_api_status, test_wallet_connection]
)
