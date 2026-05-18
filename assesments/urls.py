from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import AssignmentView , SubmissionView , send_email , home , QuestionView , QuizView , QuizSubmissionView


router = DefaultRouter()
router.register('assignments',AssignmentView,basename='assignment')
router.register('submissions',SubmissionView,basename='submission')
router.register('questions',QuestionView,basename='question')
router.register('quizes',QuizView,basename='quiz')
router.register('quizesubmission',QuizSubmissionView,basename='quizsubmission')


urlpatterns = [
    path('', home, name='home'),
    path('',include(router.urls)),
    path('send-emails/',send_email,name='send_email'),
    
]
