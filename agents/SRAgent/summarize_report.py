import os
import Nexusagent_SR
import asyncio

# import debugpy
# debugpy.listen(("0.0.0.0", 5678))
# print("🔍 Waiting for debugger to attach...")

from Nexusagent_SR.tool.summarize_report import summarize_report
from Nexusagent_SR.tool.agent_tool import get_iteration_history_tool



H = asyncio.run(summarize_report())
print(H)

history = get_iteration_history_tool()
print(history)