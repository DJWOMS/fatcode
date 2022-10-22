from . import models


class QuestionService:

    def __init__(self, question):
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

    def answers_count(self):
        return self.question.answers.all()

    def all_answers(self):
        return self.question.answers.all()

    def correct_answers_count(self):
        return self.question.answers.objects.filter(accepted=True)


class AnswerService:

    def __init__(self, answer):
        self.answer = answer

    def update_rating(self):
        self.rating += self.review.objects.filter(answer=self, grade=True).count()
        self.rating -= self.review.objects.filter(answer=self, grade=False).count()
        return super().save()

