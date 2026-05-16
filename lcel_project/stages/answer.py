"""Answer stage: answers each sub-question in parallel."""
import os
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq


# Create the prompt template
answer_prompt = PromptTemplate(
    template="""Answer the following sub-question concisely.

Sub-question: {subq}

Provide your response in this exact format:
Answer: <one-line answer>
Steps:
- <step1>
- <step2>""",
    input_variables=["subq"]
)


import os
model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm = ChatGroq(model=model_name, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# Create the answer chain
answer_chain = answer_prompt | llm


def parse_answer_output(response):
    """Parse answer output into structured format."""
    try:
        text = response.content
        
        # Extract answer line
        answer_match = re.search(r"Answer:\s*(.+?)(?=\nSteps:|$)", text, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else ""
        
        # Extract steps
        steps_match = re.search(r"Steps:\s*((?:- .+?\n?)+)", text, re.DOTALL)
        steps = []
        if steps_match:
            steps_text = steps_match.group(1)
            steps = [s.strip() for s in re.findall(r"- (.+?)(?=\n|$)", steps_text)]
        
        return {
            "answer": answer,
            "steps": steps
        }
    except Exception:
        # Fallback if parsing fails
        return {
            "answer": response.content,
            "steps": ["(no steps parsed)"]
        }


def run_answers(subquestions: list):
    """Answer multiple sub-questions in parallel."""
    # Build inputs for batch processing
    inputs = [{"subq": q} for q in subquestions]
    
    # Call answer_chain.batch() for parallel processing
    responses = answer_chain.batch(inputs)
    
    # Parse each response
    results = [parse_answer_output(resp) for resp in responses]
    
    return results


# Export the runnable
answer_runnable = RunnableLambda(run_answers)
