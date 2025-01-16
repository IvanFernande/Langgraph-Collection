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
- [Contributing](#contributing)
- [License](#license)

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
