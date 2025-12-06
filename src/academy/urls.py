from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    financial_report_api,
)

router = DefaultRouter()
router.register(r'alunos', StudentViewSet)
router.register(r'cursos', CourseViewSet)
router.register(r'matriculas', EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    path(
        'api/relatorios/financeiro/',
        financial_report_api,
        name='api_relatorio_financeiro',
    ),
]
