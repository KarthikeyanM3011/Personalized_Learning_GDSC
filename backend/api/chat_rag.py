from flask import Blueprint, request, jsonify
from uuid import uuid4
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import numpy as np
from huggingface_hub import InferenceClient

user_sessions = {}

chat_rag = Blueprint('chat_rag', __name__)

def initialize_index(num_features):
    return faiss.IndexFlatL2(num_features)

def generate_answer(user_question, context):
    client = InferenceClient(api_key="YOUR_HUGGINGFACE_API")
    prompt = f"""
    You are a knowledgeable assistant. Based on the following content, answer the question clearly and concisely.

    Context:
    {context}

    Question: {user_question}

    Provide only the answer. If necessary, include examples but avoid unnecessary information.
    """
    response = ''
    for message in client.chat_completion(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        stream=True,
    ):
        response += message.choices[0].delta.content
    return response

def vectorize_text(content, vectorizer):
    return vectorizer.transform([content]).toarray().astype(np.float32)

@chat_rag.route('/index', methods=['POST'])
def index_content():
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input format. Expected a list of objects with 'filename' and 'content'."}), 400

    session_key = str(uuid4())
    vectorizer = TfidfVectorizer()
    documents = [item.get('content') for item in data if item.get('filename') and item.get('content')]

    if len(documents) != len(data):
        return jsonify({"error": "Each item must have 'filename' and 'content'."}), 400

    vectorizer.fit(documents)
    num_features = len(vectorizer.get_feature_names_out())
    index = initialize_index(num_features)
    user_sessions[session_key] = {'vectorizer': vectorizer, 'index': index, 'documents': documents}
    document_vectors = vectorizer.transform(documents).toarray().astype(np.float32)
    index.add(document_vectors)

    return jsonify({"session_key": session_key})

@chat_rag.route('/chat', methods=['POST'])
def chat_with_rag():
    session_key = request.json.get('session_key')
    user_question = request.json.get('question')

    if not session_key or not user_question:
        return jsonify({"error": "Both 'session_key' and 'question' must be provided."}), 400

    if session_key not in user_sessions:
        return jsonify({"error": "Invalid session key."}), 400

    session_data = user_sessions[session_key]
    vectorizer = session_data['vectorizer']
    index = session_data['index']
    question_vector = vectorize_text(user_question, vectorizer)

    if question_vector.shape[1] != index.d:
        return jsonify({"error": "Mismatch between vector dimensions and index."}), 400

    D, I = index.search(question_vector, k=1)
    if I[0][0] == -1:
        return jsonify({"answer": "No relevant information found."}), 404

    most_similar_content = session_data['documents'][I[0][0]]
    answer = generate_answer(user_question, most_similar_content)
    
    return jsonify({"answer": answer})

@chat_rag.route('/close', methods=['POST'])
def close_session():
    session_key = request.json.get('session_key')
    if session_key in user_sessions:
        del user_sessions[session_key]
        return jsonify({"message": "Session closed successfully."})
    return jsonify({"error": "Invalid session key."}), 400
