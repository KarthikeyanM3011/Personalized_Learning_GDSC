from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from api.quiz_generation import quiz_generate
from api.chat_rag import chat_rag
from api.extract_text import upload_bp
from api.assignment_generation import assignment_blueprint
from api.chat import chatbot_blueprint

# Create an instance of SQLAlchemy
db = SQLAlchemy()

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)

    # Create the database tables upon initialization
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Learning Path API!"})

    try:
        app.register_blueprint(quiz_generate)
        # app.register_blueprint(data_insertion_bp) 
        app.register_blueprint(chat_rag) 
        app.register_blueprint(upload_bp) 
        app.register_blueprint(assignment_blueprint) 
        app.register_blueprint(chatbot_blueprint) 
    except Exception as e:
        print(f"Error registering blueprint: {e}")

    @app.route('/quiz', methods=['POST'])
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

    @app.route('/assessment', methods=['POST'])
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

    @app.route('/chat', methods=['POST'])
    def insert_chat():
        data = request.json
        new_chat = Chat(
            user_email=data['user_email'],
            message=data['message'],
            response=data.get('response', None)
        )
        db.session.add(new_chat)
        db.session.commit()
        return jsonify({"message": "Chat entry created successfully"}), 201

    @app.route('/user', methods=['POST'])
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

    @app.route('/user/<string:user_email>/<string:password>', methods=['GET'])
    def get_user(user_email, password):
        user = User.query.filter_by(user_email=user_email).first()
        
        if user and check_password_hash(user.password, password):  # Verify the password
            return jsonify({
                "user_email": user.user_email,
                "name": user.name,
            }), 200
        
        return jsonify({"message": "User not found or password incorrect"}), 404

    @app.route('/quizzes/<string:user_email>', methods=['GET'])
    def get_quizzes(user_email):
        quizzes = Quiz.query.filter_by(user_email=user_email).all()
        result = [
            {
                "id": quiz.id,
                "question": quiz.question,
                "answer": quiz.answer,
                "score": quiz.score,
                "datetime": quiz.datetime
            } for quiz in quizzes
        ]
        return jsonify(result), 200

    @app.route('/assessments/<string:user_email>', methods=['GET'])
    def get_assessments(user_email):
        assessments = Assessment.query.filter_by(user_email=user_email).all()
        result = [
            {
                "id": assessment.id,
                "question": assessment.question,
                "answer": assessment.answer,
                "score": assessment.score,
                "datetime": assessment.datetime
            } for assessment in assessments
        ]
        return jsonify(result), 200

    @app.route('/chats/<string:user_email>', methods=['GET'])
    def get_chats(user_email):
        chats = Chat.query.filter_by(user_email=user_email).all()
        result = [
            {
                "id": chat.id,
                "message": chat.message,
                "response": chat.response,
                "datetime": chat.datetime
            } for chat in chats
        ]
        return jsonify(result), 200

    return app

if __name__ == '__main__':
    app = create_app()  # Create the app instance
    app.run(host='0.0.0.0', port=5000, debug=True)
