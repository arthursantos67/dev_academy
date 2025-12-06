from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reports/financial/', views.financial_report_api, name='api_financial_report'),
    path('api/reports/raw-sql/', views.raw_sql_report_view, name='api_raw_sql'),

    path('', views.dashboard_view, name='dashboard'),
    path('relatorios/financeiro/', views.raw_sql_report_view, name='relatorio_financeiro'),
    path('alunos/<int:student_id>/historico/', views.student_history_view, name='historico_aluno'),
]
