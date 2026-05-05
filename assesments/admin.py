from django.contrib import admin
from .models import Assignment, Submission, Quiz, Question, QuizSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    pass