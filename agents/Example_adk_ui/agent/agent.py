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

def calculator(operator: str, a: int, b: int) -> int:
    """
    计算器工具
    input: operator, a, b
    operator: +, -, *
    a, b: int
    output: int
    """
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    else:
        return "Invalid operator"

root_agent = Agent(
    name="chat_agent",
    model=model,
    instruction="你是一个友好的AI助手，可以帮助用户回答问题和进行对话, 使用calculator工具进行计算。",
    tools=[calculator]  # No tools for now
)