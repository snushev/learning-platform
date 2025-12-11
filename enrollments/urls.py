from rest_framework import routers
from .views import EnrollmentViewSet

router = routers.DefaultRouter()
router.register(r"enrollments", EnrollmentViewSet, basename="enrollments")

urlpatterns = router.urls
