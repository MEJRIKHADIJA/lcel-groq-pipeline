"""Decompose stage: breaks complex questions into sub-questions."""
import os
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq


# Create the prompt template
decompose_prompt = PromptTemplate(
    template="""You are an expert at breaking down complex questions into simpler sub-questions.

Question: {question}

Break this question down into up to 3 numbered sub-questions that together would help answer the original question.
Return ONLY a numbered list, nothing else:
1. [First sub-question]
2. [Second sub-question]
3. [Third sub-question]""",
    input_variables=["question"]
)

# Create the model using GROQ_MODEL env var (fallback to llama3-8b-8192)

model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm = ChatGroq(model=model_name, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# Create the decomposer chain
decomposer = decompose_prompt | llm


# Create a RunnableLambda to parse the output
def parse_subquestions(response):
    """Parse LLM output to extract numbered sub-questions."""
    text = response.content
    
    # Match lines starting with 1., 2., 3., etc.
    matches = re.findall(r"^\d+\.\s+(.+)$", text, re.MULTILINE)
    
    return matches


parse_runnable = RunnableLambda(parse_subquestions)

# Export the complete chain
decompose_chain = decomposer | parse_runnable
