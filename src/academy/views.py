from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
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
        revenue_potential=Sum('course__enrollment_fee')
    )
    
    data = {
        'summary': {
            'students': total_students,
            'courses': total_courses,
            'enrollments_paid': stats['total_paid'],
            'enrollments_pending': stats['total_pending'],
            'gross_revenue_potential': stats['revenue_potential'] or 0.00
        }
    }
    return response.Response(data)

def dashboard_view(request):
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'active_courses': Course.objects.filter(is_active=True).count(),
        'enrollments_paid': Enrollment.objects.filter(status=Enrollment.Status.PAID).count(),
        'enrollments_pending': Enrollment.objects.filter(status=Enrollment.Status.PENDING).count(),
    }
    return render(request, 'academy/dashboard.html', context)

def student_history_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    enrollments = (
        Enrollment.objects
        .select_related('course')
        .filter(student=student)
        .order_by('-enrolled_at')
    )

    total_enrollments = enrollments.count()

    total_paid = sum(
        e.course.enrollment_fee
        for e in enrollments
        if e.status == Enrollment.Status.PAID
    )

    total_due = sum(
        e.course.enrollment_fee
        for e in enrollments
        if e.status == Enrollment.Status.PENDING
    )

    context = {
        'student': student,
        'enrollments': enrollments,
        'total_enrollments': total_enrollments,
        'total_paid': total_paid,
        'total_due': total_due,
    }
    return render(request, 'academy/student_history.html', context)


def raw_sql_report_view(request):
    sql_query = """
        SELECT 
            s.full_name as student_name,
            c.name as course_name,
            e.status,
            CASE 
                WHEN e.status = 'paid' THEN c.enrollment_fee 
                ELSE 0 
            END as amount_paid,
            CASE 
                WHEN e.status = 'pending' THEN c.enrollment_fee 
                ELSE 0 
            END as amount_due
        FROM academy_enrollment e
        JOIN academy_student s ON e.student_id = s.id
        JOIN academy_course c ON e.course_id = c.id
        ORDER BY s.full_name;
    """
    sql_summary_query = """
        SELECT
            s.full_name AS student_name,
            SUM(
                CASE WHEN e.status = 'paid' THEN c.enrollment_fee ELSE 0 END
            ) AS total_paid,
            SUM(
                CASE WHEN e.status = 'pending' THEN c.enrollment_fee ELSE 0 END
            ) AS total_due,
            COUNT(*) AS total_enrollments
        FROM academy_enrollment e
        JOIN academy_student s ON e.student_id = s.id
        JOIN academy_course c ON e.course_id = c.id
        GROUP BY s.full_name
        ORDER BY s.full_name;
    """

    results = []
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        for row in rows:
            results.append(dict(zip(columns, row)))
            
    total_paid = sum(item['amount_paid'] for item in results)
    total_due = sum(item['amount_due'] for item in results)
    
    summary_results = []
    with connection.cursor() as cursor:
        cursor.execute(sql_summary_query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            summary_results.append(dict(zip(columns, row)))


    if request.GET.get('format') == 'json':
        return JsonResponse({
            'report': results,
            'totals': {'paid': total_paid, 'due': total_due}
    })

    context = {
        'report_data': results,
        'total_paid': total_paid,
        'total_due': total_due,
        'summary_data': summary_results
    }

    return render(request, 'academy/sql_report.html', context)