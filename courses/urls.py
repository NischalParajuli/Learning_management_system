from rest_framework.routers import DefaultRouter
from .views import CourseViewset


router = DefaultRouter()
router.register('',CourseViewset)

urlpatterns = router.urls
