import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from typing import Any, Dict
import openai
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Use model from environment or default to deepseek
model_type = os.getenv('MODEL', 'deepseek/deepseek-chat')


# Simple echo tool for testing
@FunctionTool
def echo(message: str) -> str:
    """
    Echo back the message. This is a simple test tool.
    
    Args:
        message: The message to echo back
        
    Returns:
        The same message
    """
    return f"Echo: {message}"


@FunctionTool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: A mathematical expression to evaluate
        
    Returns:
        The result of the calculation
    """
    try:
        # Use eval safely for basic math operations
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "pow": pow,
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Create agent without MCP toolset
root_agent = Agent(
    name="simple_agent",
    model=LiteLlm(model=model_type),
    instruction="""You are an intelligent assistant. You can:
    1. Have conversations on various topics
    2. Use the echo tool to repeat messages
    3. Use the calculate tool to perform calculations
    
    Be helpful, concise, and friendly.""",
    tools=[echo, calculate]
)