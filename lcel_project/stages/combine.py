"""Combine stage: synthesizes answers into a final response."""
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


def format_answers(answer_dicts: list):
    """Format list of answer dicts into plain-text block."""
    formatted_lines = []
    
    for i, answer_dict in enumerate(answer_dicts, 1):
        formatted_lines.append(f"Sub-question {i}:")
        formatted_lines.append(f"  Answer: {answer_dict.get('answer', '')}")
        
        steps = answer_dict.get('steps', [])
        if steps:
            formatted_lines.append("  Steps:")
            for step in steps:
                formatted_lines.append(f"    - {step}")
        
        formatted_lines.append("")
    
    return {"subanswers_text": "\n".join(formatted_lines)}


# Create the format runnable
format_runnable = RunnableLambda(format_answers)

# Create the combine prompt template
combine_prompt = PromptTemplate(
    template="""You are an expert at synthesizing information.

Sub-question Answers:
{subanswers_text}

Based on the sub-question answers above, provide a response in exactly 3 lines with this format:
1) Final Answer: <one line summary>
2) Key points: - <point1>; - <point2>
3) Confidence: <low/medium/high>""",
    input_variables=["subanswers_text"]
)

model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm = ChatGroq(model=model_name, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# Create the complete chain
combine_chain = format_runnable | combine_prompt | llm | StrOutputParser()