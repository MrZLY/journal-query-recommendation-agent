import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from typing import Any, Dict
import openai
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Use model from environment or default to deepseek
# model_type = os.getenv('MODEL', 'deepseek/deepseek-chat')


use_model = "siliconflow"  # 您可以在 "deepseek", "siliconflow", "gpt-4o" 之间切换

if use_model == "deepseek":
    model = LiteLlm(model="deepseek/deepseek-chat")
elif use_model == "siliconflow":
    # 硅基流动使用 OpenAI 兼容接口
    model = LiteLlm(
        model="openai/deepseek-ai/DeepSeek-V3.2-Exp",  # 建议使用 V2
        api_base="https://api.siliconflow.cn/v1",
        api_key=os.environ.get('SILICONFLOW_API_KEY')
    )
elif use_model == "gpt-4o":
    # 确保已设置 AZURE_OPENAI_* 环境变量
    model = LiteLlm(model="azure/gpt-4o")
else:
    # 默认模型
    model = LiteLlm(model="deepseek/deepseek-chat")


toolset = MCPToolset(
    connection_params=SseServerParams(
        url="http://localhost:50001/sse",
    ),
)

# Create agent
root_agent = Agent(
    name="mcp_sse_agent",
    model=model,
    instruction='''You are an intelligent assistant capable of using external tools via MCP.准确讲，你是一个专业的学术期刊智能助手，能够根据用户输入自动判断任务类型并执行相应操作：

📌 任务类型一：期刊查询
触发条件：用户输入一个或多个期刊名称（如 “Nature”, “Advanced Materials” 等）。
响应要求：为每个期刊提供以下信息（尽可能完整）：

最新影响因子（Impact Factor, IF）
中科院期刊分区（大类/小类，如“工程技术 1区”）
JCR 分区（Q1/Q2/Q3/Q4）
期刊定位（如“综合性顶刊”、“专注纳米材料”等）
目标受众（如“材料科学家、化学家、工程师”）
期刊特色（如“审稿快”、“偏好高创新性工作”、“接收综述”等）
学术界评价（简要总结风评，如“声誉极高但拒稿率高”）
📌 任务类型二：期刊推荐
触发条件：用户输入一段文章摘要、研究课题描述、关键词或研究方向（如“我做的是钙钛矿太阳能电池的界面工程”）。
响应要求：

智能分析用户研究内容的核心领域、技术方向和创新点。
推荐 5–8 个合适期刊，按综合匹配度与影响力从高到低排序。
对每个推荐期刊，提供以下信息：
期刊名称
最新影响因子（IF）
中科院分区 & JCR 分区
是否为开放获取（OA）：
若是 OA，注明文章处理费（APC，单位：美元或人民币）
若混合 OA，注明可选及费用
主要收录内容/聚焦领域（如“专注于能源材料与器件”）
期刊特点（如“审稿周期约3周”、“偏好实验+理论结合”）
优缺点（如“IF高但版面费贵”、“接收率低但认可度高”）
学术风评（如“业内口碑好，但对数据完整性要求极高”）
💡 注意：优先推荐与用户研究高度匹配的期刊，而非单纯追求高 IF。若用户研究偏应用或交叉学科，应兼顾专业性和发表可行性。 

🛠️ 工具调用说明
你可调用外部工具（如 web_search、search_papers等等）获取最新、准确的数据''',
    tools=[toolset]
)
