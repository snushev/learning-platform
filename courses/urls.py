from rest_framework.routers import DefaultRouter
from .views import CourseViewset, CategoryViewset

router = DefaultRouter()
router.register(r"courses", CourseViewset, basename="courses")
router.register(r"categories", CategoryViewset, basename="categories")

urlpatterns = router.urls
