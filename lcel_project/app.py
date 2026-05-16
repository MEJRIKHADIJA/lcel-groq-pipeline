"""Flask app for the LCEL pipeline web interface."""
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables early
load_dotenv()

# Verify API key is set
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in .env file")

from stages import decompose_chain, answer_runnable, combine_chain

app = Flask(__name__)

# Build the pipeline
pipeline = decompose_chain | answer_runnable | combine_chain


@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/process", methods=["POST"])
def process_question():
    """API endpoint to process a question through the pipeline."""
    try:
        data = request.json
        question = data.get("question", "").strip()
        
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        # Run the pipeline
        result = pipeline.invoke({"question": question})
        
        return jsonify({
            "success": True,
            "result": result        # ← was result.content
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)