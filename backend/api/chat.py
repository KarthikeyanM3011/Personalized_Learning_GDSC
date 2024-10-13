from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient

chatbot_blueprint = Blueprint('chatbot', __name__)

def generate_chat_response(history, current_question):
    try:
        client = InferenceClient(api_key="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")
        prompt = f"""
        You are a knowledgeable teacher and professor. Please provide a clear and concise answer to the following question based on the given conversation history.

        Conversation History:
        {history}
        
        Current Question:
        {current_question}
        
        Respond only with the answer. If an example is necessary for clarification, provide it without any extra commentary.
        """

        response = ''
        for message in client.chat_completion(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=True,
        ):
            response += message.choices[0].delta.content

        return response, None
    except Exception as e:
        return None, str(e)

@chatbot_blueprint.route('/chatbot/ask', methods=['POST'])
def ask_chatbot():
    data = request.json
    current_question = data.get("current_question")
    history = data.get("history", [])

    if current_question is None:
        return jsonify({"error": "Current question must be provided."}), 400

    history_string = "\n".join(history)
    response, error = generate_chat_response(history_string, current_question)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"response": response})

