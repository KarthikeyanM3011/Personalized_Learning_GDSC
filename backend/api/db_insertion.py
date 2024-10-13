from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..main import db  # Adjust this import to your application's context

data_insertion_bp = Blueprint('data_insertion', __name__)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Renamed for clarity

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Renamed for clarity

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Renamed for clarity

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

@data_insertion_bp.route('/quiz', methods=['POST'])
def insert_quiz():
    data = request.json
    new_quiz = Quiz(
        user_email=data['user_email'],
        question=data['question'],
        answer=data['answer'],
        score=data['score']
    )
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({"message": "Quiz entry created successfully"}), 201

@data_insertion_bp.route('/assessment', methods=['POST'])
def insert_assessment():
    data = request.json
    new_assessment = Assessment(
        user_email=data['user_email'],
        question=data['question'],
        answer=data['answer'],
        score=data['score']
    )
    db.session.add(new_assessment)
    db.session.commit()
    return jsonify({"message": "Assessment entry created successfully"}), 201

@data_insertion_bp.route('/chat', methods=['POST'])
def insert_chat():
    data = request.json
    new_chat = Chat(
        user_email=data['user_email'],
        message=data['message'],
        response=data.get('response')
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"message": "Chat entry created successfully"}), 201

@data_insertion_bp.route('/user', methods=['POST'])
def insert_user():
    data = request.json

    user_email = data.get('user_email')
    password = data.get('password')
    name = data.get('name')

    if not user_email or not password or not name:
        return jsonify({"message": "All fields are required"}), 400

    existing_user = User.query.filter_by(user_email=user_email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 409

    new_user = User(
        user_email=user_email,
        password=generate_password_hash(password),
        name=name
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@data_insertion_bp.route('/user/<string:user_email>/<string:password>', methods=['GET'])
def get_user(user_email, password):
    user = User.query.filter_by(user_email=user_email).first()
    
    if user and check_password_hash(user.password, password):
        return jsonify({
            "user_email": user.user_email,
            "name": user.name,
        }), 200
    
    return jsonify({"message": "User not found or password incorrect"}), 404

@data_insertion_bp.route('/quizzes/<string:user_email>', methods=['GET'])
def get_quizzes(user_email):
    quizzes = Quiz.query.filter_by(user_email=user_email).all()
    result = [
        {
            "id": quiz.id,
            "question": quiz.question,
            "answer": quiz.answer,
            "score": quiz.score,
            "created_at": quiz.created_at  # Updated field name
        } for quiz in quizzes
    ]
    return jsonify(result), 200

@data_insertion_bp.route('/assessments/<string:user_email>', methods=['GET'])
def get_assessments(user_email):
    assessments = Assessment.query.filter_by(user_email=user_email).all()
    result = [
        {
            "id": assessment.id,
            "question": assessment.question,
            "answer": assessment.answer,
            "score": assessment.score,
            "created_at": assessment.created_at  # Updated field name
        } for assessment in assessments
    ]
    return jsonify(result), 200

@data_insertion_bp.route('/chats/<string:user_email>', methods=['GET'])
def get_chats(user_email):
    chats = Chat.query.filter_by(user_email=user_email).all()
    result = [
        {
            "id": chat.id,
            "message": chat.message,
            "response": chat.response,
            "created_at": chat.created_at  # Updated field name
        } for chat in chats
    ]
    return jsonify(result), 200
