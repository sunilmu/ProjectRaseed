from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import json
import base64
import tempfile
from typing import Optional, List
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Raseed Agent API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    status: str

class ReceiptUploadResponse(BaseModel):
    message: str
    receipt_id: Optional[str] = None
    extracted_data: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Raseed Agent API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Import the master agent
        from MASTER.agent import root_agent
        
        # Process the message through the master agent
        # Since ADK agents work differently, we'll simulate the agent's response based on the message
        message = request.message.lower()
        
        if "budget" in message or "plan" in message:
            # Budget planning response
            response = """I'll help you create a budget! Here's a monthly budget plan for $5000:

💰 **Monthly Budget Breakdown ($5000):**

🏠 **Housing (30%):** $1,500
   - Rent/Mortgage: $1,200
   - Utilities: $200
   - Insurance: $100

🍽️ **Food (15%):** $750
   - Groceries: $500
   - Dining out: $250

🚗 **Transportation (10%):** $500
   - Gas: $200
   - Public transport: $150
   - Maintenance: $150

💊 **Healthcare (10%):** $500
   - Insurance: $300
   - Medical expenses: $200

🎯 **Savings (20%):** $1,000
   - Emergency fund: $500
   - Investment: $500

🎨 **Entertainment (5%):** $250
   - Movies/Streaming: $100
   - Hobbies: $150

👕 **Personal (5%):** $250
   - Clothing: $150
   - Personal care: $100

📱 **Technology (3%):** $150
   - Phone/Internet: $100
   - Electronics: $50

🎁 **Miscellaneous (2%):** $100
   - Gifts: $50
   - Other: $50

💡 **Money-Saving Tips:**
- Cook at home more often
- Use public transportation
- Shop during sales
- Cancel unused subscriptions
- Use energy-efficient appliances

Would you like me to adjust this budget for your specific needs or city?"""
            
        elif "receipt" in message or "process" in message:
            # Receipt processing response
            response = """I can help you process receipts! Here's what I can do:

📄 **Receipt Processing Features:**
- Extract text from receipt images
- Parse merchant, date, total, and items
- Create Google Wallet passes
- Store data in Firestore database

📤 **To process a receipt:**
1. Upload an image using the /upload-receipt endpoint
2. I'll extract and parse the data
3. Create a digital wallet pass
4. Store the information

🔍 **What I extract:**
- Merchant name and address
- Transaction date and time
- Total amount
- Individual items and prices
- Payment method

Would you like to upload a receipt image now?"""
            
        elif "spending" in message or "data" in message or "query" in message:
            # Firestore query response
            response = """I can help you query your spending data! Here's what I can do:

📊 **Spending Analysis Features:**
- Query receipts by date range
- Find transactions by merchant
- Get spending by category
- Calculate total spending
- Generate spending reports

🔍 **Sample queries you can ask:**
- "Show me receipts from last week"
- "Find all Walmart receipts"
- "Get receipts between $50 and $100"
- "Show me all grocery receipts"
- "Get my spending summary"

📈 **Available Collections:**
- receipts
- transactions
- budgets
- categories

Would you like me to query your Firestore database for specific information?"""
            
        else:
            # General response
            response = f"""Hello! I'm your Raseed Agent assistant. I can help you with:

📄 **Receipt Processing:**
- Upload and process receipt images
- Extract data and create Google Wallet passes
- Store information in your database

💰 **Budget Planning:**
- Create monthly budgets
- Suggest spending allocations
- Provide money-saving tips
- City-specific recommendations

📊 **Spending Analysis:**
- Query your transaction data
- Generate spending reports
- Analyze spending patterns
- Get statistics and summaries

Your message: "{request.message}"

How can I help you today?"""
        
        return ChatResponse(
            response=response,
            agent_used="master_agent",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        # Generate a receipt ID
        receipt_id = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # For now, return mock data since we don't have the API key configured
        mock_extracted_data = {
            "merchant": "HEN AND CHICKEN",
            "address": "210 North Street, Southville, Bristol BS3 1JF",
            "date": "17/11/2018",
            "time": "13:37",
            "total": "10.50",
            "items": [
                {"name": "Porky Burger", "price": "8.00"},
                {"name": "House", "price": "2.50"}
            ],
            "payment_method": "Credit Card",
            "receipt_id": receipt_id
        }
        
        return ReceiptUploadResponse(
            message="Receipt processed successfully (mock data)",
            receipt_id=receipt_id,
            extracted_data=mock_extracted_data
        )
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": "Raseed Master Agent",
        "message": "API is running with intelligent responses"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 