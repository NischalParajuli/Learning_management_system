"""Serializers for assignment, submission, quiz, and quiz submission models."""

import json
from django.utils import timezone
from rest_framework import serializers
from .models import Assignment, Submission, Quiz, Question, QuizSubmission
from courses.models import Enrollment


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializes Assignment model instances to/from JSON.
    
    Converts Assignment objects to JSON for API responses and vice versa.
    """
    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializes Submission model instances to/from JSON.
    
    Handles submission creation, validation, and updates with role-based
    access control. Hides grades/feedback from students, enforces deadlines,
    and prevents duplicate submissions.
    """
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'content', 'feedback', 'grade', 'status', 'submitted_at']
        read_only_fields = ['student', 'status']

    def to_representation(self, instance):
        """Hide grade and feedback from students."""
        data = super().to_representation(instance) # converts model objects to dictionary
        request = self.context.get('request')
        if request is not None and hasattr(request, 'user') and request.user.is_authenticated: # safety check 
            if request.user.role == 'student':
                data.pop('feedback', None)
                data.pop('grade', None)
        return data

    def validate(self, data):
        """Validate submission data based on user role and enrollment.
        
        Ensures students are enrolled in the course, haven't already submitted,
        and don't attempt to set restricted fields like grade/feedback.
        
        Args:
            data: Data to validate.
        
        Returns:
            dict: Validated data.
            
        Raises:
            ValidationError: If validation fails.
        """
        request = self.context.get('request')
        user = request.user

        if not data.get('assignment'):
            raise serializers.ValidationError({"assignment": "Required"})

        assignment = data.get('assignment')

        if user.role == 'student':
            enrolled_courses = Enrollment.objects.filter(
                student=user
            ).values_list('course', flat=True)

            if assignment.course_id not in enrolled_courses:
                raise serializers.ValidationError(
                    {'assignment': 'You are not enrolled in this course.'}
                )

            if Submission.objects.filter(student=user, assignment=assignment).exists():
                raise serializers.ValidationError(
                    {'assignment': 'You have already submitted this assignment.'}
                )

            forbidden = ['grade', 'feedback', 'status']
            for field in forbidden:
                if data.get(field):
                    raise serializers.ValidationError(
                        {field: f'Students are not allowed to set {field}.'}
                    )

        return data

    def create(self, validated_data):
        """Create a new submission.
        
        Sets the current user as the student and automatically marks submissions
        as 'late' if submitted past the assignment deadline.
        
        Args:
            validated_data: Validated submission data.
        
        Returns:
            Submission: The newly created submission object.
        """
        request = self.context['request']
        assignment = validated_data.get('assignment')

        validated_data['student'] = request.user

        if timezone.now() > assignment.due_date:
            validated_data['status'] = 'late'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an existing submission with role-based permissions.
        
        Students can only edit their own submissions before deadline.
        Instructors can only grade submissions for their courses.
        Admins can modify any submission.
        
        Args:
            instance: The submission being updated.
            validated_data: Validated update data.
        
        Returns:
            Submission: The updated submission object.
            
        Raises:
            ValidationError: If user lacks permission or deadline has passed.
        """
        request = self.context['request']
        user = request.user

        if user.role == 'student':
            if user != instance.student:
                raise serializers.ValidationError("You cannot edit this submission")
            if timezone.now() > instance.assignment.due_date:
                raise serializers.ValidationError("Deadline passed: You cannot edit this")
            validated_data.pop('grade', None)
            validated_data.pop('feedback', None)
            validated_data.pop('status', None)

        elif user.role == 'instructor':
            if instance.assignment.course.instructor != user:
                raise serializers.ValidationError("You cannot grade this submission")
            validated_data.pop('content', None)
            validated_data['status'] = 'grd'

        elif user.role == 'admin':
            pass

        return super().update(instance, validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializes Question model instances to/from JSON.
    
    Hides the correct answer from students to prevent cheating.
    Only instructors and admins can see the correct answer.
    """
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question', 'opt1', 'opt2', 'opt3', 'opt4', 'correct_answer']

    def to_representation(self, instance):
        """Hide correct_answer from students."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.role == 'student':
                data.pop('correct_answer', None)
        return data


class QuizSerializer(serializers.ModelSerializer):
    """Serializes Quiz model instances to/from JSON.
    
    Includes nested questions with proper context-aware visibility of answers.
    Validates that instructors only create quizzes for their own courses.
    """
    quiz_questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'instructor', 'created_at', 'quiz_questions']
        read_only_fields = ['instructor', 'created_at']

    def get_quiz_questions(self, obj):
        """Return nested questions, passing request context so correct_answer is hidden for students."""
        return QuestionSerializer(
            obj.questions.all(),
            many=True,
            context=self.context,
        ).data

    def validate_course(self, course):
        """Ensure instructors only create quizzes for their own courses.
        
        Args:
            course: The course object being validated.
        
        Returns:
            Course: The validated course object.
            
        Raises:
            ValidationError: If instructor tries to create quiz for another instructor's course.
        """
        request = self.context.get('request')
        if request is not None and request.user.role == 'instructor':
            if course.instructor != request.user:
                raise serializers.ValidationError(
                    "You can only create quizzes for your own courses."
                )
        return course


class QuizSubmissionSerializer(serializers.ModelSerializer):
    """Serializes QuizSubmission model instances to/from JSON.
    
    Handles quiz submission with answer validation, scoring, and duplicate
    submission prevention. Accepts answers as JSON string mapping question IDs
    to answers (A, B, C, or D).
    """
    # Accepts a JSON string: e.g. {"4": "A", "5": "B", "6": "C"}
    answers = serializers.CharField(write_only=True)

    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'student', 'score', 'submitted_at', 'answers']
        read_only_fields = ['student', 'score', 'submitted_at']

    def validate(self, data):
        """Validate quiz submission answers and quiz requirements.
        
        Ensures:
        - Quiz is provided
        - Student hasn't already submitted this quiz
        - Answers are valid JSON format
        - All answers are A, B, C, or D
        - All questions are answered
        - No extra questions are answered
        
        Args:
            data: Data to validate.
        
        Returns:
            dict: Validated data with parsed answers.
            
        Raises:
            ValidationError: If validation fails.
        """
        request = self.context.get('request')
        user = request.user
        quiz = data.get('quiz')

        if not quiz:
            raise serializers.ValidationError({"quiz": "Required."})

        if QuizSubmission.objects.filter(student=user, quiz=quiz).exists():
            raise serializers.ValidationError(
                {"quiz": "You have already submitted this quiz."}
            )

        # Parse answers from JSON string
        raw_answers = data.get('answers', '{}') # converts raaw answers to python dictionary
        if isinstance(raw_answers, str):
            try:
                answers = json.loads(raw_answers)
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    {"answers": 'Must be valid JSON. Example: {"4": "A", "5": "B", "6": "C"}'}
                )
        else:
            answers = raw_answers

        # Validate answer values are A/B/C/D
        valid_choices = {'A', 'B', 'C', 'D'}
        for key, val in answers.items():
            if val not in valid_choices:
                raise serializers.ValidationError(
                    {"answers": f'Invalid value "{val}" for question {key}. Must be A, B, C, or D.'}
                )

        question_ids = set(quiz.questions.values_list('id', flat=True))
        provided_ids = set(int(k) for k in answers.keys())

        missing = question_ids - provided_ids
        if missing:
            raise serializers.ValidationError(
                {"answers": f"Missing answers for question id(s): {sorted(missing)}."}
            )

        extra = provided_ids - question_ids
        if extra:
            raise serializers.ValidationError(
                {"answers": f"Unknown question id(s): {sorted(extra)}."}
            )

        data['answers'] = answers
        return data

    def create(self, validated_data):
        """Create a new quiz submission with automatic scoring.
        
        Compares student answers against correct answers and calculates score.
        Sets current user as the student submitting the quiz.
        
        Args:
            validated_data: Validated submission data including answers.
        
        Returns:
            QuizSubmission: The newly created quiz submission with calculated score.
        """
        answers = validated_data.pop('answers')
        quiz = validated_data['quiz']
        request = self.context['request']

        score = sum(
            1 for question in quiz.questions.all()
            if answers.get(str(question.id)) == question.correct_answer
        )

        validated_data['student'] = request.user
        validated_data['score'] = score

        return super().create(validated_data)