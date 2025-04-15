class Question:
    """Esta clase representa una pregunta de Trivia con sus opciones
    de respuesta y la respuesta correcta.
    """
    def __init__(self, question_text: str, answer_options: list, correct_answer_index: int):
        """Crea una instancia de la clase Question

        Args:
            question_text (str): La pregunta a mostrar
            answer_options (list): Las opciones de respuesta
            correct_answer (int): La respuesta correcta (índice de la opción correcta)
        """
        self._question_text = question_text
        self._answer_options = answer_options
        
        if not 0 <= correct_answer_index < len(answer_options):
            raise ValueError(f"El índice {correct_answer_index} esta fuera del rango de respuestas.")
        self._correct_answer_index = correct_answer_index
        
    
    def show_question(self):
        """Muestra la pregunta y sus opciones de respuesta por consola
        """
        print(self._question_text)
        for i, option in enumerate(self._answer_options):
            print(f"{i + 1}) {option}")

    
            
    def is_correct(self, user_answer: int) -> bool:
        """Verifica si la respuesta es correcta

        Args:
            user_answer (int): El número de la opcion elegida por el usuario.

        Returns:
            bool: True si la respuesta del participante coincide con 'correct_answer'
        """
        return user_answer == self._correct_answer_index
    


class Quiz:
    
    def __init__(self):
        """Crea una instancia de la clase Quiz
        """
        self._questions = []
        self._current_question_index = 0
        self._correct_answers = 0
        self._incorrect_answers = 0
        
    
    def add_question(self, question: Question):
        """Agrega una pregunta al cuestionario

        Args:
            question (Question): La pregunta a agregar
        """
        self._questions.append(question)
        
    def get_next_question(self) -> Question:
        """Devuelve la siguiente pregunta del cuestionario

        Returns:
            Question: La siguiente pregunta
        """
        if self._current_question_index < len(self._questions):
            question = self._questions[self._current_question_index]
            self._current_question_index += 1
            return question
        
        return None
    
    
    def answer_question(self, user_answer: int) -> bool:
        """Verifica la respuesta del usuario y actualiza el puntaje

        Args:
            user_answer (int): La respuesta del usuario, de corresponder al indice de la respuesta
            en la lista de opciones de respuesta.

        Returns:
            bool: True si la respuesta es correcta, False si no lo es
        """
        question = self._questions[self._current_question_index - 1]
        if question.is_correct(user_answer):
            self._correct_answers += 1
            return True
        
        self._incorrect_answers += 1
        return False
    
    
def run_quiz():

    print("Bienvenido al juego de Trivia!")
    print("Responde las preguntas eligiendo el número de la opción correcta.\n")

    quiz = Quiz()
    
    question1 = Question("¿Quién escribió 'Cien años de soledad'?", ["Pablo Neruda", "Gabriel García Márquez", "Mario Vargas Llosa", "Julio Cortázar"], 1)
    question2 = Question("¿Cuál es el resultado de 3² + 4²?", ["25", "12", "5", "49"], 0)
    question3 = Question("¿En qué año ocurrió la Revolución Francesa?", ["1789", "1810", "1492", "1804"], 0)
    question4 = Question("¿Cuál es el símbolo químico del oro?", ["Ag", "Au", "Gd", "Ga"], 1)
    question5 = Question("¿Qué país tiene mayor población?", ["Estados Unidos", "India", "Rusia", "China"], 3)
    question6 = Question("¿Qué tipo de energía produce una planta nuclear?", ["Eólica", "Solar", "Térmica", "Nuclear"], 3)
    question7 = Question("¿Quién propuso la teoría de la relatividad?", ["Newton", "Einstein", "Tesla", "Bohr"], 1)
    question8 = Question("¿Quién es el creador de Linux?", ["Bill Gates", "Richard Stallman", "Linus Torvalds", "Guido van Rossum "], 2)
    question9 = Question("¿Cuál es el planeta más grande del sistema solar?", ["Tierra", "Júpiter", "Saturno", "Marte"], 1)
    question10 = Question("¿Cuántos huesos tiene el cuerpo humano adulto?", ["206", "201", "210", "205"], 0)


    quiz.add_question(question1)
    quiz.add_question(question2)
    quiz.add_question(question3)
    quiz.add_question(question4)
    quiz.add_question(question5)
    quiz.add_question(question6)
    quiz.add_question(question7)
    quiz.add_question(question8)
    quiz.add_question(question9)
    quiz.add_question(question10)
    
    while quiz._current_question_index < len(quiz._questions):
        current_question = quiz.get_next_question()
        current_question.show_question()
        
        user_answer = int(input("Elige una opción: "))
        quiz.answer_question(user_answer - 1)  # Restar 1 para que coincida con el índice de la lista
        
    print("\nJuego terminado. Aquí está tu puntuación:")
    print(f"Preguntas contestadas: {len(quiz._questions)}")
    print(f"Respuestas correctas: {quiz._correct_answers}")
    print(f"Respuesta incorrectas: {quiz._incorrect_answers}")
        
if __name__ == "__main__":
    run_quiz()