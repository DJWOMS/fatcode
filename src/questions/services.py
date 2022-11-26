from . import models


class QuestionService:

    def __init__(self, question: models.Question):
        self.question = question

    def answers_count(self):
        return self.question.answers.count()

    def correct_answers_count(self):
        return self.question.answers.filter(accepted=True).count()

    def update_rating(self):
        self.question.rating += models.QuestionReview.objects.filter(question=self, grade=True).count()
        self.question.rating -= models.QuestionReview.objects.filter(question=self, grade=False).count()
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

    def update_rating(self):
        # TODO что здесь происходит?
        self.answer.rating += self.answer.review.objects.filter(answer=self, grade=True).count()
        self.answer.rating -= self.answer.review.objects.filter(answer=self, grade=False).count()
        return super().save()

    def update_accept(self):
        self.answer.accepted = not self.answer.accepted
        return self.answer


def create_follow(question, follower):
    models.QuestionFollowers.objects.create(question=question, follower=follower)
