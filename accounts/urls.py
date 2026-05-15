from django.urls import path
from .views import RegisterView


"""Controls the register view"""
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
]
