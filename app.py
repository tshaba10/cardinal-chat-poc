"""The small Streamlit page. Run: streamlit run app.py"""

from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st

from chat_graph import get_reply


def make_message(role: str, content: str) -> dict:
    """Make one plain-Python message that can later become JSON."""
    return {
        "message_id": str(uuid4()),
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": {},
    }


st.set_page_config(page_title="Cardinal Chat", page_icon="💳")
st.title("💳 Cardinal Chat")
st.caption("A small learning project using Streamlit, LangGraph, and OpenRouter.")

# Streamlit runs this file again after every click or submitted message.
# session_state is how we remember this chat between those reruns.
if "conversation" not in st.session_state:
    st.session_state.conversation = {
        "conversation_id": str(uuid4()),
        "messages": [],
        "metadata": {},
    }

conversation = st.session_state.conversation

with st.sidebar:
    st.subheader("Conversation JSON")
    st.json(conversation)
    if st.button("New chat"):
        st.session_state.conversation = {
            "conversation_id": str(uuid4()),
            "messages": [],
            "metadata": {},
        }
        st.rerun()

# Show messages already saved in this conversation.
for message in conversation["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Wait for the user to type and submit a message.
if prompt := st.chat_input("Type a message..."):
    conversation["messages"].append(make_message("user", prompt))

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = get_reply(conversation["messages"])
            except Exception as error:
                st.error(f"The request did not work: {error}")
            else:
                st.write(reply)
                conversation["messages"].append(make_message("assistant", reply))
