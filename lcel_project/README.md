# LangChain LCEL Pipeline Project

A production-ready LangChain LCEL (LangChain Expression Language) pipeline that decomposes complex questions, answers sub-questions in parallel, and synthesizes a final response.

## Project Structure

```
lcel_project/
├── .env                 # Environment variables (API keys)
├── main.py              # Entry point - orchestrates the pipeline
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── stages/
    ├── __init__.py     # Package initialization
    ├── decompose.py    # Stage 1: Breaks questions into sub-questions
    ├── answer.py       # Stage 2: Answers each sub-question in parallel
    └── combine.py      # Stage 3: Synthesizes final response
```

## Pipeline Stages

### 1. DECOMPOSE
- **Input**: Complex question
- **Process**: Uses Gemini 1.5 Flash LLM to break question into up to 3 numbered sub-questions
- **Output**: Numbered sub-questions

### 2. ANSWER
- **Input**: Each sub-question
- **Process**: Uses LLM to answer each sub-question in **parallel** via `.batch()`
- **Output**: Individual answers for each sub-question

### 3. COMBINE
- **Input**: Original question + all sub-question answers
- **Process**: Uses LLM to synthesize answers into a structured response
- **Output**: Final 3-line answer (Final Answer / Key Points / Confidence)

## Setup

### Prerequisites
- Python 3.9 or higher
- Google Generative AI API key

### Installation

1. **Clone/Navigate to the project directory**:
   ```bash
   cd lcel_project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**:
   - Edit `.env` and replace `your_google_api_key_here` with your actual Google Generative AI API key
   - Get your API key from: https://makersuite.google.com/app/apikey

   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the pipeline with:
```bash
python main.py
```

The pipeline will process two example questions and display:
- Stage 1 output: Decomposed sub-questions
- Stage 2 output: Individual answers (processed in parallel)
- Stage 3 output: Final synthesized response with 3 lines

### Custom Questions

To process your own questions, modify the `test_questions` list in `main.py`:

```python
test_questions = [
    "Your custom question here?",
    "Another question?",
]
```

Or use the `run_pipeline()` function programmatically:

```python
from main import run_pipeline

run_pipeline("What is artificial intelligence?")
```

## Key Features

- **Parallel Processing**: Uses LangChain's `.batch()` method for efficient parallel sub-question answering
- **LCEL Pipeline**: Built entirely with LangChain Expression Language for composability
- **Structured Output**: Final answer follows a consistent 3-line format
- **Error Handling**: API key validation at startup
- **Clean Architecture**: Modular stages that are easy to extend or replace

## Tech Stack

- **LangChain**: LCEL for composable pipelines
- **Google Generative AI**: Gemini 1.5 Flash model
- **Python 3.9+**: Modern Python features
- **python-dotenv**: Environment variable management

## Example Output

```
================================================================================
PROCESSING QUESTION: How does photosynthesis work?
================================================================================

[STAGE 1: DECOMPOSE]
Breaking down the question into sub-questions...
1. What is the basic mechanism of photosynthesis?
2. What are the light-dependent and light-independent reactions?
3. Why is photosynthesis important for ecosystems?

[STAGE 2: ANSWER]
Answering each sub-question in parallel...
...

[STAGE 3: COMBINE]
Synthesizing final answer...

--------------------------------------------------------------------------------
FINAL RESPONSE:
--------------------------------------------------------------------------------
1. Final Answer: Photosynthesis is a biological process where plants use sunlight...
2. Key Points: Involves chlorophyll, ATP production, glucose synthesis...
3. Confidence: High - this is fundamental biology well-established in science
================================================================================
```

## Extending the Pipeline

### Adding a new stage:
1. Create a new file in `stages/` (e.g., `validate.py`)
2. Define a chain function and export it
3. Import and use it in `main.py`

### Changing the model:
Edit the `ChatGoogleGenerativeAI` instantiations in each stage file and change the `model` parameter to another Gemini model (e.g., `"gemini-pro"`).

### Adjusting temperature:
Modify the `temperature` parameter in each stage:
- **Low (0.1-0.3)**: More deterministic, better for decomposition
- **Medium (0.5-0.7)**: Balanced, good for answering
- **High (0.8-1.0)**: More creative

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'langchain_google_genai'`
- **Solution**: Run `pip install -r requirements.txt` to install all dependencies

**Issue**: `ValueError: GOOGLE_API_KEY not found in .env file`
- **Solution**: Ensure `.env` file exists in the project root and contains your API key

**Issue**: `API key not valid` errors
- **Solution**: Verify your API key is correct and has been generated from https://makersuite.google.com/app/apikey

## License

MIT

## Support

For issues or questions about LangChain, visit: https://python.langchain.com/
