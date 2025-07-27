import requests
import base64
import re
import os
from datetime import datetime

# # def extract_receipt_data(image_path):
# #     try:
       
# #         image = cv2.imread(image_path)
# #         if image is None:
# #             raise ValueError("Could not load image")

        
# #         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #         gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        
# #         text = pytesseract.image_to_string(gray)

        
# #         receipt_data = {
# #             "business_name": None,
# #             "receipt_number": None,
# #             "date": None,
# #             "total": None,
# #             "items": []
# #         }

# #         # Define regex patterns for extraction
# #         date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s\w+\s\d{2,4})\b'
# #         total_pattern = r'(?:Total|TOTAL|Amount Due)\s*[:$]?\s*(\d+\.?\d*)'
# #         receipt_num_pattern = r'(?:Receipt|Transaction|Order)\s*[#No:]+?\s*(\d+|[A-Z0-9-]+)'
        
# #         # Extract business name (assuming it's one of the first few lines)
# #         lines = text.split('\n')
# #         receipt_data["business_name"] = lines[0].strip() if lines else None

# #         # Extract receipt number
# #         receipt_num_match = re.search(receipt_num_pattern, text, re.IGNORECASE)
# #         if receipt_num_match:
# #             receipt_data["receipt_number"] = receipt_num_match.group(1)

# #         # Extract date
# #         date_match = re.search(date_pattern, text)
# #         if date_match:
# #             try:
# #                 # Try parsing different date formats
# #                 date_str = date_match.group(0)
# #                 parsed_date = datetime.strptime(date_str, '%d/%m/%Y') if '/' in date_str else datetime.strptime(date_str, '%d-%m-%Y')
# #                 receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
# #             except ValueError:
# #                 try:
# #                     parsed_date = datetime.strptime(date_str, '%d %B %Y')
# #                     receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
# #                 except ValueError:
# #                     receipt_data["date"] = date_str  # Fallback to raw string if parsing fails

# #         # Extract total
# #         total_match = re.search(total_pattern, text, re.IGNORECASE)
# #         if total_match:
# #             receipt_data["total"] = float(total_match.group(1))

# #         # Extract items (basic assumption: items are lines with a name and price)
# #         item_pattern = r'(.+?)\s+(\d+\.?\d*)'
# #         for line in lines:
# #             item_match = re.search(item_pattern, line)
# #             if item_match:
# #                 item_name = item_match.group(1).strip()
# #                 item_price = float(item_match.group(2))
# #                 receipt_data["items"].append({"name": item_name, "price": item_price})

# #         # Save to text file
# #         output_file = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
# #         with open(output_file, 'w', encoding='utf-8') as f:
# #             f.write("Receipt Data Extracted:\n")
# #             f.write(f"Business Name: {receipt_data['business_name']}\n")
# #             f.write(f"Receipt Number: {receipt_data['receipt_number']}\n")
# #             f.write(f"Date: {receipt_data['date']}\n")
# #             f.write(f"Total: {receipt_data['total']}\n")
# #             f.write("Items:\n")
# #             for item in receipt_data['items']:
# #                 f.write(f"  - {item['name']}: {item['price']}\n")

# #         return receipt_data, output_file

# #     except Exception as e:
# #         return {"error": str(e)}, None
# ####################################################################################3
# import pytesseract
# import cv2
# import re
# import os
# from datetime import datetime

# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\sunil.t\Desktop\OCR\tesseract.exe"
# os.environ["TESSDATA_PREFIX"] = r"C:\Users\sunil.t\Desktop\OCR\tessdata"

# def extract_receipt_data(image_path):
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
#                 receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
#             except ValueError:
#                 try:
#                     parsed_date = datetime.strptime(date_str, '%d %B %Y')
#                     receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
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

#         # 🔁 Convert to structured text for agent parsing
#         summary_lines = [
#             f"Restaurant name: {receipt_data['business_name']}",
#             f"Receipt number: {receipt_data['receipt_number']}",
#             f"Date: {date_str or receipt_data['date']}",
#             f"Total: {receipt_data['total']}",
#             "Items:"
#         ] + [f"{item['name']}: {item['price']}" for item in receipt_data['items']]

#         return "\n".join(summary_lines)

#     except Exception as e:
#         return f"Error extracting receipt data: {str(e)}"
##############################################################################
import requests
import base64
import json
def extract_text_from_image(image_path, api_key):
    """
    Extract text from image using Google Vision API with enhanced error handling.
    """
    try:
        print(f"🔍 Opening image file: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            return f"❌ Error: Image file not found at {image_path}"
        
        # Read image file
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
            print(f"📊 Read {len(img_data)} bytes from image file")
            
            if len(img_data) == 0:
                return "❌ Error: Image file is empty"
            
            b64_image = base64.b64encode(img_data).decode("utf-8")
            print(f"📝 Base64 encoded image length: {len(b64_image)}")

        # Prepare API request
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        payload = {
            "requests": [
                {
                    "image": {"content": b64_image},
                    "features": [{"type": "TEXT_DETECTION"}]
                }
            ]
        }

        print(f"🌐 Sending request to Google Vision API...")
        headers = {"Content-Type": "application/json"}
        
        # Make API request with timeout
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"📡 Vision API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if we have responses
            if 'responses' in result and result['responses']:
                response_data = result['responses'][0]
                
                # Check for text annotations
                if 'textAnnotations' in response_data and response_data['textAnnotations']:
                    text = response_data['textAnnotations'][0].get('description', '')
                    if text and text.strip():
                        print(f"✅ Extracted text successfully! Length: {len(text)}")
                        print(f"📄 First 200 characters: {text[:200]}...")
                        return text
                    else:
                        print("⚠️ Text annotations found but empty")
                        return "❌ No text content found in image"
                else:
                    print("⚠️ No text annotations in response")
                    return "❌ No text detected in image"
            else:
                print("⚠️ No responses from Vision API")
                return "❌ No response from Vision API"
        else:
            error_msg = f"❌ Vision API error: {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f" - {error_detail.get('error', {}).get('message', 'Unknown error')}"
            except:
                error_msg += f" - {response.text[:200]}"
            
            print(f"❌ {error_msg}")
            return error_msg
    
    except requests.exceptions.Timeout:
        error_msg = "❌ Error: Request timeout - Vision API took too long to respond"
        print(error_msg)
        return error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Error: Network request failed - {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Exception occurred: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

import re
from datetime import datetime

def parse_receipt_data(raw_text: str) -> dict:
    """
    Parse raw OCR text into structured receipt data with enhanced pattern matching.
    """
    try:
        print(f"🔍 Parsing receipt data from {len(raw_text)} characters of text")
        
        # Initialize structured data
        structured_data = {
            "merchantName": "Unknown",
            "totalAmount": "0.00",
            "purchaseDate": "Unknown",
            "receiptNumber": "Unknown",
            "items": [],
            "rawText": raw_text
        }
        
        # Split text into lines for processing
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        print(f"📄 Processing {len(lines)} non-empty lines")
        
        # Extract merchant name (look for business names in first few lines)
        merchant_keywords = ['restaurant', 'store', 'shop', 'market', 'cafe', 'diner', 'pizza', 'burger']
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            line_lower = line.lower()
            # Skip lines that are clearly not merchant names
            if (not line.isdigit() and 
                not re.match(r'^\d+\.?\d*$', line) and
                not any(keyword in line_lower for keyword in ['total', 'subtotal', 'tax', 'amount', 'date', 'receipt']) and
                len(line) > 2):
                structured_data["merchantName"] = line
                print(f"🏪 Found merchant: {line}")
                break
        
        # Extract total amount with multiple patterns
        total_patterns = [
            r'(?:Total|TOTAL|Amount Due|Grand Total|Final Total)\s*[:$]?\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:Total|TOTAL)',
            r'Total\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*$',  # Amount at end of line
            r'(\d+\.?\d*)\s*(?:USD|$)',  # Amount with USD or end
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                amount = match.group(1)
                # Validate it's a reasonable amount
                try:
                    float_amount = float(amount)
                    if 0.01 <= float_amount <= 10000:  # Reasonable range
                        structured_data["totalAmount"] = amount
                        print(f"💰 Found total amount: ${amount}")
                        break
                except ValueError:
                    continue
        
        # Extract date with multiple formats
        date_patterns = [
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
            r'\b(\d{1,2}\s+\w+\s+\d{2,4})\b',
            r'\b(\d{4}-\d{2}-\d{2})\b',
            r'\b(\d{2}/\d{2}/\d{4})\b',
            r'\b(\d{2}-\d{2}-\d{4})\b'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, raw_text)
            if match:
                date_str = match.group(1)
                try:
                    # Try different date parsing formats
                    if '/' in date_str:
                        parts = date_str.split('/')
                        if len(parts[0]) == 4:  # YYYY/MM/DD
                            parsed_date = datetime.strptime(date_str, '%Y/%m/%d')
                        else:  # DD/MM/YYYY
                            parsed_date = datetime.strptime(date_str, '%d/%m/%Y')
                    elif '-' in date_str:
                        if len(date_str.split('-')[0]) == 4:  # YYYY-MM-DD
                            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                        else:  # DD-MM-YYYY
                            parsed_date = datetime.strptime(date_str, '%d-%m-%Y')
                    else:
                        parsed_date = datetime.strptime(date_str, '%d %B %Y')
                    
                    structured_data["purchaseDate"] = parsed_date.strftime('%Y-%m-%d')
                    print(f"📅 Found date: {structured_data['purchaseDate']}")
                    break
                except ValueError:
                    continue
        
        # Extract receipt number
        receipt_patterns = [
            r'(?:Receipt|Transaction|Order|Invoice)\s*[#No:]+?\s*(\d+|[A-Z0-9-]+)',
            r'Receipt\s*(\d+)',
            r'Order\s*(\d+)',
            r'#\s*(\d+)',
            r'(\d{6,})',  # Long numbers might be receipt IDs
        ]
        
        for pattern in receipt_patterns:
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                receipt_num = match.group(1)
                structured_data["receiptNumber"] = receipt_num
                print(f"🔢 Found receipt number: {receipt_num}")
                break
        
        # Extract items with improved pattern matching
        items_found = []
        item_patterns = [
            r'(.+?)\s+(\d+\.?\d*)',  # Name + Price
            r'(\d+\.?\d*)\s+(.+)',    # Price + Name
            r'(.+?)\s*\$(\d+\.?\d*)', # Name + $Price
            r'(\d+\.?\d*)\s*\$',      # Price + $
        ]
        
        for line in lines:
            line_lower = line.lower()
            # Skip lines that are clearly not items
            if any(keyword in line_lower for keyword in ['total', 'subtotal', 'tax', 'amount due', 'grand total']):
                continue
                
            for pattern in item_patterns:
                item_match = re.search(pattern, line)
                if item_match:
                    if len(item_match.groups()) == 2:
                        item_name = item_match.group(1).strip()
                        item_price = item_match.group(2)
                    else:
                        continue
                    
                    # Validate item data
                    if (item_name and item_price and 
                        len(item_name) > 1 and 
                        item_name.lower() not in ['total', 'subtotal', 'tax', 'amount']):
                        try:
                            float_price = float(item_price)
                            if 0.01 <= float_price <= 1000:  # Reasonable item price
                                items_found.append({
                                    "name": item_name,
                                    "price": item_price
                                })
                                print(f"🛒 Found item: {item_name} - ${item_price}")
                        except ValueError:
                            continue
        
        structured_data["items"] = items_found
        print(f"✅ Parsing complete! Found {len(items_found)} items")
        
        return structured_data
        
    except Exception as e:
        print(f"❌ Error parsing receipt data: {str(e)}")
        # Return basic structure with error info
        return {
            "merchantName": "Unknown",
            "totalAmount": "0.00",
            "purchaseDate": "Unknown",
            "receiptNumber": "Unknown",
            "items": [],
            "rawText": raw_text,
            "error": str(e)
        }
