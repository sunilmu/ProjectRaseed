# import uuid
# import requests
# import json
# import logging
# import time

# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# from google.auth import jwt

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # === CONFIGURATION ===
# SERVICE_ACCOUNT_FILE = r"C:\Users\sunil.t\Downloads\raseed-466712-ace42483d1e8.json"  # Replace with your actual path
# WALLET_ISSUER_ID = "3388000000022967206"
# CLASS_ID = f"{WALLET_ISSUER_ID}.raseed_loyalty_class"
# ORIGIN_URL = "http://localhost"  # Since you're running locally

# # === FUNCTIONS ===

# def get_credentials():
#     """Obtain OAuth2 credentials for Google Wallet API."""
#     try:
#         credentials = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE,
#             scopes=["https://www.googleapis.com/auth/wallet_object.issuer"]
#         )
#         credentials.refresh(Request())
#         return credentials
#     except Exception as e:
#         logger.error(f"Failed to obtain credentials: {str(e)}")
#         raise

# def create_or_verify_class(credentials):
#     """Create or verify the existence of a Generic Class."""
#     headers = {
#         "Authorization": f"Bearer {credentials.token}",
#         "Content-Type": "application/json; charset=UTF-8"
#     }

#     class_payload = {
#         "id": CLASS_ID,
#         "issuerName": "Raseed AI",
#         "reviewStatus": "DRAFT",
#         "hexBackgroundColor": "#4285f4",
#         "title": "Raseed Wallet Pass",
#         "cardTitle": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": "Raseed Receipt"
#             }
#         },
#         "allowBarcodeRedemption": True
#     }

#     logger.info("Checking if class exists...")
#     class_url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass/{CLASS_ID}"
#     class_response = requests.get(class_url, headers=headers)

#     if class_response.status_code == 404:
#         logger.info("Class not found. Creating class...")
#         response = requests.post(
#             "https://walletobjects.googleapis.com/walletobjects/v1/genericClass",
#             headers=headers,
#             json=class_payload
#         )
#         if response.status_code != 200:
#             logger.error(f"Class creation failed: {response.text}")
#             raise Exception(f"Class creation failed: {response.text}")
#         logger.info("Class created successfully.")
#     elif class_response.status_code == 200:
#         logger.info("Class already exists.")
#     else:
#         logger.error(f"Unexpected response when checking class: {class_response.text}")
#         raise Exception(f"Class check failed: {class_response.text}")

# def create_generic_object(credentials, user_id):
#     """Create a Generic Object for the pass."""
#     headers = {
#         "Authorization": f"Bearer {credentials.token}",
#         "Content-Type": "application/json; charset=UTF-8"
#     }

#     object_id = f"{WALLET_ISSUER_ID}.{user_id}"
#     object_payload = {
#         "id": object_id,
#         "classId": CLASS_ID,
#         "header": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": "Raseed Receipt"
#             }
#         },
#         "cardTitle": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": "Raseed Receipt"
#             }
#         },
#         "textModulesData": [
#             {
#                 "header": "Merchant",
#                 "body": "HEN AND CHICKEN"
#             },
#             {
#                 "header": "Total",
#                 "body": "$10.50"
#             },
#             {
#                 "header": "Date",
#                 "body": "17/11/2018 13:37"
#             }
#         ],
#         "barcode": {
#             "type": "QR_CODE",
#             "value": f"Raseed-{user_id}",
#             "alternateText": "Scan to view"
#         },
#         "state": "ACTIVE"
#     }

#     logger.info("Creating generic object...")
#     object_response = requests.post(
#         "https://walletobjects.googleapis.com/walletobjects/v1/genericObject",
#         headers=headers,
#         json=object_payload
#     )

#     if object_response.status_code not in (200, 201):
#         logger.error(f"Object creation failed: {object_response.text}")
#         raise Exception(f"Object creation failed: {object_response.text}")
    
#     logger.info("Generic object created successfully.")
#     return object_id

# def generate_save_url(credentials, object_id):
#     """Generate a JWT for the Save to Google Wallet link."""
#     iat = int(time.time())
#     claims = {
#         "iss": credentials.service_account_email,
#         "aud": "google",
#         "typ": "savetowallet",
#         "iat": iat,
#         "exp": iat + 3600,
#         "origin": ORIGIN_URL,
#         "payload": {
#             "genericObjects": [
#                 {"id": object_id}
#             ]
#         }
#     }

#     try:
#         signed_jwt = jwt.encode(credentials.signer, claims).decode("utf-8")  # FIXED here
#         logger.info(f"Generated JWT successfully.")
#         save_url = f"https://pay.google.com/gp/v/save/{signed_jwt}"
#         return save_url
#     except Exception as e:
#         logger.error(f"Failed to generate JWT: {str(e)}")
#         raise

# # === MAIN EXECUTION ===

# def main():
#     try:
#         user_id = str(uuid.uuid4())[:10]  # Short UUID
#         credentials = get_credentials()
#         create_or_verify_class(credentials)
#         object_id = create_generic_object(credentials, user_id)
#         save_url = generate_save_url(credentials, object_id)

#         logger.info("\n=== Save to Google Wallet URL ===")
#         logger.info(save_url)
#         return save_url

#     except Exception as e:
#         logger.error(f"Error in main execution: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()
#####################################################
# import uuid
# import requests
# import json
# import logging
# import time
# import pytesseract
# import cv2
# import re
# import os
# from datetime import datetime
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# from google.auth import jwt

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # === CONFIGURATION ===
# SERVICE_ACCOUNT_FILE = r"C:\Users\sunil.t\Downloads\raseed-466712-ace42483d1e8.json"
# WALLET_ISSUER_ID = "3388000000022967206"
# CLASS_ID = f"{WALLET_ISSUER_ID}.raseed_loyalty_class"
# ORIGIN_URL = "http://localhost"
# TESSERACT_PATH = r"C:\Users\sunil.t\Desktop\OCR\tesseract.exe"
# TESSDATA_PREFIX = r"C:\Users\sunil.t\Desktop\OCR\tessdata"
# IMAGE_PATH = r"C:\Users\sunil.t\Downloads\ramram.jpg"  # Hardcoded image path

# # Configure Tesseract
# pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
# os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX

# # === RECEIPT PROCESSING FUNCTIONS ===

# def extract_receipt_data(image_path):
#     """Extract receipt data from image using OCR."""
#     try:
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError("Could not load image")

#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#         text = pytesseract.image_to_string(gray)

#         receipt_data = {
#             "business_name": None,
#             "receipt_number": None,
#             "date": None,
#             "total": None,
#             "items": []
#         }

#         date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s\w+\s\d{2,4})\b'
#         total_pattern = r'(?:Total|TOTAL|Amount Due)\s*[:$]?\s*(\d+\.?\d*)'
#         receipt_num_pattern = r'(?:Receipt|Transaction|Order)\s*[#No:]+?\s*(\d+|[A-Z0-9-]+)'

#         lines = text.split('\n')
#         receipt_data["business_name"] = lines[0].strip() if lines else None

#         receipt_num_match = re.search(receipt_num_pattern, text, re.IGNORECASE)
#         if receipt_num_match:
#             receipt_data["receipt_number"] = receipt_num_match.group(1)

#         date_str = None
#         date_match = re.search(date_pattern, text)
#         if date_match:
#             try:
#                 date_str = date_match.group(0)
#                 parsed_date = datetime.strptime(date_str, '%d/%m/%Y') if '/' in date_str else datetime.strptime(date_str, '%d-%m-%Y')
#                 receipt_data["date"] = parsed_date.strftime('%d/%m/%Y %H:%M')
#             except ValueError:
#                 try:
#                     parsed_date = datetime.strptime(date_str, '%d %B %Y')
#                     receipt_data["date"] = parsed_date.strftime('%d/%m/%Y %H:%M')
#                 except ValueError:
#                     receipt_data["date"] = date_str
#         else:
#             date_str = None

#         total_match = re.search(total_pattern, text, re.IGNORECASE)
#         if total_match:
#             receipt_data["total"] = float(total_match.group(1))

#         item_pattern = r'(.+?)\s+(\d+\.?\d*)'
#         for line in lines:
#             item_match = re.search(item_pattern, line)
#             if item_match:
#                 item_name = item_match.group(1).strip()
#                 item_price = float(item_match.group(2))
#                 receipt_data["items"].append({"name": item_name, "price": item_price})

#         return receipt_data

#     except Exception as e:
#         logger.error(f"Error extracting receipt data: {str(e)}")
#         raise

# # === GOOGLE WALLET FUNCTIONS ===

# def get_credentials():
#     """Obtain OAuth2 credentials for Google Wallet API."""
#     try:
#         credentials = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE,
#             scopes=["https://www.googleapis.com/auth/wallet_object.issuer"]
#         )
#         credentials.refresh(Request())
#         return credentials
#     except Exception as e:
#         logger.error(f"Failed to obtain credentials: {str(e)}")
#         raise

# def create_or_verify_class(credentials):
#     """Create or verify the existence of a Generic Class."""
#     headers = {
#         "Authorization": f"Bearer {credentials.token}",
#         "Content-Type": "application/json; charset=UTF-8"
#     }

#     class_payload = {
#         "id": CLASS_ID,
#         "issuerName": "Raseed AI",
#         "reviewStatus": "DRAFT",
#         "hexBackgroundColor": "#4285f4",
#         "title": "Raseed Wallet Pass",
#         "cardTitle": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": "Raseed Receipt"
#             }
#         },
#         "allowBarcodeRedemption": True
#     }

#     logger.info("Checking if class exists...")
#     class_url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass/{CLASS_ID}"
#     class_response = requests.get(class_url, headers=headers)

#     if class_response.status_code == 404:
#         logger.info("Class not found. Creating class...")
#         response = requests.post(
#             "https://walletobjects.googleapis.com/walletobjects/v1/genericClass",
#             headers=headers,
#             json=class_payload
#         )
#         if response.status_code != 200:
#             logger.error(f"Class creation failed: {response.text}")
#             raise Exception(f"Class creation failed: {response.text}")
#         logger.info("Class created successfully.")
#     elif class_response.status_code == 200:
#         logger.info("Class already exists.")
#     else:
#         logger.error(f"Unexpected response when checking class: {class_response.text}")
#         raise Exception(f"Class check failed: {class_response.text}")

# def create_generic_object(credentials, user_id, receipt_data):
#     """Create a Generic Object for the pass using extracted receipt data."""
#     headers = {
#         "Authorization": f"Bearer {credentials.token}",
#         "Content-Type": "application/json; charset=UTF-8"
#     }

#     object_id = f"{WALLET_ISSUER_ID}.{user_id}"
    
#     # Format items for display with better handling
#     items_text = "\n".join([f"{item.get('name', 'Item')}: ${item.get('price', 0):.2f}" 
#                           for item in receipt_data.get('items', [])])
    
#     # Handle missing total amount
#     total_amount = receipt_data.get('total')
#     if total_amount is None:
#         # Try to calculate from items if total is missing
#         total_amount = sum(item.get('price', 0) for item in receipt_data.get('items', []))
#         total_text = f"${total_amount:.2f} (calculated)" if total_amount > 0 else "Not available"
#     else:
#         total_text = f"${float(total_amount):.2f}"
    
#     # Handle missing business name
#     business_name = receipt_data.get('business_name', 'Unknown Merchant')
#     if business_name.isdigit():  # If OCR extracted just numbers as name
#         business_name = "Unknown Merchant"
    
#     # Handle date formatting
#     receipt_date = receipt_data.get('date', 'Unknown Date')
#     if isinstance(receipt_date, str) and len(receipt_date) > 20:  # If date is too long
#         receipt_date = "Unknown Date"
    
#     object_payload = {
#         "id": object_id,
#         "classId": CLASS_ID,
#         "header": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": business_name
#             }
#         },
#         "cardTitle": {
#             "defaultValue": {
#                 "language": "en-US",
#                 "value": "Raseed Receipt"
#             }
#         },
#         "textModulesData": [
#             {
#                 "header": "Merchant",
#                 "body": business_name
#             },
#             {
#                 "header": "Total",
#                 "body": total_text
#             },
#             {
#                 "header": "Date",
#                 "body": receipt_date
#             },
#             {
#                 "header": "Items",
#                 "body": items_text if items_text else "No items listed"
#             }
#         ],
#         "barcode": {
#             "type": "QR_CODE",
#             "value": f"Raseed-{user_id}",
#             "alternateText": "Scan to view"
#         },
#         "state": "ACTIVE"
#     }

#     logger.info("Creating generic object with payload: %s", json.dumps(object_payload, indent=2))
#     object_response = requests.post(
#         "https://walletobjects.googleapis.com/walletobjects/v1/genericObject",
#         headers=headers,
#         json=object_payload
#     )

#     if object_response.status_code not in (200, 201):
#         logger.error(f"Object creation failed: {object_response.text}")
#         raise Exception(f"Object creation failed: {object_response.text}")
    
#     logger.info("Generic object created successfully.")
#     return object_id
# def generate_save_url(credentials, object_id):
#     """Generate a JWT for the Save to Google Wallet link."""
#     iat = int(time.time())
#     claims = {
#         "iss": credentials.service_account_email,
#         "aud": "google",
#         "typ": "savetowallet",
#         "iat": iat,
#         "exp": iat + 3600,
#         "origin": ORIGIN_URL,
#         "payload": {
#             "genericObjects": [
#                 {"id": object_id}
#             ]
#         }
#     }

#     try:
#         signed_jwt = jwt.encode(credentials.signer, claims).decode("utf-8")
#         logger.info(f"Generated JWT successfully.")
#         save_url = f"https://pay.google.com/gp/v/save/{signed_jwt}"
#         return save_url
#     except Exception as e:
#         logger.error(f"Failed to generate JWT: {str(e)}")
#         raise

# # === MAIN EXECUTION ===

# def main():
#     try:
#         # Extract receipt data
#         logger.info(f"Processing receipt image: {IMAGE_PATH}")
#         receipt_data = extract_receipt_data(IMAGE_PATH)
#         logger.info(f"Extracted receipt data: {json.dumps(receipt_data, indent=2)}")
        
#         # Generate Google Wallet pass
#         user_id = str(uuid.uuid4())[:10]  # Short UUID
#         credentials = get_credentials()
#         create_or_verify_class(credentials)
#         object_id = create_generic_object(credentials, user_id, receipt_data)
#         save_url = generate_save_url(credentials, object_id)

#         logger.info("\n=== Save to Google Wallet URL ===")
#         logger.info(save_url)
#         return save_url

#     except Exception as e:
#         logger.error(f"Error in main execution: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()
############################################################################
# receipt_wallet.py
import uuid
import requests
import json
import logging
import time
import pytesseract
import cv2
import re
import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.auth import jwt

class ReceiptToWallet:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.SERVICE_ACCOUNT_FILE = r"C:\Users\sunil.t\Downloads\raseed-466712-ace42483d1e8.json"
        self.WALLET_ISSUER_ID = "3388000000022967206"
        self.CLASS_ID = f"{self.WALLET_ISSUER_ID}.raseed_loyalty_class"
        self.ORIGIN_URL = "http://localhost"
        self.TESSERACT_PATH = r"C:\Users\sunil.t\Desktop\OCR\tesseract.exe"
        self.TESSDATA_PREFIX = r"C:\Users\sunil.t\Desktop\OCR\tessdata"

        # Configure Tesseract
        pytesseract.pytesseract.tesseract_cmd = self.TESSERACT_PATH
        os.environ["TESSDATA_PREFIX"] = self.TESSDATA_PREFIX

    def extract_receipt_data(self, image_path):
        """Extract receipt data from image using OCR."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            text = pytesseract.image_to_string(gray)

            receipt_data = {
                "business_name": None,
                "receipt_number": None,
                "date": None,
                "total": None,
                "items": []
            }

            date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s\w+\s\d{2,4})\b'
            total_pattern = r'(?:Total|TOTAL|Amount Due)\s*[:$]?\s*(\d+\.?\d*)'
            receipt_num_pattern = r'(?:Receipt|Transaction|Order)\s*[#No:]+?\s*(\d+|[A-Z0-9-]+)'

            lines = text.split('\n')
            receipt_data["business_name"] = lines[0].strip() if lines else None

            receipt_num_match = re.search(receipt_num_pattern, text, re.IGNORECASE)
            if receipt_num_match:
                receipt_data["receipt_number"] = receipt_num_match.group(1)

            date_str = None
            date_match = re.search(date_pattern, text)
            if date_match:
                try:
                    date_str = date_match.group(0)
                    parsed_date = datetime.strptime(date_str, '%d/%m/%Y') if '/' in date_str else datetime.strptime(date_str, '%d-%m-%Y')
                    receipt_data["date"] = parsed_date.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    try:
                        parsed_date = datetime.strptime(date_str, '%d %B %Y')
                        receipt_data["date"] = parsed_date.strftime('%d/%m/%Y %H:%M')
                    except ValueError:
                        receipt_data["date"] = date_str
            else:
                date_str = None

            total_match = re.search(total_pattern, text, re.IGNORECASE)
            if total_match:
                receipt_data["total"] = float(total_match.group(1))

            item_pattern = r'(.+?)\s+(\d+\.?\d*)'
            for line in lines:
                item_match = re.search(item_pattern, line)
                if item_match:
                    item_name = item_match.group(1).strip()
                    item_price = float(item_match.group(2))
                    receipt_data["items"].append({"name": item_name, "price": item_price})

            return receipt_data

        except Exception as e:
            self.logger.error(f"Error extracting receipt data: {str(e)}")
            raise

    def get_credentials(self):
        """Obtain OAuth2 credentials for Google Wallet API."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/wallet_object.issuer"]
            )
            credentials.refresh(Request())
            return credentials
        except Exception as e:
            self.logger.error(f"Failed to obtain credentials: {str(e)}")
            raise

    def create_or_verify_class(self, credentials):
        """Create or verify the existence of a Generic Class."""
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        class_payload = {
            "id": self.CLASS_ID,
            "issuerName": "Raseed AI",
            "reviewStatus": "DRAFT",
            "hexBackgroundColor": "#4285f4",
            "title": "Raseed Wallet Pass",
            "cardTitle": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "Raseed Receipt"
                }
            },
            "allowBarcodeRedemption": True
        }

        self.logger.info("Checking if class exists...")
        class_url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass/{self.CLASS_ID}"
        class_response = requests.get(class_url, headers=headers)

        if class_response.status_code == 404:
            self.logger.info("Class not found. Creating class...")
            response = requests.post(
                "https://walletobjects.googleapis.com/walletobjects/v1/genericClass",
                headers=headers,
                json=class_payload
            )
            if response.status_code != 200:
                self.logger.error(f"Class creation failed: {response.text}")
                raise Exception(f"Class creation failed: {response.text}")
            self.logger.info("Class created successfully.")
        elif class_response.status_code == 200:
            self.logger.info("Class already exists.")
        else:
            self.logger.error(f"Unexpected response when checking class: {class_response.text}")
            raise Exception(f"Class check failed: {class_response.text}")

    def create_generic_object(self, credentials, user_id, receipt_data):
        """Create a Generic Object for the pass using extracted receipt data."""
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        object_id = f"{self.WALLET_ISSUER_ID}.{user_id}"
        
        # Format items for display with better handling
        items_text = "\n".join([f"{item.get('name', 'Item')}: ${item.get('price', 0):.2f}" 
                              for item in receipt_data.get('items', [])])
        
        # Handle missing total amount
        total_amount = receipt_data.get('total')
        if total_amount is None:
            # Try to calculate from items if total is missing
            total_amount = sum(item.get('price', 0) for item in receipt_data.get('items', []))
            total_text = f"${total_amount:.2f} (calculated)" if total_amount > 0 else "Not available"
        else:
            total_text = f"${float(total_amount):.2f}"
        
        # Handle missing business name
        business_name = receipt_data.get('business_name', 'Unknown Merchant')
        if business_name.isdigit():  # If OCR extracted just numbers as name
            business_name = "Unknown Merchant"
        
        # Handle date formatting
        receipt_date = receipt_data.get('date', 'Unknown Date')
        if isinstance(receipt_date, str) and len(receipt_date) > 20:  # If date is too long
            receipt_date = "Unknown Date"
        
        object_payload = {
            "id": object_id,
            "classId": self.CLASS_ID,
            "header": {
                "defaultValue": {
                    "language": "en-US",
                    "value": business_name
                }
            },
            "cardTitle": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "Raseed Receipt"
                }
            },
            "textModulesData": [
                {
                    "header": "Merchant",
                    "body": business_name
                },
                {
                    "header": "Total",
                    "body": total_text
                },
                {
                    "header": "Date",
                    "body": receipt_date
                },
                {
                    "header": "Items",
                    "body": items_text if items_text else "No items listed"
                }
            ],
            "barcode": {
                "type": "QR_CODE",
                "value": f"Raseed-{user_id}",
                "alternateText": "Scan to view"
            },
            "state": "ACTIVE"
        }

        self.logger.info("Creating generic object with payload: %s", json.dumps(object_payload, indent=2))
        object_response = requests.post(
            "https://walletobjects.googleapis.com/walletobjects/v1/genericObject",
            headers=headers,
            json=object_payload
        )

        if object_response.status_code not in (200, 201):
            self.logger.error(f"Object creation failed: {object_response.text}")
            raise Exception(f"Object creation failed: {object_response.text}")
        
        self.logger.info("Generic object created successfully.")
        return object_id

    def generate_save_url(self, credentials, object_id):
        """Generate a JWT for the Save to Google Wallet link."""
        iat = int(time.time())
        claims = {
            "iss": credentials.service_account_email,
            "aud": "google",
            "typ": "savetowallet",
            "iat": iat,
            "exp": iat + 3600,
            "origin": self.ORIGIN_URL,
            "payload": {
                "genericObjects": [
                    {"id": object_id}
                ]
            }
        }

        try:
            signed_jwt = jwt.encode(credentials.signer, claims).decode("utf-8")
            self.logger.info(f"Generated JWT successfully.")
            save_url = f"https://pay.google.com/gp/v/save/{signed_jwt}"
            return save_url
        except Exception as e:
            self.logger.error(f"Failed to generate JWT: {str(e)}")
            raise

    def create_wallet_pass(self, image_path):
        """Main method to create wallet pass from receipt image."""
        try:
            # Extract receipt data
            self.logger.info(f"Processing receipt image: {image_path}")
            receipt_data = self.extract_receipt_data(image_path)
            self.logger.info(f"Extracted receipt data: {json.dumps(receipt_data, indent=2)}")
            
            # Generate Google Wallet pass
            user_id = str(uuid.uuid4())[:10]  # Short UUID
            credentials = self.get_credentials()
            self.create_or_verify_class(credentials)
            object_id = self.create_generic_object(credentials, user_id, receipt_data)
            save_url = self.generate_save_url(credentials, object_id)

            self.logger.info("\n=== Save to Google Wallet URL ===")
            self.logger.info(save_url)
            return {
                "status": "success",
                "wallet_url": save_url,
                "receipt_data": receipt_data
            }

        except Exception as e:
            self.logger.error(f"Error in wallet pass creation: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }