from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Importamos las clases Question y Quiz desde nuestro archivo trivia.py
from trivia import Question as TriviaQuestion, Quiz as TriviaQuiz

app = FastAPI()

# --- Modelos Pydantic para la API ---

class QuestionOut(BaseModel):
    """Modelo para la respuesta de la API al devolver una pregunta.
    Attributes:
        question_text (str): Texto de la pregunta.
        answer_options (List[str]): Opciones de respuesta.
        id (int): ID de la pregunta.
    """
    question_text: str
    answer_options: List[str]
    id: int

class QuizOut(BaseModel):
    """Modelo para la respuesta de la API al crear un nuevo quiz.
    Attributes:
        quiz_id (int): ID del nuevo quiz.
    """
    quiz_id: int

class AnswerIn(BaseModel):
    """Modelo para recibir la respuesta del usuario."""
    user_answer: int # Representa la opción elegida por el usuario (1, 2, 3 o 4)

class AnswerOut(BaseModel):
    """Modelo para la respuesta de la API al verificar una respuesta."""
    correct: bool

class NextQuestionOut(BaseModel):
    """Modelo para la respuesta de la API al obtener la siguiente pregunta.
    Attributes:
        question_text (str): Texto de la pregunta.
        answer_options (List[str]): Opciones de respuesta.
        question_index (int): Índice de la pregunta actual en el quiz.
        total_questions (int): Total de preguntas en el quiz.
    """
    question_text: str
    answer_options: List[str]
    question_index: int
    total_questions: int

# --- Preguntas predefinidas ---
PREDEFINED_QUESTIONS = [
    TriviaQuestion("¿Quién escribió 'Cien años de soledad'?", ["Pablo Neruda", "Gabriel García Márquez", "Mario Vargas Llosa", "Julio Cortázar"], 1),
    TriviaQuestion("¿Cuál es el resultado de 3² + 4²?", ["25", "12", "5", "49"], 0),
    TriviaQuestion("¿En qué año ocurrió la Revolución Francesa?", ["1789", "1810", "1492", "1804"], 0),
    TriviaQuestion("¿Cuál es el símbolo químico del oro?", ["Ag", "Au", "Gd", "Ga"], 1),
    TriviaQuestion("¿Qué país tiene mayor población?", ["Estados Unidos", "India", "Rusia", "China"], 3),
    TriviaQuestion("¿Qué tipo de energía produce una planta nuclear?", ["Eólica", "Solar", "Térmica", "Nuclear"], 3),
    TriviaQuestion("¿Quién propuso la teoría de la relatividad?", ["Newton", "Einstein", "Tesla", "Bohr"], 1),
    TriviaQuestion("¿Quién es el creador de Linux?", ["Bill Gates", "Richard Stallman", "Linus Torvalds", "Guido van Rossum "], 2),
    TriviaQuestion("¿Cuál es el planeta más grande del sistema solar?", ["Tierra", "Júpiter", "Saturno", "Marte"], 1),
    TriviaQuestion("¿Cuántos huesos tiene el cuerpo humano adulto?", ["206", "201", "210", "205"], 0),
]

quizzes_db = {}

# ID para el siguiente quiz a crear
next_quiz_id = 1

# --- Endpoints de la API ---

@app.get("/")
def read_root():
    """Endpoint raíz de la API."""
    return {"message": "¡Hola desde la API de Trivia!"}

@app.get("/questions/{question_id}", response_model=QuestionOut)
def get_question(question_id: int):
    """Endpoint para obtener una pregunta por su ID."""
    if 0 <= question_id < len(PREDEFINED_QUESTIONS):
        question = PREDEFINED_QUESTIONS[question_id]
        return QuestionOut(
            question_text=question._question_text,
            answer_options=question._answer_options,
            id=question_id
        )
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/quizzes/", response_model=QuizOut, status_code=201)
def create_quiz():
    """Endpoint para crear un nuevo quiz."""
    global next_quiz_id
    quiz_id = next_quiz_id
    new_quiz = TriviaQuiz()
    for question in PREDEFINED_QUESTIONS:
        new_quiz.add_question(question)
    quizzes_db[quiz_id] = new_quiz
    next_quiz_id += 1
    return QuizOut(quiz_id=quiz_id)

@app.get("/quizzes/{quiz_id}/next_question", response_model=NextQuestionOut)
def get_next_question(quiz_id: int):
    """Endpoint para obtener la siguiente pregunta de un quiz."""
    if quiz_id not in quizzes_db:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz = quizzes_db[quiz_id]
    next_question = quiz.get_next_question()
    if next_question:
        return NextQuestionOut(
            question_text=next_question._question_text,
            answer_options=next_question._answer_options,
            question_index=quiz._current_question_index,
            total_questions=len(quiz._questions)
        )
    raise HTTPException(status_code=404, detail="No more questions in the quiz")

@app.post("/quizzes/{quiz_id}/answer", response_model=AnswerOut)
def answer_question(quiz_id: int, answer: AnswerIn):
    """Endpoint para responder a la pregunta actual de un quiz."""
    if quiz_id not in quizzes_db:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz = quizzes_db[quiz_id]
    # Ajustamos la respuesta del usuario para que coincida con el índice de la lista
    user_answer_index = answer.user_answer - 1
    is_correct = quiz.answer_question(user_answer_index)
    return AnswerOut(correct=is_correct)