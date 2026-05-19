from django.contrib import admin
from .models import Assignment, Submission, Quiz, Question, QuizSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for Assignment model.
    
    Allows administrators to manage course assignments through Django admin interface.
    """
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for Submission model.
    
    Allows administrators to view and manage student assignment submissions.
    """
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin configuration for Quiz model.
    
    Allows administrators to manage course quizzes and their settings.
    """
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model.
    
    Allows administrators to manage quiz questions and answer options.
    """
    pass


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for QuizSubmission model.
    
    Allows administrators to view and manage student quiz submissions and scores.
    """
    pass