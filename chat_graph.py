"""The small LangGraph backend. It does not know about Streamlit."""

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()  # Read OPENROUTER_API_KEY from the local .env file.


class ChatState(TypedDict):
    # LangGraph uses LangChain message objects while it is running.
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot(state: ChatState) -> dict:
    """Send the conversation to OpenRouter and return one assistant message."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Add OPENROUTER_API_KEY to your .env file first.")

    model = ChatOpenRouter(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        api_key=api_key,
    )
    system_message = SystemMessage(
        content="You are Cardinal, a helpful assistant for learning about agentic workflows."
    )
    answer = model.invoke([system_message, *state["messages"]])
    return {"messages": [AIMessage(content=str(answer.content))]}


# This first graph has only one step: START -> chatbot -> END.
builder = StateGraph(ChatState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()


def get_reply(chat_messages: list[dict]) -> str:
    """Convert simple JSON-style messages to LangChain messages, then run the graph."""
    messages_for_graph = []
    for message in chat_messages:
        if message["role"] == "user":
            messages_for_graph.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            messages_for_graph.append(AIMessage(content=message["content"]))

    result = graph.invoke({"messages": messages_for_graph})
    return str(result["messages"][-1].content)
