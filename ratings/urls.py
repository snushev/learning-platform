from rest_framework.routers import DefaultRouter
from .views import CourseRatingViewset

router = DefaultRouter()
router.register(r"ratings", CourseRatingViewset, basename="ratings")

urlpatterns = router.urls
