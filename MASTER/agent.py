import sys
sys.path.append(r"D:\Projects\ProjectRaseed")

from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()


from .Slaves.extraction_agent.agent import IamExtractorAgent


root_agent = Agent(
    name="Raseed_Agent",
    model="gemini-2.0-flash",
    description="Raseed_Agent",
    instruction="""
    - You are an exclusive Receipt agent
    - You help users to discover their bills and cost of living based on the city
    - You are responsible for delegating tasks to the following agents:
        - IamExtractorAgent: call this agent if user uploads any image or video; this will extract the data.
        - google_search_agent: call this agent when users ask about news or Google Wallet features; it will search and summarize the information.
    """,
    sub_agents=[IamExtractorAgent],
)