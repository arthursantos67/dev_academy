from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Student(TimestampedModel):
    full_name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    enrollment_date = models.DateField(verbose_name="Data de Ingresso")

    def __str__(self):
        return f"{self.full_name} ({self.cpf})"

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['full_name']


class Course(TimestampedModel):
    name = models.CharField(max_length=255, verbose_name="Nome do Curso")
    workload_in_hours = models.PositiveIntegerField(verbose_name="Carga Horária (h)")
    enrollment_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inscrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class Enrollment(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pendente')
        PAID = 'paid', _('Pago')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status Pagamento"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Matrícula")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}"

    @property
    def is_paid(self):
        return self.status == self.Status.PAID
