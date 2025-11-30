from rest_framework.routers import DefaultRouter
from .views import LessonViewset

router = DefaultRouter()
router.register(r"lessons", LessonViewset, basename="lessons")


urlpatterns = router.urls
