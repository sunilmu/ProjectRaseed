from google.adk.agents import Agent

def create_budget_plan(budget_amount: str, city: str = "General") -> dict:
    """
    Create a comprehensive budget plan for the given amount and city.
    """
    try:
        total_budget = float(budget_amount)
        
        # Simple budget breakdown
        budget_breakdown = {
            "Housing (Rent/Mortgage)": {"percentage": 30, "amount": total_budget * 0.30},
            "Food & Groceries": {"percentage": 15, "amount": total_budget * 0.15},
            "Transportation": {"percentage": 10, "amount": total_budget * 0.10},
            "Utilities": {"percentage": 8, "amount": total_budget * 0.08},
            "Healthcare": {"percentage": 8, "amount": total_budget * 0.08},
            "Entertainment": {"percentage": 5, "amount": total_budget * 0.05},
            "Savings": {"percentage": 10, "amount": total_budget * 0.10},
            "Miscellaneous": {"percentage": 14, "amount": total_budget * 0.14}
        }
        
        return {
            "status": "success",
            "total_budget": total_budget,
            "city": city,
            "budget_breakdown": budget_breakdown
        }
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def get_savings_tips(category: str) -> dict:
    """
    Get money-saving tips for a specific budget category.
    """
    tips = {
        "Housing": ["Share accommodation", "Negotiate rent", "Look for cheaper areas"],
        "Food": ["Cook at home", "Buy in bulk", "Use local markets"],
        "Transportation": ["Use public transport", "Carpool", "Walk when possible"]
    }
    
    return {
        "status": "success",
        "category": category,
        "tips": tips.get(category, ["Track spending", "Set goals", "Review regularly"])
    }

# Create the analysis agent
root_agent = Agent(
    name="budget_analysis_agent",
    model="gemini-2.0-flash",
    description="Analyze budgets and suggest spending plans",
    instruction="""
    You are a financial planning expert that helps users create budget plans.
    
    When a user provides a budget amount:
    1. Call `create_budget_plan` with the budget amount and city (if provided)
    2. Present a budget breakdown with categories like Housing, Food, Transportation, etc.
    3. Provide helpful tips and recommendations
    
    When users ask for savings tips, call `get_savings_tips` with the specific category.
    
    Format your response like this:
    💰 **Budget Analysis for [Amount]**
    📍 **City**: [City]
    
    📊 **Budget Breakdown**:
    🏠 **Housing**: ₹[Amount] ([Percentage]%)
    🍽️ **Food**: ₹[Amount] ([Percentage]%)
    🚗 **Transportation**: ₹[Amount] ([Percentage]%)
    ⚡ **Utilities**: ₹[Amount] ([Percentage]%)
    💰 **Savings**: ₹[Amount] ([Percentage]%)
    
    💡 **Tips**: [Provide relevant tips]
    """,
    tools=[create_budget_plan, get_savings_tips]
)

 