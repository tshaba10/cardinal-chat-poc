# Cardinal Chat — learning version

This is intentionally small: two Python files and one `.env` file.

```text
You → app.py (the web page) → chat_graph.py (LangGraph + OpenRouter) → reply
```

## Run it

1. Open this folder in VS Code.
2. Open the VS Code terminal.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the libraries:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to a new file named `.env` and replace the placeholder with your OpenRouter key.
6. Start the chat:

   ```powershell
   streamlit run app.py
   ```

## The two files

### `app.py`: the visible chat page

This file makes the Streamlit page. It saves the conversation in `st.session_state`, displays existing messages, accepts a new message, then calls `get_reply(...)`.

### `chat_graph.py`: the chatbot brain

This file contains the simple LangGraph workflow:

```text
START → chatbot → END
```

The `chatbot` function sends the message history to an OpenRouter model. The default model setting is `openrouter/free`; change `OPENROUTER_MODEL` in `.env` if you later want a specific model.

## The conversation JSON

The sidebar shows the simple data saved by the app:

```json
{
  "conversation_id": "unique ID for this chat",
  "messages": [
    {
      "message_id": "unique ID for one message",
      "role": "user",
      "content": "Hello",
      "timestamp": "2026-09-15T15:30:00+00:00",
      "metadata": {}
    }
  ],
  "metadata": {}
}
```

This is ordinary Python dictionary data, so it can easily become JSON later. It is different from the LangGraph state: LangGraph temporarily uses `HumanMessage` and `AIMessage` objects because those are the message types the model library understands.

For now, do not add credit-card records, business rules, approvals, database storage, or multiple agents. First get comfortable changing the page title, system message, and graph flow.
