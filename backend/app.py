from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from information_agent import run_vector_information_agent
from legal_assistant import initialize_rag_system, create_legal_assistant_chain
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global state for RAG system
rag_chain = None
topics_cache = None

def initialize_rag():
    """Initialize the RAG system on startup"""
    global rag_chain
    try:
        retriever = initialize_rag_system()
        rag_chain = create_legal_assistant_chain(retriever)
        print("✅ RAG System initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing RAG System: {e}")

def load_topics():
    """Load or generate topics from legal documents"""
    global topics_cache
    
    topics_file = "topics_cache.json"
    
    # Check if cache exists
    if os.path.exists(topics_file):
        try:
            with open(topics_file, 'r') as f:
                topics_cache = json.load(f)
                print(f"✅ Loaded {len(topics_cache)} topics from cache")
                return topics_cache
        except Exception as e:
            print(f"Warning: Could not load cache - {e}")
    
    # Generate topics if no cache
    print("🔄 Generating topics from legal documents...")
    topics_cache = generate_topics()
    
    # Save to cache
    try:
        with open(topics_file, 'w') as f:
            json.dump(topics_cache, f, indent=2)
        print("✅ Topics cached for future use")
    except Exception as e:
        print(f"Warning: Could not save cache - {e}")
    
    return topics_cache

def generate_topics():
    """Generate topics using the information agent"""
    try:
        # Call the information agent which now returns a list of dictionaries
        results = run_vector_information_agent()
        
        if not results or not isinstance(results, list):
            print("Warning: Information agent returned no results")
            return []
        
        print(f"✅ Generated {len(results)} topics from information agent")
        return results
    except Exception as e:
        print(f"Error generating topics: {e}")
        import traceback
        traceback.print_exc()
        return []

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Fetch all topics"""
    try:
        if topics_cache is None:
            load_topics()
        
        return jsonify(topics_cache if topics_cache else []), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/topic/<topic_id>', methods=['GET'])
def get_topic(topic_id):
    """Fetch a specific topic by ID"""
    try:
        if topics_cache is None:
            load_topics()
        
        topic = next((t for t in topics_cache if t["_id"] == topic_id), None)
        if not topic:
            return jsonify({"error": "Topic not found"}), 404
        
        return jsonify(topic), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to the legal assistant"""
    try:
        if rag_chain is None:
            return jsonify({"error": "RAG system not initialized"}), 500
        
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data["message"]
        
        # Get response from RAG chain
        response = rag_chain.invoke({"input": user_message})
        
        return jsonify({
            "reply": response.get("answer", "I couldn't process your question."),
            "success": True
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "rag_initialized": rag_chain is not None,
        "topics_loaded": topics_cache is not None
    }), 200

if __name__ == '__main__':
    # Initialize RAG system on startup
    initialize_rag()
    
    # Load topics on startup
    load_topics()
    
    # Start the Flask app on port 5001 (5000 is often used by AirPlay on macOS)
    app.run(debug=True, port=5001, host='0.0.0.0')
