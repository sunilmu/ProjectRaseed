# Receipt Manager Sub-Agent

A multi-lingual receipt processing agent that uses Google Vertex AI to extract and translate receipt data from images and videos.

## Features

- Processes both image and video files
- Multi-language support with automatic translation to English
- Extracts structured data: business name, receipt number, date, total, items, etc.
- Returns data in JSON format
- Uses Google Vertex AI Gemini model for accurate OCR and translation

## Usage

```python
from receipt_manager.agent import ReceiptManager

manager = ReceiptManager("your-project-id")
result = manager.process_receipt("path/to/receipt.jpg")
print(result)
```

## Command Line

```bash
python main.py path/to/receipt.jpg
```

## Environment Variables

- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: GCP region (default: us-central1)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON file