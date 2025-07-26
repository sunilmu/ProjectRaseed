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

#         # Define regex patterns for extraction
#         date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s\w+\s\d{2,4})\b'
#         total_pattern = r'(?:Total|TOTAL|Amount Due)\s*[:$]?\s*(\d+\.?\d*)'
#         receipt_num_pattern = r'(?:Receipt|Transaction|Order)\s*[#No:]+?\s*(\d+|[A-Z0-9-]+)'
        
#         # Extract business name (assuming it's one of the first few lines)
#         lines = text.split('\n')
#         receipt_data["business_name"] = lines[0].strip() if lines else None

#         # Extract receipt number
#         receipt_num_match = re.search(receipt_num_pattern, text, re.IGNORECASE)
#         if receipt_num_match:
#             receipt_data["receipt_number"] = receipt_num_match.group(1)

#         # Extract date
#         date_match = re.search(date_pattern, text)
#         if date_match:
#             try:
#                 # Try parsing different date formats
#                 date_str = date_match.group(0)
#                 parsed_date = datetime.strptime(date_str, '%d/%m/%Y') if '/' in date_str else datetime.strptime(date_str, '%d-%m-%Y')
#                 receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
#             except ValueError:
#                 try:
#                     parsed_date = datetime.strptime(date_str, '%d %B %Y')
#                     receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
#                 except ValueError:
#                     receipt_data["date"] = date_str  # Fallback to raw string if parsing fails

#         # Extract total
#         total_match = re.search(total_pattern, text, re.IGNORECASE)
#         if total_match:
#             receipt_data["total"] = float(total_match.group(1))

#         # Extract items (basic assumption: items are lines with a name and price)
#         item_pattern = r'(.+?)\s+(\d+\.?\d*)'
#         for line in lines:
#             item_match = re.search(item_pattern, line)
#             if item_match:
#                 item_name = item_match.group(1).strip()
#                 item_price = float(item_match.group(2))
#                 receipt_data["items"].append({"name": item_name, "price": item_price})

#         # Save to text file
#         output_file = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#         with open(output_file, 'w', encoding='utf-8') as f:
#             f.write("Receipt Data Extracted:\n")
#             f.write(f"Business Name: {receipt_data['business_name']}\n")
#             f.write(f"Receipt Number: {receipt_data['receipt_number']}\n")
#             f.write(f"Date: {receipt_data['date']}\n")
#             f.write(f"Total: {receipt_data['total']}\n")
#             f.write("Items:\n")
#             for item in receipt_data['items']:
#                 f.write(f"  - {item['name']}: {item['price']}\n")

#         return receipt_data, output_file

#     except Exception as e:
#         return {"error": str(e)}, None
####################################################################################3
import pytesseract
import cv2
import re
import os
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\sunil.t\Desktop\OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Users\sunil.t\Desktop\OCR\tessdata"

def extract_receipt_data(image_path):
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
                receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                try:
                    parsed_date = datetime.strptime(date_str, '%d %B %Y')
                    receipt_data["date"] = parsed_date.strftime('%Y-%m-%d')
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

        # 🔁 Convert to structured text for agent parsing
        summary_lines = [
            f"Restaurant name: {receipt_data['business_name']}",
            f"Receipt number: {receipt_data['receipt_number']}",
            f"Date: {date_str or receipt_data['date']}",
            f"Total: {receipt_data['total']}",
            "Items:"
        ] + [f"{item['name']}: {item['price']}" for item in receipt_data['items']]

        return "\n".join(summary_lines)

    except Exception as e:
        return f"Error extracting receipt data: {str(e)}"
