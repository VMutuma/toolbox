import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import litellm
from dotenv import load_dotenv

load_dotenv()

# Set API Keys
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

litellm.api_key = gemini_api_key

search_tool = SerperDevTool()

def gemini_completion(prompt):
    response = litellm.completion(
        model="gemini/gemini-pro",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response["choices"][0]["message"]["content"] if "choices" in response else "No response"

lead_analyzer = Agent(
    role="Lead Analyst",
    goal="Analyze incoming leads and provide detailed insights.",
    backstory="You are an experienced analyst specializing in lead assessment.",
    tools=[search_tool],
    allow_delegation=True,
    llm="gemini/gemini-pro" 
)

comms_agent = Agent(
    role="Email Writer",
    goal="Write personalized emails to leads to schedule a meeting.",
    backstory="You are an expert copywriter skilled in persuasive communication.",
    llm="gemini/gemini-pro" 
)

lead_analysis = Task(
    description="Analyze and provide a full report on the given lead, including company insights.",
    expected_output="Detailed lead profile and company insights.",
    agent=lead_analyzer,
    async_execution=False
)

email_task = Task(
    description="Write a compelling, personalized email for the given lead to secure a meeting.",
    expected_output="Well-structured, engaging email to the lead.",
    agent=comms_agent,
    async_execution=False
)

lead_comms = Crew(
    agents=[lead_analyzer, comms_agent],
    tasks=[lead_analysis, email_task],
    verbose=True
)

lead_info = {"lead": "Taha", "company": "Beem"}

result = lead_comms.kickoff(inputs=lead_info)
print("\nFinal Output:\n", result)
