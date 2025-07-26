import json
import os
from typing import Union, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import base64
import cv2

class ReceiptManager:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)
        
    def _encode_media(self, file_path: str) -> tuple[str, str]:
        """Encode image/video file to base64"""
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            mime_type = f"image/{ext[1:]}"
        elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
            mime_type = f"video/{ext[1:]}"
        else:
            mime_type = "application/octet-stream"
            
        return content, mime_type
    
    def _extract_frames_from_video(self, video_path: str, max_frames: int = 5) -> list:
        """Extract key frames from video for processing"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for i in range(0, frame_count, frame_count // max_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_b64 = base64.b64encode(buffer).decode('utf-8')
                frames.append(frame_b64)
                
        cap.release()
        return frames
    
    def process_receipt(self, file_path: str) -> Dict[str, Any]:
        """Process receipt from image or video file"""
        try:
            content, mime_type = self._encode_media(file_path)
            
            if mime_type.startswith('video'):
                frames = self._extract_frames_from_video(file_path)
                content = frames[0] if frames else content
                mime_type = "image/jpeg"
            
            prompt = """Extract all text from this receipt image and translate it to English. 
            Return the data in JSON format with these fields:
            {
                "business_name": "string",
                "receipt_number": "string", 
                "date": "YYYY-MM-DD",
                "total": "number",
                "currency": "string",
                "items": [{"name": "string", "price": "number", "quantity": "number"}],
                "tax": "number",
                "original_language": "string",
                "raw_text": "string"
            }"""
            
            model = aiplatform.Model("publishers/google/models/gemini-1.5-pro")
            
            response = model.predict(
                instances=[{
                    "content": {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": content}}
                        ]
                    }
                }]
            )
            
            result_text = response.predictions[0]['content']['parts'][0]['text']
            
            # Parse JSON from response
            try:
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                json_str = result_text[json_start:json_end]
                return json.loads(json_str)
            except:
                return {"error": "Failed to parse JSON response", "raw_response": result_text}
                
        except Exception as e:
            return {"error": str(e)}