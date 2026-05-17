"""
app.py - Main Flask Application for Edugator
Entry point for the backend server. Handles API routes and chat endpoints.
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from rag_pipeline import EduGatorRAG

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Initialize the RAG pipeline (loads documents, builds vector DB)
print("🚀 Initializing Edugator RAG Pipeline...")
rag = EduGatorRAG()
rag.initialize()
print("✅ Edugator is ready!")


@app.route("/")
def index():
    """Serve the main chat interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.
    Accepts a JSON body: { "message": "...", "history": [...] }
    Returns: { "response": "...", "sources": [...] }
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data.get("message", "").strip()
        chat_history = data.get("history", [])  # List of past messages

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Get answer from RAG pipeline
        result = rag.get_answer(user_message, chat_history)

        return jsonify({
            "response": result["answer"],
            "sources": result.get("sources", []),
            "status": "success"
        })

    except Exception as e:
        print(f"❌ Error in /api/chat: {e}")
        return jsonify({
            "error": "Something went wrong. Please try again.",
            "status": "error"
        }), 500


@app.route("/api/suggestions", methods=["GET"])
def suggestions():
    """Return suggested starter questions for the UI."""
    suggested = [
        "What should I choose after 10th grade – Science or Commerce?",
        "How do I prepare for JEE Main 2025?",
        "What are the career options after 12th Arts?",
        "Tell me about TNPSC Group 2 exam",
        "What skills do I need for an IT job?",
        "How to get into government jobs after graduation?",
        "What is the NEET exam and who can apply?",
        "How to prepare for UPSC Civil Services?",
        "What are polytechnic courses after 10th?",
        "Career options in teaching profession in India"
    ]
    return jsonify({"suggestions": suggested})


@app.route("/api/categories", methods=["GET"])
def categories():
    """Return topic categories for the category buttons in UI."""
    cats = [
        {"id": "after10", "label": "After 10th", "icon": "🎓", "color": "#4f46e5"},
        {"id": "after12", "label": "After 12th", "icon": "📚", "color": "#0891b2"},
        {"id": "career", "label": "Career Guide", "icon": "💼", "color": "#059669"},
        {"id": "exams", "label": "Exams", "icon": "📝", "color": "#d97706"},
        {"id": "govt", "label": "Govt Jobs", "icon": "🏛️", "color": "#7c3aed"},
        {"id": "skills", "label": "Skills & Tech", "icon": "💻", "color": "#db2777"},
    ]
    return jsonify({"categories": cats})


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Edugator is running!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
