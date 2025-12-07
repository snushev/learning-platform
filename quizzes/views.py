from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Quiz, QuizQuestion, QuizAnswer, StudentQuizAttempt
from .serializers import QuizSerializer, StudentQuizAttemptSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['course']
    ordering = ['order']
    
    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only create quizzes for your own courses")
        serializer.save()
    
    def perform_update(self, serializer):
        if serializer.instance.course.instructor != self.request.user:
            raise PermissionDenied("You can only update quizzes for your own courses")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.course.instructor != self.request.user:
            raise PermissionDenied("You can only delete quizzes for your own courses")
        instance.delete()


class StudentQuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = StudentQuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == "Student":
            return StudentQuizAttempt.objects.filter(enrollment__student=self.request.user)
        return StudentQuizAttempt.objects.filter(quiz__course__instructor=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.role != "Student":
            raise PermissionDenied("Only students can take quizzes")
        
        quiz = serializer.validated_data.get('quiz')
        
        from enrollments.models import Enrollment
        try:
            enrollment = Enrollment.objects.get(
                student=self.request.user,
                course=quiz.course
            )
        except Enrollment.DoesNotExist:
            raise PermissionDenied("You must be enrolled in the course to take this quiz")
        
        existing_attempts = StudentQuizAttempt.objects.filter(
            enrollment=enrollment,
            quiz=quiz
        ).count()
        
        if existing_attempts >= quiz.max_attempts:
            raise ValidationError(f"Maximum attempts ({quiz.max_attempts}) reached for this quiz")
        
        serializer.save(
            enrollment=enrollment,
            attempt_number=existing_attempts + 1,
            score=0,
            passed=False,
            answers={}
        )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        
        if attempt.enrollment.student != request.user:
            raise PermissionDenied("You can only submit your own attempts")
        
        if attempt.answers and len(attempt.answers) > 0:
            return Response(
                {"error": "This attempt has already been submitted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submitted_answers = request.data.get('answers', {})
        
        if not submitted_answers:
            return Response(
                {"error": "No answers provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quiz = attempt.quiz
        questions = quiz.quiz_questions.all()
        total_points = sum(q.points for q in questions)
        earned_points = 0
        
        for question in questions:
            question_id = str(question.id)
            submitted_answer = submitted_answers.get(question_id)
            
            if not submitted_answer:
                continue
            
            if question.question_type == 'multiple_choice':
                try:
                    answer = QuizAnswer.objects.get(
                        id=submitted_answer,
                        question=question
                    )
                    if answer.is_correct:
                        earned_points += question.points
                except QuizAnswer.DoesNotExist:
                    pass
            
            elif question.question_type == 'true_false':
                correct_answer = QuizAnswer.objects.filter(
                    question=question,
                    is_correct=True
                ).first()
                
                if correct_answer and submitted_answer.lower() == correct_answer.answer_text.lower():
                    earned_points += question.points
        
        score_percentage = int((earned_points / total_points) * 100) if total_points > 0 else 0
        passed = score_percentage >= quiz.passing_score
        
        attempt.answers = submitted_answers
        attempt.score = score_percentage
        attempt.passed = passed
        attempt.save()
        
        return Response({
            "message": "Quiz submitted successfully",
            "score": score_percentage,
            "passed": passed,
            "earned_points": earned_points,
            "total_points": total_points
        }, status=status.HTTP_200_OK)