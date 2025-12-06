from django.db.models import Count, Sum, Q

from rest_framework import viewsets, decorators, response

from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course')
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

    @decorators.action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        enrollment = self.get_object()
        enrollment.status = Enrollment.Status.PAID
        enrollment.save()
        return response.Response({'status': 'Matrícula marcada como paga'})


@decorators.api_view(['GET'])
def financial_report_api(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()

    stats = Enrollment.objects.aggregate(
        total_paid=Count('id', filter=Q(status=Enrollment.Status.PAID)),
        total_pending=Count('id', filter=Q(status=Enrollment.Status.PENDING)),
        revenue_potential=Sum('course__enrollment_fee'),
    )

    data = {
        'summary': {
            'students': total_students,
            'courses': total_courses,
            'enrollments_paid': stats['total_paid'],
            'enrollments_pending': stats['total_pending'],
            'gross_revenue_potential': stats['revenue_potential'] or 0.00,
        }
    }
    return response.Response(data)
