from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SponsorshipViewset ,  CourseSponsorViewset

router = DefaultRouter()
router.register('sponsorship',SponsorshipViewset,basename='sponsorship')
router.register('coursesponsor', CourseSponsorViewset , basename='coursesponsor')


urlpatterns = [

  path('',include(router.urls))



]