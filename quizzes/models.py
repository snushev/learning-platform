from django.db import models
from courses.models import Course
from enrollments.models import Enrollment


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    order = models.IntegerField()
    passing_score = models.IntegerField()
    max_attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class QuizQuestion(models.Model):
    TYPES = (("multiple_choice", "Multiple_choise"), ("true_false", "True_false"))

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_questions")
    question_text = models.TextField(max_length=500)
    question_type = models.CharField(max_length=20, choices=TYPES)
    order = models.IntegerField()
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text[:50]

    class Meta:
        ordering = ["order"]


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer_text


class StudentQuizAttempt(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempt_quiz")
    attempt_number = models.IntegerField()
    score = models.IntegerField()
    answers = models.JSONField()
    completed_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField()

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.quiz.title} - Attempt {self.attempt_number}"
