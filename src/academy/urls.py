from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
