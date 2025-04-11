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
        return user_answer == self._correct_answer_index + 1  # +1 porque los índices de las listas empiezan en 0 y las opciones empiezan en 1
    