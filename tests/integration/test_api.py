from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Prueba para el endpoint raíz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Hola desde la API de Trivia!"}

def test_get_question_by_id():
    """Prueba para obtener una pregunta por su ID (índice en la lista predefinida)."""
    expected_question_text = "¿Quién escribió 'Cien años de soledad'?"
    response = client.get("/questions/0")  # ID 0 para la primera pregunta
    assert response.status_code == 200
    assert response.json()["question_text"] == expected_question_text
    assert response.json()["id"] == 0

    response_not_found = client.get("/questions/999")  # ID que no existe
    assert response_not_found.status_code == 404
    assert response_not_found.json()["detail"] == "Question not found"

def test_create_quiz_and_get_next_question():
    """Prueba para crear un quiz y obtener la siguiente pregunta."""
    # Crear un quiz
    create_quiz_response = client.post("/quizzes/")
    assert create_quiz_response.status_code == 201
    assert "quiz_id" in create_quiz_response.json()
    # Extraer el ID del quiz creado
    quiz_id = create_quiz_response.json()["quiz_id"]

    # Obtener la primera pregunta del quiz
    get_next_response = client.get(f"/quizzes/{quiz_id}/next_question")
    assert get_next_response.status_code == 200
    assert "question_text" in get_next_response.json()
    assert "answer_options" in get_next_response.json()
    assert get_next_response.json()["question_index"] == 1
    assert get_next_response.json()["total_questions"] == 10  # Tenemos 10 preguntas predefinidas

def test_answer_question_correct_and_incorrect():
    """Prueba para responder una pregunta correctamente e incorrectamente."""
    # Creamos un quiz
    create_quiz_response = client.post("/quizzes/")
    assert create_quiz_response.status_code == 201
    quiz_id = create_quiz_response.json()["quiz_id"]

    # Obtenemos la primera pregunta
    get_next_response = client.get(f"/quizzes/{quiz_id}/next_question")
    assert get_next_response.status_code == 200
    first_question = get_next_response.json()

    # La primera pregunta es "¿Quién escribió 'Cien años de soledad'?" y la respuesta correcta es la opción con índice 1 (Gabriel García Márquez).
    # El usuario elegiría la opción 2 en la interfaz (índice + 1).
    correct_answer = 2
    answer_correct_response = client.post(f"/quizzes/{quiz_id}/answer", json={"user_answer": correct_answer})
    assert answer_correct_response.status_code == 200
    assert answer_correct_response.json() == {"correct": True}

    # Obtenemos la siguiente pregunta
    get_next_response_2 = client.get(f"/quizzes/{quiz_id}/next_question")
    if get_next_response_2.status_code == 200:
        # Respondemos incorrectamente a la siguiente pregunta (la respuesta correcta para la segunda pregunta es el índice 0, que es la opción 1).
        # La pregunta es: ¿Cuál es el resultado de 3² + 4²?
        # El usuario elegiría una opción incorrecta, por ejemplo, la 3
        incorrect_answer = 3
        answer_incorrect_response = client.post(f"/quizzes/{quiz_id}/answer", json={"user_answer": incorrect_answer})
        assert answer_incorrect_response.status_code == 200
        assert answer_incorrect_response.json() == {"correct": False}