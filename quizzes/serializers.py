from rest_framework import serializers
from .models import Quiz, QuizAnswer, QuizQuestion, StudentQuizAttempt


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ["id", "answer_text", "is_correct"]
        extra_kwargs = {"is_correct": {"write_only": True}}


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ["id", "question_text", "question_type", "order", "points", "answers"]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(source="quiz_questions", many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "course", "title", "description", "order", "passing_score", "max_attempts", "questions"]


class StudentQuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentQuizAttempt
        fields = ["id", "enrollment", "quiz", "attempt_number", "score", "answers", "completed_at", "passed"]
