from typing import Annotated, Literal, TypedDict
import os
from api_keys import OPENAI_API_KEY, TAVILY_API_KEY
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from graphviz import Digraph

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

def visualize_graph(workflow: StateGraph, filename: str = "stategraph"):
    """
    Visualizes the workflow state graph using Graphviz.

    Args:
        workflow (StateGraph): The state graph representing the workflow.
        filename (str): The name of the output PNG file.
    """
    dot = Digraph(comment="StateGraph")
    
    for node in workflow.nodes:
        dot.node(node, node)
    
    for edge in workflow.edges:
        dot.edge(edge[0], edge[1])

    dot.render(filename, format="png", cleanup=True)
    print(f"Graph saved as {filename}.png")

@tool
def search(query: str):
    """
    Performs a web search using the Tavily API.

    Args:
        query (str): The search query string.

    Returns:
        str: The search results obtained from the Tavily API.
    """
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    answer = tavily_client.qna_search(query=query)
    return answer

@tool
def calculate_sum(expression: str):
    """
    Calculates the sum of two numbers provided in a string.

    Args:
        expression (str): A string containing two numbers separated by spaces.

    Returns:
        str: The result of the sum or an error message if input is invalid.
    """
    try:
        numbers = [int(x) for x in expression.split() if x.isdigit()]
        if len(numbers) == 2:
            # Calculate and return the sum if exactly two numbers are found
            return f"The sum of {numbers[0]} and {numbers[1]} is {sum(numbers)}."
        else:
            # Return an error message if the number of inputs is incorrect
            return "I need exactly two numbers to calculate the sum."
    except Exception as e:
        # Handle any exceptions and return an error message
        return f"Error calculating sum: {str(e)}"


# Initialize the secondary AI agent with specified model and temperature
secondary_agent = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

@tool
def invoke_secondary_agent(prompt: str) -> str:
    """
    Invokes the secondary AI agent with the provided prompt and returns its response.

    Args:
        prompt (str): The input prompt to send to the secondary agent.

    Returns:
        str: The response from the secondary agent or an error message if invocation fails.
    """
    try:
        # Create a HumanMessage with the given prompt
        human_message = HumanMessage(content=prompt)
        # Invoke the secondary agent with the message
        response = secondary_agent.invoke([human_message])
        # Check if the response is an AIMessage and return its content
        if response and isinstance(response, AIMessage):
            return response.content.strip()
        else:
            return "The secondary agent did not respond correctly."
    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error invoking the secondary agent: {str(e)}"


# List of tool functions to be used by the agent
tools = [search, calculate_sum, invoke_secondary_agent]

# Initialize a ToolNode with the defined tools
tool_node = ToolNode(tools)

# Initialize the primary ChatOpenAI model and bind the tools to it
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5).bind_tools(tools)

# Define the system message that provides initial instructions to the AI assistant
system_message = SystemMessage(
    content=(
        "You are an AI assistant, and you have to answer as truthfully as possible. "
        "To do this, you have a number of tools, one of which is an LLM model to corroborate your information. " 
        "In addition, with the other tools you will always try to answer as accurately as possible."
    )
)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    """
    Determines whether the workflow should continue to the tools node or end.

    Args:
        state (MessagesState): The current state of messages in the workflow.

    Returns:
        Literal["tools", END]: Indicates whether to proceed to the tools node or end the workflow.
    """
    messages = state['messages']
    last_message = messages[-1]
    # If the last message includes tool calls, proceed to the tools node
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # Otherwise, end the workflow and respond to the user
    return END

def call_model(state: MessagesState):
    """
    Invokes the primary AI model with the current messages.

    Args:
        state (MessagesState): The current state of messages in the workflow.

    Returns:
        dict: A dictionary containing the new messages generated by the model.
    """
    messages = state['messages']
    # Prepend the system message if it's not already present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [system_message] + messages
    # Invoke the model with the updated messages
    response = model.invoke(messages)
    # Return the response as a list of messages
    return {"messages": [response]}

# Initialize the state graph for managing workflow
workflow = StateGraph(MessagesState)

# Add nodes to the workflow graph
workflow.add_node("agent", call_model)  # Node for the primary AI agent
workflow.add_node("tools", tool_node)   # Node for tool invocations

# Define the starting point of the workflow
workflow.add_edge(START, "agent")

# Add conditional edges based on the should_continue function
workflow.add_conditional_edges(
    "agent",
    should_continue,
)

# Define the transition from tools back to the agent
workflow.add_edge("tools", 'agent')

# Initialize memory saver to persist state between workflow executions
checkpointer = MemorySaver()

# Compile the workflow into a runnable application
app = workflow.compile(checkpointer=checkpointer)

# Visualize the workflow graph and save it as a PNG file
visualize_graph(workflow)


# Start the interactive conversation loop
while True:
    try:
        # Prompt the user for input
        human_message = input('Prompt: ')
        # Create a HumanMessage object with the user's input
        new_message = HumanMessage(content=human_message)

        # Invoke the workflow with the new message and a thread ID for context
        final_state = app.invoke(
            {"messages": [new_message]},
            config={"configurable": {"thread_id": 42}}
        )

        # Iterate through the messages in the final state to display responses
        for msg in final_state['messages']:
            # Get the class name of the message to determine its type
            msg_class = msg.__class__.__name__
            # Extract and clean the content of the message
            content = getattr(msg, "content", "").strip()
            
            # Skip empty messages
            if not content:
                continue
            
            # Display messages based on their type
            if msg_class == "HumanMessage":
                print(f"(HUMAN)    → {content}")
            elif msg_class == "AIMessage":
                print(f"(AI MODEL) → {content}")
            elif msg_class == "ToolMessage":
                # Get the tool name, defaulting to "Unknown Tool" if not available
                tool_name = getattr(msg, "name", "Unknown Tool")
                print(f"(TOOL: {tool_name}) → {content}")
            else:
                print(f"(UNKNOWN)  → {content}")
    except KeyboardInterrupt:
        # Handle user interrupt (Ctrl+C) gracefully
        print("\nConversation terminated by the user.")
        break
    except Exception as e:
        # Handle any unexpected exceptions and notify the user
        print(f"An error occurred: {str(e)}")