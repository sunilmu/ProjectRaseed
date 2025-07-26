# import os
# import base64
# import json
# import re
# import requests
# from dotenv import load_dotenv
# from datetime import datetime

# # Load the API key from .env
# load_dotenv()
# API_KEY = os.getenv("GOOGLE_CLOUD_VISION_API_KEY")

# def extract_text_from_image(image_path):
#     """Use Google Vision API to perform OCR on an image."""
#     with open(image_path, "rb") as image_file:
#         content = base64.b64encode(image_file.read()).decode("utf-8")

#     endpoint_url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
#     payload = {
#         "requests": [
#             {
#                 "image": {"content": content},
#                 "features": [{"type": "TEXT_DETECTION"}]
#             }
#         ]
#     }

#     response = requests.post(endpoint_url, json=payload)
#     if response.status_code != 200 or "error" in response.json():
#         print("Error:", response.json())
#         return ""

#     annotations = response.json()["responses"][0]
#     return annotations.get("fullTextAnnotation", {}).get("text", "")

# def extract_fields(text):
#     """Extract structured fields from OCR text."""
#     fields = {
#         "Company Name": "",
#         "Address": "",
#         "Date": "",
#         "Time": "",
#         "Category": "",
#         "Cost": "",
#         "GST": "",
#         "Discount": ""
#     }

#     # Example regex patterns (can be customized)
#     lines = text.splitlines()

#     # Company Name: usually in the first line
#     fields["Company Name"] = lines[0] if lines else ""

#     # Address: look for typical address patterns
#     for line in lines:
#         if any(word in line.lower() for word in ["road", "street", "avenue", "block", "area", "city", "pincode"]):
#             fields["Address"] = line
#             break

#     # Date and Time
#     date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", text)
#     time_match = re.search(r"(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)", text)

#     if date_match:
#         fields["Date"] = date_match.group(1)
#     if time_match:
#         fields["Time"] = time_match.group(1)

#     # Category (example: electronics, food, clothing)
#     category_match = re.search(r"(electronics|food|grocery|clothing|stationery)", text, re.IGNORECASE)
#     if category_match:
#         fields["Category"] = category_match.group(1).capitalize()

#     # Cost / Amount
#     cost_match = re.search(r"(Total\s*[:\-]?\s*\₹?\s*\d+\.?\d*)", text, re.IGNORECASE)
#     if cost_match:
#         fields["Cost"] = cost_match.group(1)

#     # GST
#     gst_match = re.search(r"(GST\s*[:\-]?\s*\₹?\s*\d+\.?\d*)", text, re.IGNORECASE)
#     if gst_match:
#         fields["GST"] = gst_match.group(1)

#     # Discount
#     discount_match = re.search(r"(Discount\s*[:\-]?\s*\₹?\s*\d+\.?\d*)", text, re.IGNORECASE)
#     if discount_match:
#         fields["Discount"] = discount_match.group(1)

#     return fields

# def save_output(text, fields, output_file):
#     """Save OCR output and extracted fields to text file."""
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("===== Extracted OCR Text =====\n")
#         f.write(text + "\n\n")
#         f.write("===== Extracted Fields =====\n")
#         for key, value in fields.items():
#             f.write(f"{key}: {value}\n")

# if __name__ == "__main__":
#     image_path = r"C:\Users\sunil.t\Downloads\ramram.jpg"
#     output_path = r"C:\Users\sunil.t\Downloads\ocr_output.txt"

#     print("[🔍] Performing OCR...")
#     ocr_text = extract_text_from_image(image_path)

#     if ocr_text:
#         print("[✅] Extracting fields...")
#         extracted_fields = extract_fields(ocr_text)

#         print("[💾] Saving to file...")
#         save_output(ocr_text, extracted_fields, output_path)

#         print(f"[✅] Done. Output saved to:\n{output_path}")
#     else:
#         print("[❌] Failed to extract text from image.")
###########################################above code is working##########################
#########################################below is the open source###########################
# from google.adk.agents import Agent
# from dotenv import load_dotenv
# from .extract import extract_receipt_data
# import os

# load_dotenv()
# IamExtractorAgent = Agent(
#     name="extraction_agent",
#     model="gemini-2.0-flash",
#     description="Agent for extracting data from receipts",
#     instruction="""
#     You are a friendly and helpful agent that extracts data from receipt images.

#     - Do NOT show the raw code or function call to the user.
#     - Use the `extract_receipt_data` function behind the scenes to process the image and extract:
#       business_name, receipt_number, date, total, and items.
#     - Then, summarize the extracted data in a clean, user-friendly format.
#     - Show only:
#         • Restaurant name
#         • Address (if found in text)
#         • Date
#         • Items (name + price)
#         • Total
#         • Payment method (if mentioned)
#         • GST/VAT (if mentioned)
#     - Always greet the user warmly and offer to help further.
#     """
# )
#####################################extract and pass creation ############
# from google.adk.agents import Agent
# from google.oauth2 import service_account
# from google.auth.transport.requests import AuthorizedSession
# from dotenv import load_dotenv
# from .extract import extract_receipt_data  # Make sure this import path is correct
# import os
# from datetime import datetime
# import json
# import uuid

# load_dotenv()

# # Offline storage configuration
# STORAGE_DIR = "receipt_data"
# os.makedirs(STORAGE_DIR, exist_ok=True)

# class WalletPassService:
#     """Handles Google Wallet pass creation"""
#     def __init__(self):
#         self.issuer_id = os.getenv("WALLET_ISSUER_ID")
#         self.client = AuthorizedSession(
#             service_account.Credentials.from_service_account_file(
#                 os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
#                 scopes=["https://www.googleapis.com/auth/wallet_object.issuer"]
#             )
#         )
    
#     def create_loyalty_pass(self, business_name: str, receipt_number: str, total: str, date: str = None) -> str:
#         """Creates a loyalty pass with receipt data"""
#         try:
#             # Format date if provided
#             formatted_date = datetime.strptime(date, "%d/%m/%Y").isoformat() + "Z" if date else None
            
#             class_id = f"{self.issuer_id}.{business_name.lower().replace(' ', '_')}_class"
#             object_id = f"{self.issuer_id}.{receipt_number}"
            
#             # Create pass class
#             self.client.put(
#                 f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass/{class_id}",
#                 json={
#                     "id": class_id,
#                     "issuerName": business_name,
#                     "reviewStatus": "UNDER_REVIEW",
#                     "programName": f"{business_name} Rewards",
#                     "programLogo": {
#                         "sourceUri": {
#                             "uri": "https://example.com/logo.png"  # Replace with your logo
#                         }
#                     }
#                 }
#             )
            
#             # Create pass object
#             pass_payload = {
#                 "id": object_id,
#                 "classId": class_id,
#                 "state": "ACTIVE",
#                 "barcode": {
#                     "type": "QR_CODE",
#                     "value": receipt_number
#                 },
#                 "accountId": receipt_number[-4:],  # Last 4 digits as account ID
#                 "loyaltyPoints": {
#                     "label": "Points",
#                     "balance": {
#                         "int": str(int(float(total)))
#                     }
#                 }
#             }
            
#             if formatted_date:
#                 pass_payload["validTimeInterval"] = {
#                     "start": {"date": formatted_date}
#                 }
            
#             response = self.client.put(
#                 f"https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject/{object_id}",
#                 json=pass_payload
#             )
            
#             return f"https://pay.google.com/gp/v/save/{response.json()['id']}"
            
#         except Exception as e:
#             raise Exception(f"Wallet API Error: {str(e)}")

# def parse_agent_output(text):
#     """Parse agent's textual output into a structured dict."""
#     data = {}
#     lines = text.strip().split('\n')
#     for line in lines:
#         if ":" in line:
#             key, value = line.split(":", 1)
#             key, value = key.strip(), value.strip()
#             if key.lower() == "items":
#                 data["Items"] = {}
#                 continue
#             data[key] = value
#         elif line.strip() and "Items" in data:
#             try:
#                 item_name, price = line.rsplit(":", 1)
#                 data["Items"][item_name.strip()] = float(price.strip())
#             except Exception:
#                 pass
#     return data

# def save_to_offline_storage(data):
#     """Save the parsed receipt data to a JSON file offline."""
#     try:
#         # Generate a unique filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         unique_id = str(uuid.uuid4())[:8]
#         filename = f"receipt_{timestamp}_{unique_id}.json"
#         filepath = os.path.join(STORAGE_DIR, filename)
        
#         # Save data as JSON
#         with open(filepath, 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)
        
#         return filename
#     except Exception as e:
#         raise Exception(f"Storage error: {str(e)}")

# class ReceiptToWalletAgent(Agent):
#     def run(self, input_data):
#         try:
#             # Step 1: Extract receipt data
#             extracted_data = extract_receipt_data(input_data)
#             print("🛠️ EXTRACTED DATA:", extracted_data)
            
#             # Step 2: Parse and save offline
#             parsed_data = parse_agent_output(extracted_data)
#             save_to_offline_storage(parsed_data)
            
#             # Step 3: Create wallet pass
#             wallet_url = create_wallet_pass(
#                 business_name=parsed_data.get("Restaurant name", "Unknown Business"),
#                 receipt_number=parsed_data.get("Receipt number", str(uuid.uuid4())[:8]),
#                 total=parsed_data.get("Total", "0"),
#                 date=parsed_data.get("Date")
#             )
            
#             # Step 4: Format response
#             return (
#                 f"🏢 {parsed_data.get('Restaurant name', 'Unknown Business')}\n"
#                 f"📅 {parsed_data.get('Date', 'Unknown date')}\n"
#                 f"🧾 Receipt# {parsed_data.get('Receipt number', 'N/A')}\n"
#                 f"💵 Total: {parsed_data.get('Total', '0')}\n"
#                 f"✅ Wallet Pass: {wallet_url}"
#             )
#         except Exception as e:
#             return f"❌ Error processing receipt: {str(e)}"

# def create_wallet_pass(business_name: str, receipt_number: str, total: str, date: str = None) -> str:
#     """Function that ADK will call to create passes"""
#     try:
#         return WalletPassService().create_loyalty_pass(
#             business_name=business_name,
#             receipt_number=receipt_number,
#             total=total,
#             date=date
#         )
#     except Exception as e:
#         raise Exception(f"Pass creation failed: {str(e)}")

# # ADK-compatible agent
# root_agent = ReceiptToWalletAgent(
#     name="receipt_to_wallet_agent",
#     model="gemini-2.0-flash",
#     description="Creates Google Wallet passes from receipt data",
#     instruction="""
#     You are a complete receipt processing system that:
#     1. Extracts data from receipts using extract_receipt_data()
#     2. Saves the data offline in JSON format
#     3. Creates Google Wallet loyalty passes
#     4. Returns a formatted response with pass URL
    
#     Required receipt fields:
#     - Business name
#     - Receipt number
#     - Total amount
#     - Date (optional)
    
#     Always return the formatted response even if some fields are missing.
#     Handle errors gracefully without technical details.
#     """
# )
#########################################################################33
import uuid
import logging
from dotenv import load_dotenv
from google.adk.agents import Agent
 

from createpass import ReceiptToWallet 

load_dotenv()



# Root agent instance
root_agent = ReceiptToWalletAgent(
    name="receipt_to_wallet_agent",
    model="gemini-2.0-flash",
    description="Creates Google Wallet generic passes from receipt images",
    instruction="""
     .
    """
)
