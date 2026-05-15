from rest_framework.routers import DefaultRouter
from .views import CourseViewset , EnrollmentViewset


router = DefaultRouter()
router.register('',CourseViewset)
router.register('enrollment/',EnrollmentViewset)

urlpatterns = router.urls
