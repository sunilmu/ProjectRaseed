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

def get_fuel_spending_this_month_tool() -> str:
    """Get fuel spending for the current month"""
    try:
        from datetime import datetime, timedelta
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        fuel_receipts = []
        total_fuel_spending = 0.0
        
        for receipt in spend_analysis_agent.sample_data:
            # Check if it's a gas station receipt
            merchant = receipt['merchantName'].lower()
            if any(gas_station in merchant for gas_station in ['shell', 'exxon', 'gas', 'fuel', 'mobil']):
                # Parse the date
                try:
                    receipt_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
                    if receipt_date.month == current_month and receipt_date.year == current_year:
                        fuel_receipts.append(receipt)
                        total_fuel_spending += float(receipt['totalAmount'])
                except:
                    # If date parsing fails, check if it's a recent receipt
                    continue
        
        if not fuel_receipts:
            return "⛽ No fuel purchases found this month."
        
        inr_amount = total_fuel_spending * spend_analysis_agent.usd_to_inr
        
        result = f"⛽ **Fuel Spending This Month:**\n"
        result += f"💰 Total: ${total_fuel_spending:.2f} ({spend_analysis_agent.format_inr(inr_amount)})\n"
        result += f"📊 Purchases: {len(fuel_receipts)}\n"
        
        # Quick insight
        if total_fuel_spending > 100:
            result += f"💡 Consider carpooling to reduce fuel costs.\n"
        elif len(fuel_receipts) > 3:
            result += f"💡 Frequent purchases - look for bulk discounts.\n"
        else:
            result += f"💡 Your fuel spending looks reasonable.\n"
        
        return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

def can_cook_biryani_with_groceries_tool() -> str:
    """Analyze if available groceries can be used to cook biryani"""
    try:
        # Biryani ingredients checklist
        biryani_ingredients = {
            'rice': ['rice', 'basmati', 'long grain'],
            'meat': ['chicken', 'mutton', 'beef', 'lamb', 'meat'],
            'spices': ['cardamom', 'cinnamon', 'cloves', 'bay leaves', 'cumin', 'coriander', 'turmeric', 'saffron'],
            'vegetables': ['onion', 'tomato', 'ginger', 'garlic', 'mint', 'coriander leaves'],
            'dairy': ['ghee', 'yogurt', 'milk'],
            'nuts': ['cashews', 'almonds', 'raisins'],
            'other': ['oil', 'salt', 'sugar']
        }
        
        # Collect all grocery items from receipts
        available_groceries = []
        grocery_receipts = []
        
        for receipt in spend_analysis_agent.sample_data:
            merchant = receipt['merchantName'].lower()
            # Check if it's a grocery store
            if any(grocery in merchant for grocery in ['walmart', 'kroger', 'whole foods', 'trader joe', 'publix', 'safeway', 'albertsons', 'grocery', 'market']):
                grocery_receipts.append(receipt)
                for item in receipt.get('items', []):
                    item_name = item.get('name', '').lower()
                    available_groceries.append(item_name)
        
        if not grocery_receipts:
            return "🛒 No grocery purchases found. Need to shop for biryani ingredients!"
        
        # Analyze what ingredients are available
        available_ingredients = {}
        missing_ingredients = {}
        
        for category, ingredients in biryani_ingredients.items():
            available_ingredients[category] = []
            missing_ingredients[category] = []
            
            for ingredient in ingredients:
                found = False
                for grocery in available_groceries:
                    if ingredient in grocery:
                        available_ingredients[category].append(ingredient)
                        found = True
                        break
                if not found:
                    missing_ingredients[category].append(ingredient)
        
        # Calculate availability percentage
        total_ingredients = sum(len(ingredients) for ingredients in biryani_ingredients.values())
        available_count = sum(len(ingredients) for ingredients in available_ingredients.values())
        availability_percentage = (available_count / total_ingredients) * 100
        
        result = f"🍚 **Biryani Analysis:** {availability_percentage:.0f}% ready\n\n"
        
        # Quick verdict
        if availability_percentage >= 70:
            result += "✅ **YES!** You can cook biryani.\n"
        elif availability_percentage >= 50:
            result += "🤔 **MAYBE** - need some shopping.\n"
        else:
            result += "❌ **NO** - need more ingredients.\n"
        
        # Key missing items
        if missing_ingredients.get('meat'):
            result += f"💡 Buy: meat (chicken/mutton)\n"
        if missing_ingredients.get('rice'):
            result += f"💡 Buy: basmati rice\n"
        if missing_ingredients.get('spices'):
            result += f"💡 Buy: biryani spices\n"
        
        return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

def what_can_i_cook_with_groceries_tool() -> str:
    """Analyze available groceries and suggest multiple recipes that can be cooked"""
    try:
        # Recipe database with ingredients and difficulty
        recipes = {
            'Pasta Carbonara': {
                'ingredients': ['pasta', 'eggs', 'bacon', 'cheese', 'parmesan', 'black pepper', 'salt'],
                'difficulty': 'Easy',
                'time': '20 minutes',
                'category': 'Italian'
            },
            'Chicken Stir Fry': {
                'ingredients': ['chicken', 'vegetables', 'soy sauce', 'oil', 'garlic', 'ginger', 'onion'],
                'difficulty': 'Medium',
                'time': '25 minutes',
                'category': 'Asian'
            },
            'Vegetable Curry': {
                'ingredients': ['onion', 'tomato', 'potato', 'carrot', 'spices', 'turmeric', 'cumin', 'coriander', 'oil'],
                'difficulty': 'Medium',
                'time': '30 minutes',
                'category': 'Indian'
            },
            'Beef Tacos': {
                'ingredients': ['beef', 'tortillas', 'lettuce', 'tomato', 'cheese', 'onion', 'spices'],
                'difficulty': 'Easy',
                'time': '20 minutes',
                'category': 'Mexican'
            },
            'Fish and Chips': {
                'ingredients': ['fish', 'potato', 'flour', 'oil', 'salt', 'pepper'],
                'difficulty': 'Medium',
                'time': '30 minutes',
                'category': 'British'
            },
            'Vegetable Soup': {
                'ingredients': ['carrot', 'onion', 'celery', 'potato', 'tomato', 'vegetable broth', 'herbs'],
                'difficulty': 'Easy',
                'time': '45 minutes',
                'category': 'Soup'
            },
            'Chicken Rice Bowl': {
                'ingredients': ['chicken', 'rice', 'vegetables', 'soy sauce', 'oil', 'garlic'],
                'difficulty': 'Easy',
                'time': '25 minutes',
                'category': 'Asian'
            },
            'Pizza Margherita': {
                'ingredients': ['flour', 'tomato', 'mozzarella', 'basil', 'olive oil', 'salt'],
                'difficulty': 'Medium',
                'time': '40 minutes',
                'category': 'Italian'
            },
            'Beef Burger': {
                'ingredients': ['beef', 'bun', 'lettuce', 'tomato', 'onion', 'cheese', 'ketchup'],
                'difficulty': 'Easy',
                'time': '20 minutes',
                'category': 'American'
            },
            'Vegetable Pasta': {
                'ingredients': ['pasta', 'vegetables', 'olive oil', 'garlic', 'parmesan', 'salt', 'pepper'],
                'difficulty': 'Easy',
                'time': '20 minutes',
                'category': 'Italian'
            },
            'Chicken Salad': {
                'ingredients': ['chicken', 'lettuce', 'tomato', 'cucumber', 'olive oil', 'lemon', 'salt'],
                'difficulty': 'Easy',
                'time': '15 minutes',
                'category': 'Salad'
            },
            'Rice and Beans': {
                'ingredients': ['rice', 'beans', 'onion', 'garlic', 'spices', 'oil', 'salt'],
                'difficulty': 'Easy',
                'time': '30 minutes',
                'category': 'Vegetarian'
            },
            'Scrambled Eggs': {
                'ingredients': ['eggs', 'milk', 'butter', 'salt', 'pepper'],
                'difficulty': 'Easy',
                'time': '10 minutes',
                'category': 'Breakfast'
            },
            'Grilled Cheese': {
                'ingredients': ['bread', 'cheese', 'butter'],
                'difficulty': 'Easy',
                'time': '10 minutes',
                'category': 'Sandwich'
            },
            'Fruit Smoothie': {
                'ingredients': ['banana', 'strawberry', 'milk', 'yogurt', 'honey'],
                'difficulty': 'Easy',
                'time': '5 minutes',
                'category': 'Drink'
            }
        }
        
        # Collect all grocery items from receipts
        available_groceries = []
        grocery_receipts = []
        
        for receipt in spend_analysis_agent.sample_data:
            merchant = receipt['merchantName'].lower()
            # Check if it's a grocery store
            if any(grocery in merchant for grocery in ['walmart', 'kroger', 'whole foods', 'trader joe', 'publix', 'safeway', 'albertsons', 'grocery', 'market']):
                grocery_receipts.append(receipt)
                for item in receipt.get('items', []):
                    item_name = item.get('name', '').lower()
                    available_groceries.append(item_name)
        
        if not grocery_receipts:
            return "🛒 No grocery purchases found. Time to go shopping!"
        
        # Analyze which recipes can be made
        possible_recipes = []
        
        for recipe_name, recipe_data in recipes.items():
            required_ingredients = recipe_data['ingredients']
            available_count = 0
            
            for ingredient in required_ingredients:
                for grocery in available_groceries:
                    if ingredient in grocery:
                        available_count += 1
                        break
            
            # Calculate availability percentage
            availability_percentage = (available_count / len(required_ingredients)) * 100
            
            if availability_percentage >= 60:  # At least 60% of ingredients available
                possible_recipes.append({
                    'name': recipe_name,
                    'availability': availability_percentage,
                    'difficulty': recipe_data['difficulty'],
                    'time': recipe_data['time'],
                    'category': recipe_data['category']
                })
        
        # Sort recipes by availability percentage
        possible_recipes.sort(key=lambda x: x['availability'], reverse=True)
        
        result = f"🍳 **What Can You Cook?**\n"
        result += f"📦 Found {len(possible_recipes)} recipes from {len(available_groceries)} grocery items\n\n"
        
        if not possible_recipes:
            result += "❌ No recipes found. Buy more ingredients!\n"
            result += "💡 Try: chicken, rice, vegetables, spices\n"
        else:
            # Top 3 recommendations
            result += "🏆 **Top Recipes:**\n"
            for i, recipe in enumerate(possible_recipes[:3], 1):
                status = "🟢" if recipe['availability'] >= 80 else "🟡" if recipe['availability'] >= 70 else "🟠"
                result += f"   {i}. {status} {recipe['name']} ({recipe['availability']:.0f}%)\n"
                result += f"      {recipe['time']} | {recipe['difficulty']}\n"
        
        return result
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
- "How much fuel I got in this month?" → Fuel spending analysis for current month
- "Can I cook biryani with the grocery I have?" → Analyze available ingredients for cooking
- "What can I cook with my groceries?" → Suggest multiple recipes based on available ingredients
- "Test database connection" → Check if database is working

**Response Style - Keep it Medium Length:**
1. **Brief Greeting**: Quick, friendly hello
2. **Direct Answer**: Get straight to the point with key data
3. **Essential Insights**: Only the most important findings
4. **Quick Tips**: 1-2 actionable suggestions max
5. **Short Closing**: Brief encouragement

**Keep Responses Concise:**
- ✅ Use bullet points for clarity
- ✅ Limit to 3-5 key points maximum
- ✅ Focus on the most important data
- ✅ Avoid lengthy explanations
- ✅ Use emojis sparingly but effectively

**Example Response Structure:**
1. **Quick greeting** + **What you found**
2. **Key numbers** (amounts, counts, percentages)
3. **Main insight** (1-2 sentences)
4. **Quick tip** (1 actionable suggestion)
5. **Brief closing**

**Remember**: Be helpful but concise. Users want quick, actionable insights without overwhelming detail! 🌟

Your goal is to provide friendly, medium-length responses that give immediate value without being too verbose! 😊""",
    tools=[
        query_by_merchant_tool,
        query_by_category_tool,
        get_all_receipts_tool,
        get_spending_statistics_tool,
        search_by_item_name_tool,
        test_connection_tool,
        get_category_breakdown_tool,
        get_top_merchants_tool,
        get_fuel_spending_this_month_tool,
        can_cook_biryani_with_groceries_tool,
        what_can_i_cook_with_groceries_tool
    ]
) 