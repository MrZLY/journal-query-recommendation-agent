import os
from Nexusagent_SR.tool.deepresearch import deepresearch_agent
import asyncio

import Nexusagent_SR

query = """
I am working on a network dynamics inference task for a networked biophysical neuron system.

The dataset describes the dynamics of a target neuron embedded in a network, where:
	•	x₁ represents the membrane potential of the target neuron,
	•	x₂ is a fast activation variable (e.g., reflecting fast ion-channel gating),
	•	x₃ is a slow adaptation variable (e.g., capturing slow potassium or calcium currents).

In addition, the dataset includes the membrane potentials of other neurons in the network, denoted as x₄, x₅, ..., x_N.
Each of these neurons may influence the target neuron through pairwise interactions.

⸻

🔬 Research Objective

The goal is to discover the governing equation for the membrane potential dynamics of the target neuron:

y = \frac{dx₁}{dt} = f(x₁, x₂, x₃) + \sum_{j \ne 1} g(x₁, x_j)

Where:
	•	f(x₁, x₂, x₃) captures the intrinsic dynamics of the target neuron,
	•	g(x₁, xⱼ) models the interaction effect from neuron j to neuron 1.

There is no magnetic flux modulation involved in this system.

"""

response = asyncio.run(deepresearch_agent(query))
print(response)