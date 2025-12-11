from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizAnswer, StudentQuizAttempt


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1
    inlines = [QuizAnswerInline]


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]
    list_display = ["title", "course", "passing_score", "max_attempts"]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(StudentQuizAttempt)
