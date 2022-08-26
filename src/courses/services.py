def check_quiz(self):
    return self.quiz_answer.right


def check_code(self):
    student_answer = list(self.code_answer.replace(' ', ''))
    answer = list(self.lesson.code.first().answer.replace(' ', ''))
    return student_answer == answer
