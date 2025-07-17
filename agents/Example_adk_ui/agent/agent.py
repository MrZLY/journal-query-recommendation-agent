import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Use model from environment or default to deepseek
model_type = os.getenv('MODEL', 'deepseek/deepseek-chat')

# Create model
model = LiteLlm(model=model_type)

# Create a simple agent without MCP tools
root_agent = Agent(
    name="chat_agent",
    model=model,
    instruction="你是一个友好的AI助手，可以帮助用户回答问题和进行对话。",
    tools=[]  # No tools for now
)