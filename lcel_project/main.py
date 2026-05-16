"""Main entry point for the LCEL pipeline."""
import os
from dotenv import load_dotenv

# Load environment variables from .env early so stage modules can read them
load_dotenv()

from stages import decompose_chain, answer_runnable, combine_chain

# Verify API key is set (Groq)
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in .env file")


# Build the complete LCEL pipeline
pipeline = decompose_chain | answer_runnable | combine_chain


def main():
    """Main function."""
    question = "How can I reduce latency in a web app that serves ML predictions?"
    
    print("\n" + "=" * 80)
    print(f"QUESTION: {question}")
    print("=" * 80 + "\n")
    
    try:
        # Run the pipeline
        result = pipeline.invoke({"question": question})
        
        # Print the result
        print(result)          # ← was result.content
        print("\n" + "=" * 80 + "\n")
    except Exception as e:
        print(f"\n❌ Error running pipeline: {e}")
        print(f"Error type: {type(e).__name__}")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    main()