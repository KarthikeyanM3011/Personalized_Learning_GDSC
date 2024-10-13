from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient

quiz_generate = Blueprint('quiz_generate', __name__)

def generate_quiz_from_topic(topic, level):
    try:
        client = InferenceClient(api_key="YOUR_HUGGINGFACE_API")
        prompt = f"""
        Generate 5 {level} level quiz questions on the topic {topic} in the following format:
        
        Each question should be on a new line and follow this structure:
        <Q_Number> | <Question_Text> | <Option_1> , <Option_2> , <Option_3> , <Option_4> | <Correct_Answer>
        
        Pattern Explanation:
        - Each element is separated by `|` to make it easy to extract.
        - Options are separated by commas `,`.
        - The correct answer directly matches one of the options.
        - Ensure correct answers appear in the options list.
        
        Example Output:
        Q1 | What is Artificial Intelligence (AI)? | The simulation of human intelligence by machines , A computer programming language , A type of operating system , A new programming paradigm | The simulation of human intelligence by machines
        """

        quiz_lines = ''
        for message in client.chat_completion(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=True,
        ):
            quiz_lines += message.choices[0].delta.content

        quiz = []
        quiz_lines = quiz_lines.strip().split("\n")
        for line in quiz_lines:
            parts = line.split(" | ")
            if len(parts)>2:
                question_number = parts[0].strip()
                question_text = parts[1].strip()
                options = [opt.strip() for opt in parts[2].split(",")]
                answer = parts[3].strip()

                question_data = {
                    "question_number": question_number,
                    "question": question_text,
                    "options": options,
                    "answer": answer
                }
                
                quiz.append(question_data)

        return quiz, None
    except Exception as e:
        return None, str(e)

@quiz_generate.route('/quiz/generate/topic', methods=['POST'])
def generate_quiz_ontopic():
    data = request.json
    topic = data.get("topic")
    level = data.get("level", "Intermediate")

    if not topic or not level:
        return jsonify({"error": "Both 'topic' and 'level' must be provided."}), 400

    quiz, error = generate_quiz_from_topic(topic, level)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(quiz)

def generate_quiz_from_content(text_content, level):
    try:
        client = InferenceClient(api_key="YOUR_HUGGINGFACE_API")
        prompt = f"""
        Based on the following content, generate 5 {level} level quiz questions. 
        Each question should focus on key concepts or important details within the text. 
        Each question should be in the format:
        <Q_Number> | <Question_Text> | <Option_1> , <Option_2> , <Option_3> , <Option_4> | <Correct_Answer>
        
        Text Content:
        {text_content}
        
        Example Output:
        Q1 | What is Artificial Intelligence (AI)? | The simulation of human intelligence by machines , A computer programming language , A type of operating system , A new programming paradigm | The simulation of human intelligence by machines
        """

        quiz_lines = ''
        for message in client.chat_completion(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            stream=True,
        ):
            quiz_lines += message.choices[0].delta.content

        quiz = []
        quiz_lines = quiz_lines.strip().split("\n")
        for line in quiz_lines:
            parts = line.split(" | ")
            if len(parts)==4:
                print(parts)
                question_number = parts[0].strip()
                question_text = parts[1].strip()
                options = [opt.strip() for opt in parts[2].split(",")]
                answer = parts[3].strip()

                question_data = {
                    "question_number": question_number,
                    "question": question_text,
                    "options": options,
                    "answer": answer
                }
                
                quiz.append(question_data)

        return quiz, None
    except Exception as e:
        return None, str(e)

@quiz_generate.route('/quiz/generate/content', methods=['POST'])
def generate_quiz_oncontent():
    data = request.json
    text_content = data.get("text_content")
    level = data.get("level")

    if not text_content or not level:
        return jsonify({"error": "Both 'text_content' and 'level' must be provided."}), 400

    quiz, error = generate_quiz_from_content(text_content, level)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(quiz)
