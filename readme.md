# AI-Powered Chatbot and RAG System

## Table of Contents
- [Welcome](#welcome)
- [Chatbot](#chatbot)
- [RAG Chat](#rag-chat)
- [Quiz Generation](#quiz-generation)
- [Assignment Generation](#assignment-generation)
- [Technologies Used](#technologies-used)
- [Installation](#installation)

<p align="center">
  <img src="pictures/image.png" width="350" height="300" style="margin-right: 10px;"/>
</p>

## 🌟 Key Features
## Welcome
Welcome to the AI-Powered Chatbot and RAG System! This project leverages the capabilities of AI models, including the Mixtral model from Hugging Face, to provide intelligent interaction with uploaded documents, quizzes, and assignment generation based on user inputs.

## Chatbot
The Chatbot feature allows users to ask questions and receive responses generated by an AI model. The chatbot can handle various topics and provide accurate information. It utilizes advanced natural language processing techniques to ensure a seamless user experience.

### Features
- **Real-time conversation**: Engage with the chatbot and receive immediate answers.
- **Contextual understanding**: The chatbot remembers previous interactions to provide contextually relevant responses.

## RAG Chat
The RAG (Retrieval-Augmented Generation) Chat feature allows users to upload multiple PDF files, which are then processed to extract content for question answering. This feature combines document retrieval with generative responses for enhanced information delivery.

### Features
- **Multiple file uploads**: Users can upload PDFs, PPTs, and DOCX files for analysis.
- **Contextual responses**: The system uses the content of uploaded documents to answer user questions accurately.

## Quiz Generation
The Quiz Generation feature allows the system to create quizzes based on the contents of uploaded files. Users can specify topics or keywords, and the system will generate relevant questions.

### Features
- **Dynamic quiz creation**: Generate quizzes based on document content and specified topics.
- **Variety of question types**: Support for multiple-choice, true/false, and open-ended questions.

## Assignment Generation
The Assignment Generation feature enables users to create assignments based on specific topics or the content of uploaded files. This is particularly useful for educators looking to create tailored assignments for students.

### Features
- **Topic-based assignments**: Generate assignments based on user-defined topics.
- **Content extraction**: Use uploaded files to create relevant assignment questions.

## Technologies Used
This project incorporates several technologies for robust performance and modular architecture:

- **Flask**: A lightweight WSGI web application framework for Python, used for building the backend.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool for interacting with relational databases in Python.
- **Blueprints**: Used in Flask for modularizing the application, allowing for cleaner code and easier management of routes and views.
- **Streamlit**: For building the interactive front end that communicates with the backend services.
- **Hugging Face Models**: Integrating advanced NLP models and different Prompt engineering techniques for chatbot responses and document analysis.

## Installation
To install the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
    ```

    ```bash
    cd streamlit_app
    ```

    ```python
    streamlit rum app.py
    ```

    ```bash 
    cd backend
    ```

    ```python 
    python main.py
    ```

2. Replace YOUR_HUGGINGFACE_API with your API KEY in backend files

### 🖥️ Interface
<p align="center">
  <img src="pictures/Signup.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/Login.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/Welcome.png" width="250"/>
  <img src="pictures/Assignment_on_topic.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/Chat_with_historycontext.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/Quiz_on_document.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/Quiz_on_topic.png" width="250" style="margin-right: 10px;"/>
  <img src="pictures/RAG.png" width="250" style="margin-right: 10px;"/>
</p>

    
### Key Additions
- **Technologies Used**: This section details the technologies and frameworks used in the project, including SQLAlchemy and Flask.
- **Installation Instructions**: Clarified the installation process, including how to set up both the backend and frontend, specifically for Windows users.
- **Modular Architecture**: Highlighted the use of Blueprints for a modular approach in the Flask backend.

Feel free to customize any sections further to suit your project's specifics!

## Contact
For any inquiries or feedback, you can reach me at:
- Email: karthikeyanmjnk13579@gmail.com
