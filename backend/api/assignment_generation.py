from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient

assignment_blueprint = Blueprint('assignment', __name__)

def generate_assignment_questions(topic, level, num_questions=5):
    client = InferenceClient(api_key="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")
    
    prompt = f"""
    Generate {num_questions} short 2-mark questions on the topic {topic} for {level} level. Each question should test the understanding of fundamental concepts and be straightforward, requiring precise but concise answers. Follow the format:
    
    Each question should be on a new line and follow this structure:
    <Q_Number> | <Question_Text>
    
    Example Output:
    Q1 | Explain the basic concept of Machine Learning.
    Q2 | What is the purpose of Natural Language Processing?
    Q3 | Define Deep Learning in simple terms.
    """
    
    assignment_lines = ''
    for message in client.chat_completion(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        stream=True,
    ):
        assignment_lines += message.choices[0].delta.content

    questions = []
    assignment_lines = assignment_lines.strip().split("\n")
    for line in assignment_lines:
        parts = line.split(" | ")
        if len(parts)>=2:
            question_number = parts[0].strip()
            question_text = parts[1].strip()

            question_data = {
                "question_number": question_number,
                "question": question_text
            }
            
            questions.append(question_data)
    
    return questions

def generate_questions_from_text(text_content, level, num_questions=5):
    client = InferenceClient(api_key="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")
    
    prompt = f"""
    Based on the following text, generate {num_questions} short 2-mark questions suitable for {level} level. Each question should focus on key concepts or important details within the text. The questions should be straightforward and require precise but concise answers. Follow the format:
    
    Each question should be on a new line and follow this structure:
    <Q_Number> | <Question_Text>
    
    Text Content:
    {text_content}
    
    Example Output:
    Q1 | What is the main theme of the text?
    Q2 | Describe a key event mentioned in the text.
    Q3 | What conclusions can be drawn from the text?
    """
    
    assignment_lines = ''
    for message in client.chat_completion(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        stream=True,
    ):
        assignment_lines += message.choices[0].delta.content

    questions = []
    assignment_lines = assignment_lines.strip().split("\n")
    for line in assignment_lines:
        parts = line.split(" | ")
        if len(parts) >= 2:
            question_number = parts[0].strip()
            question_text = parts[1].strip()

            question_data = {
                "question_number": question_number,
                "question": question_text
            }
            
            questions.append(question_data)
    
    return questions

def evaluate_answers(questions, user_answers):
    client = InferenceClient(api_key="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")
    
    prompt = "Evaluate the following answers to 2-mark questions and provide only the scores out of 2. Format: <Q_Number> | Score out of 2: <Score>.\n"
    
    for i, q in enumerate(questions):
        question_text = q['question']
        user_answer = user_answers[i]
        prompt += f"Q{i+1} | {question_text} | Answer: {user_answer}\n"
    
    evaluation = ''
    for message in client.chat_completion(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        stream=True,
    ):
        evaluation += message.choices[0].delta.content

    scores = []
    evaluation_lines = evaluation.strip().split("\n")
    total_score = 0
    max_score = len(questions) * 2
    
    for line in evaluation_lines:
        parts = line.split(" | ")
        
        if len(parts) >= 2 and parts[0].startswith("Q"):
            score_text = parts[1].strip().split(":")[-1].strip()
            try:
                score = float(score_text) 
            except ValueError:
                score = 0.0

            scores.append(score)
            total_score += score
        else:
            continue

    score_percentage = (total_score / max_score) * 100

    result = [{"question_number": f"Q{i+1}", "score": score} for i, score in enumerate(scores)]
    
    return result, score_percentage

@assignment_blueprint.route('/assignment/generate/topic', methods=['POST'])
def generate_assignment():
    try:
        data = request.json
        topic = data.get("topic")
        level = data.get("level")
        num_questions = data.get("num_questions", 5)

        if not topic or not level:
            return jsonify({"error": "Both 'topic' and 'level' must be provided."}), 400

        questions = generate_assignment_questions(topic, level, num_questions)
        return jsonify(questions)

    except Exception as e:
        return jsonify({"error": "An error occurred while generating assignment questions.", "message": str(e)}), 500

@assignment_blueprint.route('/assignment/generate/content', methods=['POST'])
def generate_rag_questions():
    try:
        data = request.json
        text_content = data.get("text_content")
        level = data.get("level")
        num_questions = data.get("num_questions", 5)

        if not text_content or not level:
            return jsonify({"error": "'text_content' and 'level' must be provided."}), 400

        questions = generate_questions_from_text(text_content, level, num_questions)
        return jsonify(questions)

    except Exception as e:
        return jsonify({"error": "An error occurred while generating questions from the text.", "message": str(e)}), 500

@assignment_blueprint.route('/assignment/evaluate', methods=['POST'])
def evaluate_assignment():
    try:
        data = request.json
        questions = data.get("questions")
        user_answers = data.get("user_answers")

        if not questions or not user_answers:
            return jsonify({"error": "Both 'questions' and 'user_answers' must be provided."}), 400

        results, score_percentage = evaluate_answers(questions, user_answers)
        return jsonify({"results": results, "score_percentage": score_percentage})

    except Exception as e:
        return jsonify({"error": "An error occurred while evaluating answers.", "message": str(e)}), 500
