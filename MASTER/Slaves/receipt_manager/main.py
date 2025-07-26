#!/usr/bin/env python3
import json
import sys
from agent import ReceiptManager
from config import GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_or_video_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not GOOGLE_CLOUD_PROJECT:
        print("Error: GOOGLE_CLOUD_PROJECT not set in environment")
        sys.exit(1)
    
    manager = ReceiptManager(GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION)
    result = manager.process_receipt(file_path)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()