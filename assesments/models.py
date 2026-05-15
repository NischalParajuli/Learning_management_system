"""Models for assignments, submissions, quizzes, and reminders.

Defines core assessment models including Assignment, Submission, Quiz,
Question, QuizSubmission, and ReminderLog for tracking course activities.
"""

from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class Assignment(models.Model):
    """Represents a course assignment.
    
    Attributes:
        course: ForeignKey to the Course this assignment belongs to.
        instructor: ForeignKey to the User who created the assignment.
        title: Assignment title.
        description: Detailed description of the assignment.
        due_date: Deadline for submission.
        created_at: Timestamp when assignment was created.
    """
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='assignments')
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course})"


class Submission(models.Model):
    """Represents a student's submission for an assignment.
    
    Attributes:
        assignment: ForeignKey to the Assignment being submitted.
        student: ForeignKey to the User (student) submitting.
        content: The submission content.
        submitted_at: Timestamp of submission.
        feedback: Instructor feedback on the submission.
        grade: Numerical grade given by instructor.
        status: Current status of the submission (submitted, graded, late).
    """
    SUBMISSION_STATUS = (
        ('sub', 'submitted'),
        ('grd', 'graded'),
        ('late', 'late'),
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                   related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='assignment_submissions')
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    feedback = models.CharField(max_length=200, blank=True)
    grade = models.FloatField(default=0)
    status = models.CharField(max_length=4, choices=SUBMISSION_STATUS, default='sub')

    class Meta:
        # Enforce one submission per student per assignment
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"


class Quiz(models.Model):
    """Represents a quiz/test within a course.
    
    Attributes:
        course: ForeignKey to the Course this quiz belongs to.
        title: Quiz title.
        instructor: ForeignKey to the User who created the quiz.
        created_at: Timestamp when quiz was created.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=150)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course})"


class Question(models.Model):
    """Represents a multiple-choice question in a quiz.
    
    Attributes:
        quiz: ForeignKey to the Quiz this question belongs to.
        question: The question text.
        opt1-opt4: The four answer options.
        correct_answer: The correct option (A, B, C, or D).
    """
    CORRECT = (
        ('A', 'Option1'),
        ('B', 'Option2'),
        ('C', 'Option3'),
        ('D', 'Option4'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=200)
    opt1 = models.TextField()
    opt2 = models.TextField()
    opt3 = models.TextField()
    opt4 = models.TextField()
    correct_answer = models.CharField(max_length=1, choices=CORRECT)

    def __str__(self):
        return f"{self.question[:50]}"


class QuizSubmission(models.Model):
    """Represents a student's submission of a quiz.
    
    Attributes:
        quiz: ForeignKey to the Quiz being taken.
        student: ForeignKey to the User (student) taking the quiz.
        score: The student's score on the quiz.
        submitted_at: Timestamp when quiz was submitted.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforce one submission per student per quiz
        unique_together = ('quiz', 'student')

    def __str__(self):
        return f"{self.quiz.title} - {self.student.username}"


class ReminderLog(models.Model):
    """Tracks reminder emails sent to students.
    
    Prevents duplicate reminders by recording when reminders were last sent.
    
    Attributes:
        student: ForeignKey to the User receiving reminders.
        assignment: Optional ForeignKey to an Assignment (if assignment-specific).
        course: Optional ForeignKey to a Course (if course-specific).
        last_reminder_sent_at: Timestamp of the last reminder sent.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    last_reminder_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'assignment')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"