import os
import sys


import Nexusagent_SR
from Nexusagent_SR.tool.pysr_config import set_unary_operators
from Nexusagent_SR.tool.pysr_config import set_binary_operators

unary_operators = ["exp", "square", "tanh"]
binary_operators = ["+", "-", "*", "/"]

set_unary_operators(unary_operators)
set_binary_operators(binary_operators)

import asyncio

from Nexusagent_SR.tool.pysr import run_symbolic_pysr

# Get data file path from command line arguments or use default
if len(sys.argv) > 1:
    data_path = sys.argv[1]
else:
    data_path = "data/hr_example.csv"

asyncio.run(run_symbolic_pysr(data_path))