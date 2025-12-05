from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Student, Course, Enrollment

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_fee = serializers.DecimalField(source='course.enrollment_fee', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name',
            'course', 'course_name', 'course_fee',
            'status', 'enrolled_at'
        ]
        read_only_fields = ['enrolled_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Enrollment.objects.all(),
                fields=['student', 'course'],
                message="Este aluno já está matriculado neste curso."
            )
        ]

    def validate(self, data):
       
        if 'course' in data and not data['course'].is_active:
            raise serializers.ValidationError("Não é possível matricular em um curso inativo.")
        return data