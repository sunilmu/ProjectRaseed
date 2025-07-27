import uuid
import requests
import json
import logging
import time
import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.auth import jwt

class ReceiptToWallet:
    def __init__(self, service_account_file=None, wallet_issuer_id=None, origin_url=None):
        self.logger = logging.getLogger(__name__)
        
        # Configuration - Use provided parameters or environment variables
        self.SERVICE_ACCOUNT_FILE = service_account_file or os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", 
                                            r"C:\Users\sunil.t\Downloads\raseed-466712-ace42483d1e8.json")
        self.WALLET_ISSUER_ID = wallet_issuer_id or os.getenv("WALLET_ISSUER_ID", "3388000000022967206")
        self.CLASS_ID = f"{self.WALLET_ISSUER_ID}.raseed_loyalty_class"
        self.ORIGIN_URL = origin_url or os.getenv("ORIGIN_URL", "http://localhost")
        
        # Validate critical paths
        if not os.path.exists(self.SERVICE_ACCOUNT_FILE):
            self.logger.error(f"Service account file not found at {self.SERVICE_ACCOUNT_FILE}")
            raise FileNotFoundError(f"Service account file not found at {self.SERVICE_ACCOUNT_FILE}")

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
            self.logger.error(f"Authentication failed: {str(e)}")
            raise

    def create_or_verify_class(self, credentials):
        """Create or verify the existence of a Generic Class."""
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        class_url = f"https://walletobjects.googleapis.com/walletobjects/v1/genericClass/{self.CLASS_ID}"
        
        try:
            # Check if class exists
            response = requests.get(class_url, headers=headers)
            if response.status_code == 200:
                self.logger.info("Wallet class already exists")
                return
            
            # Create new class if not exists
            class_payload = {
                "id": self.CLASS_ID,
                "issuerName": "Raseed AI",
                "reviewStatus": "UNDER_REVIEW",
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

            response = requests.post(
                "https://walletobjects.googleapis.com/walletobjects/v1/genericClass",
                headers=headers,
                json=class_payload
            )
            response.raise_for_status()
            self.logger.info("Successfully created wallet class")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Class operation failed: {str(e)}")
            raise

    def create_generic_object(self, credentials, user_id, receipt_data):
        """Create a Generic Object for the pass."""
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        object_id = f"{self.WALLET_ISSUER_ID}.{user_id}"
        
        # Format display data with fallbacks
        business_name = receipt_data.get('merchantName', receipt_data.get('business_name', 'Unknown Merchant'))
        if not business_name or business_name.isdigit():
            business_name = "Unknown Merchant"
            
        total_amount = receipt_data.get('totalAmount', receipt_data.get('total'))
        if total_amount is None:
            total_amount = sum(item.get('price', 0) for item in receipt_data.get('items', []))
            total_text = f"${total_amount:.2f} (calculated)" if total_amount > 0 else "Not available"
        else:
            try:
                total_text = f"${float(total_amount):.2f}"
            except (ValueError, TypeError):
                total_text = "Not available"
        
        items_text = "\n".join(
            f"{item.get('name', 'Item')}: ${item.get('price', 0):.2f}" 
            for item in receipt_data.get('items', [])
        ) or "No items listed"

        receipt_date = receipt_data.get('purchaseDate', receipt_data.get('date', 'Unknown Date'))
        if isinstance(receipt_date, str) and len(receipt_date) > 30:
            receipt_date = "Unknown Date"

        object_payload = {
            "id": object_id,
            "classId": self.CLASS_ID,
            "state": "ACTIVE",
            "header": {
                "defaultValue": {
                    "language": "en-US",
                    "value": business_name
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
                    "body": items_text
                }
            ],
            "barcode": {
                "type": "QR_CODE",
                "value": f"Raseed-{user_id}",
                "alternateText": "Scan to view"
            }
        }

        try:
            response = requests.post(
                "https://walletobjects.googleapis.com/walletobjects/v1/genericObject",
                headers=headers,
                json=object_payload
            )
            
            # Debug: Log response details
            self.logger.info(f"Object creation response status: {response.status_code}")
            self.logger.info(f"Object creation response: {response.text}")
            
            response.raise_for_status()
            self.logger.info("Successfully created wallet object")
            
            # Verify object was created by trying to get it
            verify_response = requests.get(
                f"https://walletobjects.googleapis.com/walletobjects/v1/genericObject/{object_id}",
                headers=headers
            )
            if verify_response.status_code == 200:
                self.logger.info("Object verification successful")
            else:
                self.logger.warning(f"Object verification failed: {verify_response.status_code}")
            
            return object_id
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Object creation failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response text: {e.response.text}")
            raise

    def generate_save_url(self, credentials, object_id):
        """Generate a JWT for the Save to Google Wallet link."""
        try:
            iat = int(time.time())
            claims = {
                "iss": credentials.service_account_email,
                "aud": "google",
                "typ": "savetowallet",
                "iat": iat,
                "exp": iat + 3600,
                "origin": self.ORIGIN_URL,
                "payload": {
                    "genericObjects": [{"id": object_id}]
                }
            }

            # Debug: Print claims for verification
            self.logger.info(f"JWT Claims: {json.dumps(claims, indent=2)}")
            self.logger.info(f"Service Account Email: {credentials.service_account_email}")
            self.logger.info(f"Object ID: {object_id}")

            signed_jwt = jwt.encode(credentials.signer, claims).decode("utf-8")
            save_url = f"https://pay.google.com/gp/v/save/{signed_jwt}"
            self.logger.info("Generated wallet save URL")
            return save_url
        except Exception as e:
            self.logger.error(f"JWT generation failed: {str(e)}")
            raise

    def generate_pass_from_json(self, wallet_pass_json):
        """Create Google Wallet pass from JSON data."""
        try:
            self.logger.info("Starting wallet pass creation from JSON data")
            
            # Extract data from JSON
            receipt_data = {
                'merchantName': wallet_pass_json.get('subheader', {}).get('defaultValue', {}).get('value', 'Unknown Merchant'),
                'totalAmount': wallet_pass_json.get('header', {}).get('defaultValue', {}).get('value', '0.00').replace('₹', '').replace('$', ''),
                'purchaseDate': None,
                'items': []
            }
            
            # Extract date from text modules
            for module in wallet_pass_json.get('textModulesData', []):
                if module.get('header') == 'DATE':
                    receipt_data['purchaseDate'] = module.get('body', 'Unknown Date')
                elif module.get('header') == 'ITEMS':
                    # Parse items from text
                    items_text = module.get('body', '')
                    if items_text and items_text != 'No items listed':
                        for line in items_text.split('\n'):
                            if ':' in line and '$' in line:
                                try:
                                    name, price = line.split(':', 1)
                                    price = price.strip().replace('$', '')
                                    receipt_data['items'].append({
                                        'name': name.strip(),
                                        'price': float(price)
                                    })
                                except:
                                    continue
            
            # Generate Google Wallet pass
            user_id = str(uuid.uuid4())[:8]  # Short unique ID
            credentials = self.get_credentials()
            
            # Ensure class exists
            self.create_or_verify_class(credentials)
            
            # Create wallet object
            object_id = self.create_generic_object(credentials, user_id, receipt_data)
            
            # Generate save URL
            save_url = self.generate_save_url(credentials, object_id)
            
            self.logger.info("Wallet pass creation completed successfully")
            return save_url

        except Exception as e:
            self.logger.error(f"Wallet pass creation failed: {str(e)}")
            return f"❌ Error creating wallet pass: {str(e)}"

    def test_wallet_connection(self):
        """Test the wallet connection and credentials."""
        try:
            self.logger.info("Testing wallet connection...")
            credentials = self.get_credentials()
            self.logger.info(f"✅ Credentials loaded successfully")
            self.logger.info(f"Service Account Email: {credentials.service_account_email}")
            
            # Test API access
            headers = {
                "Authorization": f"Bearer {credentials.token}",
                "Content-Type": "application/json"
            }
            
            test_response = requests.get(
                "https://walletobjects.googleapis.com/walletobjects/v1/genericClass",
                headers=headers
            )
            
            self.logger.info(f"API Test Response: {test_response.status_code}")
            if test_response.status_code == 200:
                self.logger.info("✅ API access successful")
                return "✅ Wallet connection test successful"
            else:
                self.logger.error(f"❌ API access failed: {test_response.text}")
                return f"❌ API access failed: {test_response.status_code}"
                
        except Exception as e:
            self.logger.error(f"❌ Wallet connection test failed: {str(e)}")
            return f"❌ Wallet connection test failed: {str(e)}"

    def create_wallet_pass(self, extracted_data):
        """Create wallet pass from extracted data."""
        try:
            self.logger.info("Starting wallet pass creation from extracted data")
            
            # Generate Google Wallet pass
            user_id = str(uuid.uuid4())[:8]  # Short unique ID
            credentials = self.get_credentials()
            
            # Ensure class exists
            self.create_or_verify_class(credentials)
            
            # Create wallet object
            object_id = self.create_generic_object(credentials, user_id, extracted_data)
            
            # Generate save URL
            save_url = self.generate_save_url(credentials, object_id)
            
            self.logger.info("Wallet pass creation completed successfully")
            return save_url

        except Exception as e:
            self.logger.error(f"Wallet pass creation failed: {str(e)}")
            return f"❌ Error creating wallet pass: {str(e)}"
