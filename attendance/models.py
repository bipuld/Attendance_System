from django.db import models
from django.conf import settings
# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=255)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.CASCADE, 
    #     related_name="students"
    # )
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.name}"
    
class Class(models.Model):
    name=models.CharField(max_length=255)
    students = models.ManyToManyField(Student,related_name='classes',blank=True)
    def __str__(self):
        return f"{self.name}"

class Attendance(models.Model):
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_instance =models.ForeignKey(Class,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])


    def __str__(self):
        return f"{self.student} - {self.date} - {{self.get_status_display()}}"
    

    class Meta:
        unique_together = ('student', 'class_instance', 'date')  # Ensure a student can have only one attendance record per date