from django.urls import path
from .views import AdminDashboardView , SponsorDashboardView

urlpatterns = [
    path('',AdminDashboardView.as_view(),name='admin-dashboard'),
    path('',SponsorDashboardView.as_view(),name='sponsor-dashboard'),
]