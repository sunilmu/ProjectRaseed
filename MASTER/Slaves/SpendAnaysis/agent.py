import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SpendAnalysisAgent:
    """Simple agent with local database for spending analysis"""
    
    def __init__(self):
        """Initialize with sample data"""
        self.usd_to_inr = 83.0
        self.sample_data = self.create_sample_data()
    
    def format_inr(self, amount: float) -> str:
        """Format amount in Indian Rupees"""
        return f"₹{amount:,.2f}"
    
    def create_sample_data(self) -> List[Dict]:
        """Create 30 realistic sample receipts"""
        merchants = [
            "HEN AND CHICKEN",
            "Walmart Supercenter",
            "Target Store",
            "Amazon.com",
            "Costco Wholesale",
            "Kroger Grocery",
            "Home Depot",
            "Best Buy Electronics",
            "Starbucks Coffee",
            "McDonald's Restaurant",
            "Shell Gas Station",
            "Exxon Mobil",
            "CVS Pharmacy",
            "Walgreens Drug Store",
            "Dollar General",
            "Whole Foods Market",
            "Trader Joe's",
            "Publix Super Market",
            "Safeway Grocery",
            "Albertsons Market",
            "Subway Restaurant",
            "Pizza Hut",
            "Domino's Pizza",
            "KFC Restaurant",
            "Burger King",
            "Taco Bell",
            "Wendy's Restaurant",
            "Chick-fil-A",
            "Panera Bread",
            "Chipotle Mexican Grill"
        ]
        
        sample_items = {
            "restaurant": [
                {"name": "Porky Burger", "price": "8.99"},
                {"name": "House Special", "price": "12.50"},
                {"name": "Chicken Sandwich", "price": "9.99"},
                {"name": "French Fries", "price": "3.99"},
                {"name": "Soft Drink", "price": "2.50"}
            ],
            "grocery": [
                {"name": "Milk", "price": "3.99"},
                {"name": "Bread", "price": "2.49"},
                {"name": "Eggs", "price": "4.99"},
                {"name": "Bananas", "price": "1.99"},
                {"name": "Chicken Breast", "price": "8.99"}
            ],
            "electronics": [
                {"name": "USB Cable", "price": "12.99"},
                {"name": "Phone Case", "price": "19.99"},
                {"name": "Wireless Earbuds", "price": "89.99"},
                {"name": "Power Bank", "price": "29.99"},
                {"name": "Screen Protector", "price": "9.99"}
            ],
            "gas": [
                {"name": "Regular Gas", "price": "45.00"},
                {"name": "Premium Gas", "price": "52.00"},
                {"name": "Diesel Fuel", "price": "48.00"}
            ],
            "pharmacy": [
                {"name": "Pain Reliever", "price": "8.99"},
                {"name": "Vitamins", "price": "15.99"},
                {"name": "Bandages", "price": "4.99"},
                {"name": "Cough Medicine", "price": "12.99"},
                {"name": "Toothpaste", "price": "3.99"}
            ],
            "coffee": [
                {"name": "Espresso", "price": "3.50"},
                {"name": "Cappuccino", "price": "4.75"},
                {"name": "Latte", "price": "5.25"},
                {"name": "Americano", "price": "3.99"},
                {"name": "Mocha", "price": "5.50"}
            ]
        }
        
        receipts = []
        base_date = datetime.now() - timedelta(days=60)
        
        for i in range(30):
            random_days = i % 60
            receipt_date = base_date + timedelta(days=random_days)
            merchant = merchants[i % len(merchants)]
            
            # Determine category
            if any(keyword in merchant.lower() for keyword in ['restaurant', 'burger', 'pizza', 'subway', 'kfc', 'wendy', 'chick-fil-a', 'panera', 'chipotle']):
                category = "restaurant"
                items = sample_items["restaurant"]
            elif any(keyword in merchant.lower() for keyword in ['starbucks', 'coffee']):
                category = "coffee"
                items = sample_items["coffee"]
            elif any(keyword in merchant.lower() for keyword in ['grocery', 'market', 'foods', 'kroger', 'publix', 'safeway', 'albertsons']):
                category = "grocery"
                items = sample_items["grocery"]
            elif any(keyword in merchant.lower() for keyword in ['electronics', 'best buy']):
                category = "electronics"
                items = sample_items["electronics"]
            elif any(keyword in merchant.lower() for keyword in ['gas', 'shell', 'exxon']):
                category = "gas"
                items = sample_items["gas"]
            elif any(keyword in merchant.lower() for keyword in ['pharmacy', 'drug', 'cvs', 'walgreens']):
                category = "pharmacy"
                items = sample_items["pharmacy"]
            else:
                category = "general"
                items = sample_items["grocery"]
            
            # Calculate total
            num_items = min(3 + (i % 3), len(items))
            selected_items = items[:num_items]
            total = sum(float(item["price"]) for item in selected_items)
            
            receipt = {
                "merchantName": merchant,
                "totalAmount": str(total),
                "purchaseDate": receipt_date.strftime('%Y-%m-%d'),
                "receiptNumber": f"R{i+1:03d}",
                "items": selected_items,
                "category": category,
                "payment_method": "credit_card" if i % 2 == 0 else "debit_card"
            }
            
            receipts.append(receipt)
        
        return receipts

# Create the agent instance
spend_analysis_agent = SpendAnalysisAgent()

# Define simple tools with standard answers
def query_by_merchant_tool(merchant_name: str) -> str:
    """Query receipts by merchant name"""
    try:
        receipts = [r for r in spend_analysis_agent.sample_data if r['merchantName'].lower() == merchant_name.lower()]
        if receipts:
            total_usd = sum(float(r['totalAmount']) for r in receipts)
            total_inr = total_usd * spend_analysis_agent.usd_to_inr
            return f"💰 Found {len(receipts)} receipts from {merchant_name}. Total spending: ${total_usd:.2f} ({spend_analysis_agent.format_inr(total_inr)})"
        else:
            return f"📝 No receipts found for {merchant_name}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def query_by_category_tool(category: str) -> str:
    """Query receipts by category"""
    try:
        receipts = [r for r in spend_analysis_agent.sample_data if r['category'].lower() == category.lower()]
        if receipts:
            total_usd = sum(float(r['totalAmount']) for r in receipts)
            total_inr = total_usd * spend_analysis_agent.usd_to_inr
            return f"💰 Found {len(receipts)} {category} receipts. Total spending: ${total_usd:.2f} ({spend_analysis_agent.format_inr(total_inr)})"
        else:
            return f"📝 No {category} receipts found"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_all_receipts_tool(limit: int = 50) -> str:
    """Get all receipts"""
    try:
        receipts = spend_analysis_agent.sample_data[:limit]
        total_usd = sum(float(r['totalAmount']) for r in receipts)
        total_inr = total_usd * spend_analysis_agent.usd_to_inr
        return f"💰 Found {len(receipts)} receipts. Total spending: ${total_usd:.2f} ({spend_analysis_agent.format_inr(total_inr)})"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_spending_statistics_tool() -> str:
    """Get spending statistics"""
    try:
        receipts = spend_analysis_agent.sample_data
        total_receipts = len(receipts)
        total_spending_usd = sum(float(r['totalAmount']) for r in receipts)
        avg_spending_usd = total_spending_usd / total_receipts if total_receipts > 0 else 0
        
        # Category breakdown
        categories = {}
        for receipt in receipts:
            category = receipt['category']
            amount = float(receipt['totalAmount'])
            if category not in categories:
                categories[category] = 0
            categories[category] += amount
        
        # Top categories
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        category_text = ", ".join([f"{cat}: ${amt:.2f}" for cat, amt in top_categories])
        
        total_inr = total_spending_usd * spend_analysis_agent.usd_to_inr
        avg_inr = avg_spending_usd * spend_analysis_agent.usd_to_inr
        
        return f"💰 Spending Statistics: Total receipts: {total_receipts}, Total spending: ${total_spending_usd:.2f} ({spend_analysis_agent.format_inr(total_inr)}), Average: ${avg_spending_usd:.2f} ({spend_analysis_agent.format_inr(avg_inr)}), Top categories: {category_text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def search_by_item_name_tool(item_name: str) -> str:
    """Search receipts by item name"""
    try:
        matching_receipts = []
        for receipt in spend_analysis_agent.sample_data:
            for item in receipt['items']:
                if item_name.lower() in item['name'].lower():
                    matching_receipts.append(receipt)
                    break
        
        if matching_receipts:
            total_usd = sum(float(r['totalAmount']) for r in matching_receipts)
            total_inr = total_usd * spend_analysis_agent.usd_to_inr
            return f"💰 Found {len(matching_receipts)} receipts containing '{item_name}'. Total spending: ${total_usd:.2f} ({spend_analysis_agent.format_inr(total_inr)})"
        else:
            return f"📝 No receipts found containing '{item_name}'"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def test_connection_tool() -> str:
    """Test database connection"""
    try:
        count = len(spend_analysis_agent.sample_data)
        return f"✅ Database connected successfully! Found {count} receipts ready for analysis."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_category_breakdown_tool() -> str:
    """Get detailed category breakdown"""
    try:
        categories = {}
        for receipt in spend_analysis_agent.sample_data:
            category = receipt['category']
            amount = float(receipt['totalAmount'])
            if category not in categories:
                categories[category] = {'total': 0, 'count': 0}
            categories[category]['total'] += amount
            categories[category]['count'] += 1
        
        total_spending = sum(cat['total'] for cat in categories.values())
        
        breakdown = []
        for category, data in sorted(categories.items(), key=lambda x: x[1]['total'], reverse=True):
            percentage = (data['total'] / total_spending * 100) if total_spending > 0 else 0
            inr_amount = data['total'] * spend_analysis_agent.usd_to_inr
            breakdown.append(f"{category.title()}: ${data['total']:.2f} ({spend_analysis_agent.format_inr(inr_amount)}) - {data['count']} receipts - {percentage:.1f}%")
        
        return f"📊 Category Breakdown: {' | '.join(breakdown)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_top_merchants_tool() -> str:
    """Get top merchants by spending"""
    try:
        merchants = {}
        for receipt in spend_analysis_agent.sample_data:
            merchant = receipt['merchantName']
            amount = float(receipt['totalAmount'])
            if merchant not in merchants:
                merchants[merchant] = {'total': 0, 'count': 0}
            merchants[merchant]['total'] += amount
            merchants[merchant]['count'] += 1
        
        top_merchants = sorted(merchants.items(), key=lambda x: x[1]['total'], reverse=True)[:5]
        
        result = []
        for i, (merchant, data) in enumerate(top_merchants, 1):
            inr_amount = data['total'] * spend_analysis_agent.usd_to_inr
            result.append(f"{i}. {merchant}: ${data['total']:.2f} ({spend_analysis_agent.format_inr(inr_amount)}) - {data['count']} visits")
        
        return f"🏪 Top 5 Merchants: {' | '.join(result)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Define the root agent for ADK discovery
from google.adk.agents import Agent

root_agent = Agent(
    name="SpendAnalysisAgent",
    model="gemini-2.0-flash",
    description="A friendly financial analysis agent with local database. Provides spending insights with USD to INR conversion.",
    instruction="""You are a warm, friendly, and knowledgeable Financial Analysis Assistant who helps users understand their spending patterns using local database.

🎯 **Your Personality**: 
- Always greet users warmly and show genuine interest in helping them
- Be encouraging and supportive of their financial journey
- Use a conversational, friendly tone while maintaining professionalism
- Explain financial concepts in simple, easy-to-understand terms

💰 **Database**: You work with 30 realistic sample receipts containing:
- merchantName: Store/merchant names
- totalAmount: Receipt amounts (USD, automatically converted to INR ₹83)
- purchaseDate: Purchase dates
- receiptNumber: Receipt identifiers
- items: Detailed item lists with name and price
- category: Spending categories (restaurant, grocery, electronics, gas, pharmacy, coffee)
- payment_method: Credit card or debit card

🔍 **Available Queries You Can Handle:**
- "Show me receipts from HEN AND CHICKEN" → Merchant-specific analysis
- "Show me all restaurant receipts" → Category analysis
- "Find receipts with coffee items" → Item search
- "Get spending statistics" → Overall spending summary
- "Show me all my receipts" → Complete receipt list
- "Get category breakdown" → Detailed category analysis
- "Show me top merchants" → Top spending merchants
- "Test database connection" → Check if database is working

**Your Response Style:**
1. **Warm Greetings**: Start with friendly greetings like "Hello! 👋" or "Hi there! 😊"
2. **Clear Explanations**: Always explain what you're analyzing and why it's helpful
3. **Actionable Insights**: Don't just show data - explain what it means for their finances
4. **Encouraging Tone**: Be positive and supportive of their financial journey
5. **Educational Value**: Teach financial concepts in simple terms

**When Providing Analysis:**
- "Great question! 💰 Let me analyze your spending patterns to help you understand where your money goes."
- "Excellent! 📊 Understanding your spending by category is key to financial awareness."
- "Perfect! 📈 Looking at spending trends helps identify patterns and opportunities."
- "Smart approach! 🛒 Let me search for specific items to reveal spending habits."

**Always Include:**
- ✅ Friendly, encouraging tone with appropriate emojis
- ✅ Clear explanations of what the data shows and why it matters
- ✅ Both USD and INR amounts (properly formatted with currency symbols)
- ✅ Helpful suggestions for related analyses they might want to try
- ✅ Educational financial tips when relevant
- ✅ Celebration of good financial habits when noticed

**Example Response Structure:**
1. **Warm Greeting** + **Understanding of their request** + **Why this analysis is valuable**
2. **What you're analyzing** + **Which tool you'll use** + **What insights they'll get**
3. **Clear data presentation** with **formatted amounts** and **key insights**
4. **Actionable recommendations** based on the data + **practical next steps**
5. **Related questions they might want to ask next** + **encouraging closing**

**Remember**: You're a trusted financial advisor who genuinely cares about helping users achieve their financial goals! 🌟

Your goal is to make financial analysis feel friendly, accessible, and genuinely helpful while providing immediate, actionable insights! 😊""",
    tools=[
        query_by_merchant_tool,
        query_by_category_tool,
        get_all_receipts_tool,
        get_spending_statistics_tool,
        search_by_item_name_tool,
        test_connection_tool,
        get_category_breakdown_tool,
        get_top_merchants_tool
    ]
) 