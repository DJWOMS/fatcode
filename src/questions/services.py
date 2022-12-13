from django.db.models import Q, Count

from . import models
from ..profiles.services import ReputationService


class QuestionService:

    def __init__(self, question: models.Question):
        self.question = question

    def answers_count(self):
        return self.question.answers.count()

    def correct_answers_count(self):
        return self.question.answers.filter(accepted=True).count()

    def update_rating(self, grade):
        if grade:
            self.question.rating += 1
            ReputationService(self.question.author).increase_reputation(15, 'inc')
        else:
            self.question.rating -= 1
            ReputationService(self.question.author).increase_reputation(15, 'dcr')
        return self.question.save()

    def update_tags(self, tags):
        for tag_data in tags:
            tag_qs = models.Tag.objects.filter(name__iexact=tag_data["name"])
            if tag_qs.exists():
                tag = tag_qs.first()
            else:
                tag = models.Tag.objects.create(**tag_data)
            self.question.tags.add(tag)

    def all_answers(self):
        return self.question.answers.all()


class AnswerService:

    def __init__(self, answer: models.Answer):
        self.answer = answer

    def update_rating(self, grade):
        if grade:
            self.answer.rating += 1
            ReputationService(self.answer.author).increase_reputation(15, 'inc')
        else:
            self.answer.rating -= 1
            ReputationService(self.answer.author).increase_reputation(15, 'dcr')
        return self.answer.save()

    def update_accept(self):
        self.answer.accepted = not self.answer.accepted
        ReputationService(self.answer.author).increase_reputation(20, 'inc')
        return self.answer.save()


def create_follow(question, follower):
    models.QuestionFollowers.objects.create(question=question, follower=follower)
