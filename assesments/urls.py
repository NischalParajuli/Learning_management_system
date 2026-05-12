from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import AssignmentView , SubmissionView , send_email , home


router = DefaultRouter()
router.register('assignments',AssignmentView,basename='assignment')
router.register('submissions',SubmissionView,basename='submission')


urlpatterns = [
    path('', home, name='home'),
    path('',include(router.urls)),
    path('send-emails/',send_email,name='send_email'),
]
