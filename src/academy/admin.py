from django.contrib import admin
from .models import Student, Course, Enrollment

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('enrolled_at',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'cpf', 'enrollment_date')
    search_fields = ('full_name', 'cpf', 'email')
    list_filter = ('enrollment_date',)
    inlines = [EnrollmentInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'workload_in_hours', 'enrollment_fee', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_at')
    list_filter = ('status', 'enrolled_at')
    search_fields = ('student__full_name', 'course__name')