from . import models


class QuestionService:

    def __init__(self, question):
        self.question = question

    def answers_count(self):
        return self.question.answers.count()

    def correct_answers_count(self):
        return self.question.answers.filter(accepted=True).count()


