# AI Assistant with Tool Integration

![AI Assistant](https://img.shields.io/badge/AI-Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflow Visualization](#workflow-visualization)
- [Tools](#tools)

## Overview

This project implements an AI-powered assistant using OpenAI's GPT-4 model, integrated with various tools to enhance its capabilities. The assistant can perform web searches, calculate sums, and invoke a secondary AI agent for more complex tasks. The workflow is managed using a state graph, ensuring smooth transitions between different states and tool invocations.

## Features

- **AI-Powered Conversations:** Leverages OpenAI's GPT-4 model for intelligent and context-aware responses.
- **Tool Integration:**
  - **Web Search:** Perform searches using the Tavily API.
  - **Calculation:** Compute sums of numerical expressions.
  - **Secondary AI Agent:** Invoke an additional AI agent for specialized tasks.
- **Workflow Management:** Utilizes a state graph to manage conversation flow and tool usage.
- **Graph Visualization:** Generates visual representations of the workflow state graph using Graphviz.
- **Persistent Memory:** Saves conversation state between sessions using `MemorySaver`.

## Prerequisites

- Python 3.9 or higher
- API keys for OpenAI and Tavily

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/IvanFernande/Langgraph-Collection.git
cd ai-assistant
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Configuration

1. **Set up API Keys:**

- Create a file called api_keys.py in the root directory of the project.
- Add your OpenAI and Tavily API keys:

```python
OPENAI_API_KEY = "your_openai_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

2. **Global variables:**

The script sets global variables for the API keys. Make sure api_keys.py is set correctly as shown above.


## Usage

1. **Execute the script:**
```bash
python script.py
```

2. **Interact with the Assistant:**
- Upon launch, you will be prompted to enter your messages.
- The assistant will respond based on your input, using the built-in tools as needed.

```bash
Prompt: What is the date today?
(HUMAN)    → What is the date today?
(TOOL: search) → The current date and time is January 16, 2025, and the time is 19:08:29.
(AI MODEL) → Today's date is January 16, 2025.
```

3. **Finish the conversation:**
Press `Ctrl+C` to safely exit the chat cycle.

## Workflow Visualization
The assistant's workflow is managed by a status network. To visualise this workflow:

1. Graph generation:
   When running the script, a PNG image of the state graph will be generated (default name: `stategraph.png`).
2. Custom Name: You can change the name by modifying the call to the visualize_graph function in the script:
  ```python
    visualize_graph(workflow, filename=‘my_workflow’)
  ```
  This will save the graph as `my_workflow.png`.

## Tools
1. **Web Search(search):** Make web searches using the Tavily API.
- Usage:
```python
search("Your search query here")
```
- Example
```bash
Prompt: Find the latest on AI of today 16/01/2025
(HUMAN)    → Find the latest on AI of today 16/01/2025
(TOOL: search) → On January 16, 2025, the latest news on AI includes developments in Generative AI space, exciting AI advancements in automation, healthcare, and autonomous vehicles, Microsoft's $3 billion investment in India to boost AI and cloud services, Cognizant leading enterprises into the next generation of AI adoption with Neuro-R AI Multi-Agent Accelerator, and Thundercomm launching its latest innovations at CES 2025.
(AI MODEL) → On January 16, 2025, the latest developments in AI include:

1. **Generative AI Advancements**: Continued progress in the generative AI space, enhancing creativity and content creation.
2. **Automation and Healthcare**: Significant advancements in AI applications for automation and healthcare, improving efficiency and patient care.
3. **Microsoft's Investment**: Microsoft announced a $3 billion investment in India aimed at boosting AI and cloud services.
4. **Cognizant's AI Adoption**: Cognizant is leading enterprises into the next generation of AI adoption with its Neuro-R AI Multi-Agent Accelerator.
5. **Thundercomm Innovations**: Thundercomm launched its latest innovations at CES 2025, showcasing new AI technologies.

These highlights reflect the ongoing evolution and integration of AI across various sectors.
```

2. **Calculate Sum(calculate_sum):** Calculates the sum of two numbers given in a string.
- Usage:
```python
calculate_sum("15 27")
```
- Example
```bash
Prompt: What is the result of 2 plus 5?
(HUMAN)    → What is the result of 2 plus 5?
(TOOL: calculate_sum) → The sum of 2 and 5 is 7.
(AI MODEL) → The result of 2 plus 5 is 7.
```

3. **Invoke Secondary Agent (invoke_secondary_agent)** Invoke a secondary AI agent for specialised tasks.
- Usage:
```python
invoke_secondary_agent("Your prompt here")
```
- Example
```bash
Prompt: Explain the theory of relativity, using other agent to check the answer. I need the answer to be short
(HUMAN)    → Explain the theory of relativity, using other agent to check the answer. I need the answer to be short
(TOOL: invoke_secondary_agent) → The theory of relativity, developed by Albert Einstein, consists of two main parts: special relativity and general relativity.

1. **Special Relativity (1905)**: This theory addresses the physics of objects moving at constant speeds, particularly at speeds close to the speed of light. It introduces two key concepts:
   - The laws of physics are the same for all observers, regardless of their relative motion.
   - The speed of light in a vacuum is constant and does not change, regardless of the motion of the light source or observer. This leads to phenomena such as time dilation (time moving slower for fast-moving observers) and length contraction (objects appearing shorter in the direction of motion).

2. **General Relativity (1915)**: This theory extends the principles of special relativity to include acceleration and gravity. It describes gravity not as a force but as the curvature of spacetime caused by mass. Massive objects like planets and stars warp the fabric of spacetime, causing objects to follow curved paths. This explains phenomena such as the bending of light around massive objects and the precession of planetary orbits.

In summary, relativity fundamentally alters our understanding of space, time, and gravity, showing that they are interconnected and relative to the observer's motion.
(AI MODEL) → The theory of relativity, developed by Albert Einstein, consists of two main parts:

1. **Special Relativity (1905)**: This focuses on objects moving at constant speeds, particularly near the speed of light. It introduces two key ideas:
   - The laws of physics are the same for all observers, regardless of their relative motion.
   - The speed of light in a vacuum is constant, leading to effects like time dilation (time moves slower for fast-moving observers) and length contraction (objects appear shorter in the direction of motion).

2. **General Relativity (1915)**: This extends special relativity to include acceleration and gravity, describing gravity not as a force but as the curvature of spacetime caused by mass. Massive objects warp spacetime, causing other objects to follow curved paths, explaining phenomena like the bending of light around massive objects.

In essence, relativity changes our understanding of space, time, and gravity, showing they are interconnected and relative to the observer's motion.
```

---

Any improvements or contributions to this code would be greatly appreciated! I hope this project has helped you learn something new. For any questions, feel free to email me at: ivanfdezg@hotmail.com.
