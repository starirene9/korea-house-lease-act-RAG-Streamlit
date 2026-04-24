# Housing Lease Protection Act RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot specialized for Q&A on Korea's **Housing Lease Protection Act (주택임대차보호법)**.  
Built with `Streamlit + LangChain + OpenAI + Pinecone`, it generates answers grounded in retrieved legal text rather than model-only memory.

---

## Project Goal

This project is designed to prioritize **retrieved statutory evidence** over unsupported model guesses.

- Deliver reliable, law-focused answers for lease-related questions
- Minimize hallucinations by constraining responses to retrieved context
- Keep outputs concise and consistent in a legal response format

---

## Key Features

- **Legal RAG pipeline**: retrieve relevant provisions and generate evidence-grounded responses
- **Query normalization (Dictionary Chain)**: map informal terms to official legal terminology
- **History-aware question rewriting**: convert follow-up questions into standalone queries
- **Few-shot response control**: enforce a statute-first legal answer style
- **Concise outputs**: responses are intentionally short (typically 2-3 sentences)

---

## Tech Stack

- **UI**: Streamlit
- **LLM**: OpenAI chat models (`langchain-openai`)
- **Embeddings**: OpenAI `text-embedding-3-large`
- **Vector Database**: Pinecone
- **Orchestration**: LangChain (retriever, retrieval chain, message history)

---

## How It Works

1. A user submits a legal question in the chat UI.
2. The Dictionary Chain normalizes wording into legal terminology.
3. A history-aware retriever rewrites the query (if needed) using chat context.
4. Relevant legal chunks are retrieved from Pinecone (`top-k`).
5. The LLM generates a final response grounded in retrieved context.

---

## Project Structure

- `chat.py`: Streamlit chat UI entry point
- `llm.py`: RAG pipeline, retriever setup, history management, response generation
- `config.py`: few-shot examples used to control answer style
- `requirements.txt`: project dependencies
- `documents/`: source/legal document assets

---

## Quick Start

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

> The current code uses the Pinecone index name `tax-markdown-index`.

### 4) Run the app

```bash
source .venv/bin/activate
streamlit run chat.py
```

Open `http://localhost:8501` in your browser.

---

## Security Notes (Important)

- Never commit `.env` files containing API keys or secrets.
- The following are already excluded via `.gitignore`:
  - `.env`
  - `.venv/`
  - `.streamlit/secrets.toml`
- Always check `git status` before every commit/push.

---

## Potential Improvements

- Improve retrieval precision with better metadata/index design
- Strengthen citation formatting for statutory references
- Persist chat history in Redis/DB for multi-session use
- Add regression tests for prompts and chain behavior
