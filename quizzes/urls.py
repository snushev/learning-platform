from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, StudentQuizAttemptViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quizzes')
router.register(r'quiz-attempts', StudentQuizAttemptViewSet, basename='quiz-attempts')

urlpatterns = router.urls