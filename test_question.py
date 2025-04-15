import pytest
from trivia import Question

def test_question_creation():
    
    question = Question("¿Capital de Italia?", ["Roma", "Madrid", "Berlín", "Londres"], 0)
    assert question._question_text == "¿Capital de Italia?"
    assert question._answer_options == ["Roma", "Madrid", "Berlín", "Londres"]
    assert question._correct_answer_index == 0
    

def test_is_correct_true():
    question = Question("2 + 2", ["3", "4", "5", "0"], 1)
    assert question.is_correct(1) == True  
    
def test_is_correct_false():
    
    question = Question("¿En que año llego Cristobal Colon a America", ["1542", "1476", "1492", "1500"], 2)
    assert question.is_correct(1) == False