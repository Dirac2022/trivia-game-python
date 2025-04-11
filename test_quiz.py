import pytest
from trivia import Quiz, Question

def test_quiz_creation():
    quiz = Quiz()
    assert quiz._questions == []
    assert quiz._current_question_index == 0
    assert quiz._correct_answers == 0
    assert quiz._incorrect_answers == 0
    
def test_add_question():
    quiz = Quiz()
    question = Question(
        "¿Capital de Italia?", 
        ["Roma", "Madrid", "Berlín", "Londres"], 
        0)
    quiz.add_question(question)
    assert len(quiz._questions) == 1
    assert quiz._questions[0] == question
    
def test_get_next_question():
    quiz = Quiz()
    question1 = Question(
        "¿Capital de Italia?", 
        ["Roma", "Madrid", "Berlín", "Londres"], 
        0)
    question2 = Question(
        "¿Capital de Francia?", 
        ["Roma", "Madrid", "París", "Londres"], 
        2)
    quiz.add_question(question1)
    quiz.add_question(question2)
    
    assert quiz.get_next_question() == question1
    assert quiz._current_question_index == 1  # Se ha incrementado el índice de la pregunta actual
    assert quiz.get_next_question() == question2
    assert quiz._current_question_index == 2  # Se ha incrementado el índice de la pregunta actual
    assert quiz.get_next_question() == None  # No hay más preguntas
    assert quiz._current_question_index == 2  # El índice no ha cambiado
    

def test_get_next_question_empty_quiz():
    quiz = Quiz()
    assert quiz.get_next_question() == None  # No hay preguntas en el cuestionario
    assert quiz._current_question_index == 0  # El índice no ha cambiado
    
def test_answer_question_correct():
    quiz = Quiz()
    question = Question(
        "¿Cual es el nombre del creador de Linux?",
        ["Linus Torvalds", "Bill Gates", "Steve Jobs", "Richard Stallman"],
        0)
    quiz.add_question(question)
    assert quiz.answer_question_correct(0) == True 
    assert quiz._correct_answers == 1
    assert quiz._incorrect_answers == 0
    
    
def test_answer_question_incorrect():
    quiz = Quiz()
    question = Question(
        "¿Cual es el nombre del creador de Linux?",
        ["Linus Torvalds", "Bill Gates", "Steve Jobs", "Richard Stallman"],
        0)
    quiz.add_question(question)
    assert quiz.answer_question(1) == False 
    assert quiz._correct_answers == 0
    assert quiz._incorrect_answers == 1
    
    
