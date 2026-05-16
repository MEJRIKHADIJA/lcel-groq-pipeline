# LCEL Groq Pipeline

A multi-stage NLP pipeline built with LangChain LCEL and Groq .
Includes a Flask web interface.

## How it works
1. **Decompose** — breaks a complex question into 3 sub-questions
2. **Answer** — answers each sub-question in parallel
3. **Combine** — synthesizes a final 3-line response

## Where LCEL pipes were used
Each stage is connected using the `|` operator, creating a `RunnableSequence`:
```python
pipeline = decompose_chain | answer_runnable | combine_chain
```
Inside each stage: `prompt | llm | parser` — output of one component flows automatically into the next.

## Why batch helps
In Stage 2, `.batch()` sends all 3 sub-questions to the LLM simultaneously instead of one by one. This runs them in parallel, cutting response time significantly.

## Setup
1. Clone the repo
2. Copy `.env.example` to `.env` and add your `GROQ_API_KEY`
3. Run `pip install -r requirements.txt`
4. Run `python app.py`
