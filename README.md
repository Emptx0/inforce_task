# Chat LLM API (FastAPI + SQLAlchemy)

A minimal chat backend with session tracking, token usage, and cost accounting.  
Designed to run **as Python modules from `src/`**.

---

## Features

- FastAPI REST API
- SQLite database
- Chat sessions + message history
- Token + cost tracking
- LLM calls

---

## ❗️ LLM Backend ❗️

This project uses **Gemma 3 (1B)** running **locally via Ollama**.

The LLM is accessed through a custom-written client that exposes an **OpenAI-style interface**, including:
- `chat(messages)` format
- role-based messages (`user`, `assistant`)
- structured `usage` metadata (token counting)

The LLM layer is designed using **OOP patterns (factory + base interface)**, which allows:
- easy replacement of models (Gemma, LLaMA, etc.)
- switching between local and remote providers
- minimal changes in business logic when adding new LLM backends

This approach keeps the system modular, extensible, and compatible with OpenAI-like APIs, without relying on external cloud services.


---

## Project Structure

```
.
├── chat.db
└── src
├── api
│   ├── main.py
│   └── routes
│       └── chat.py
├── db
│   ├── db.py
│   ├── init_db.py
│   └── models.py
├── llm
│   ├── base.py
│   ├── factory.py
│   └── ollama_client.py
├── schemas.py
└── config.py
````

---

## Install dependencies:

```bash
pip install -r requirements.txt
````

---

## Initialize Database (REQUIRED)

Before running the API, create the database:

```bash
python -m src.db.init_db
```

This will create `chat.db` and all tables.

---

## Run API

From the project root:

```bash
uvicorn src.api.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Create chat session

```
POST /sessions/
```

### Send message

```
POST /sessions/{session_id}/messages
```

### Get chat history

```
GET /sessions/{session_id}
```

---

## Token Accounting Logic

* **Message.tokens** - tokens used for THIS response only
* **ChatSession.total_tokens** - sum of all assistant tokens
* User messages have `tokens = 0`
* Cost is calculated per message and accumulated per session

---

## Example Usage with CLI
![Example output](examples/1.jpg)
\
\
Result in database: \
![Example db1](examples/2.jpg)
\
\
![Example db2](examples/3.jpg)