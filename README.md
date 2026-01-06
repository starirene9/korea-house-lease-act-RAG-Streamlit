# 🏢 Housing Lease Protection Act RAG Chatbot (Streamlit)

A **Retrieval-Augmented Generation (RAG)** chatbot built with **Streamlit, LangChain, Pinecone, and OpenAI**, designed to answer questions strictly grounded in the **Korean Housing Lease Protection Act (주택임대차보호법)**.

This project emphasizes **source-first legal answers**: every response is generated only after retrieving relevant statutory provisions and is written in a concise, legally structured format.

---

## Key Features

- **Legal RAG pipeline**  
  Retrieves relevant clauses of the Housing Lease Protection Act and generates answers based only on those clauses.

- **Few-shot answer control**  
  Uses curated examples to enforce a consistent legal answer style.

- **Query normalization (Dictionary Chain)**  
  Converts informal user expressions into official legal terminology before retrieval.  
  Examples:
  - `house / apartment / jeonse` → `housing`
  - `landlord` → `lessor`
  - `tenant` → `lessee`

- **History-aware retrieval**  
  Reformulates follow-up questions into standalone queries using chat history.

- **Concise legal answers**  
  Answers are limited to **2–3 sentences** for clarity and precision.

- **Legal basis-first format**  
  Every answer starts with:  
  `According to Article ○ of the Housing Lease Protection Act, ...`

---

## Tech Stack

- **Frontend**: Streamlit  
- **LLM**: OpenAI Chat Models (via `langchain-openai`)  
- **Embeddings**: OpenAI `text-embedding-3-large`  
- **Vector Database**: Pinecone  
- **RAG Orchestration**: LangChain  
  - History-aware retriever  
  - Retrieval chain  
  - Message history management  

---

## Architecture Overview

1. **User submits a question**
2. **Dictionary Chain** normalizes informal language into legal terminology
3. **History-aware retriever** rewrites the question as a standalone query (if needed)
4. **Pinecone retriever** fetches the top-k relevant law sections
5. **LLM** generates a short answer grounded strictly in retrieved context
6. The answer is returned with a **statutory citation-first format**

---

## Project Structure (Example)

```txt
.
├─ app.py                  # Streamlit UI
├─ llm.py                  # RAG pipeline and dictionary chain
├─ config.py               # Few-shot answer examples
├─ requirements.txt
└─ .env                    # Environment variables (not committed)
