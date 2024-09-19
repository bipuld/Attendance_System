from django import forms
from .models import Student, Attendance, Class
from django.forms import inlineformset_factory


from django import forms
from .models import Attendance, Class



class AttendanceForm(forms.ModelForm):
    """
    A ModelForm for the Attendance model. This form is used to create and update
    attendance records for students.
    """
    def __init__(self, *args, **kwargs):
        class_instance = kwargs.pop('class_instance', None)
        super().__init__(*args, **kwargs)
        if class_instance:
            self.fields['student'].queryset = class_instance.students.all()

    class Meta:
        model = Attendance
        fields = ['id','student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.RadioSelect,
        }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        date = cleaned_data.get('date')
        class_instance = self.instance.class_instance

        if student and date and class_instance:
            if Attendance.objects.filter(student=student, date=date, class_instance=class_instance).exists():
                raise forms.ValidationError(f"Attendance for {student} on {date} already exists.")
        return cleaned_data

AttendanceFormSet = inlineformset_factory(
    Class,
    Attendance,
    form=AttendanceForm,
    extra=1,
    can_delete=True
)

class StudentCreationForm(forms.ModelForm):
    """
    A ModelForm for the Student model. This form is used to create and update student records.
    """
    class Meta:
        model = Student
        fields = ['student_id', 'name']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student ID',
                'style': 'width: 100%; padding: 10px; border-radius: 4px;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Name',
                'style': 'width: 100%; padding: 10px; border-radius: 4px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        if not self.request:
            raise ValueError("Request object is missing in StudentCreationForm")
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['student_id'].widget.attrs['readonly'] = True
            self.fields['student_id'].widget.attrs['class'] = 'form-control-plaintext'
            self.fields['student_id'].widget.attrs['style'] = 'width: 100%; padding: 10px; border-radius: 4px; background-color: #e9ecef;'

    def clean_student_id(self):
        manager = self.request.user
        student_id = self.cleaned_data.get('student_id')
        
        if not self.instance.pk and Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError(f"Student with ID {student_id} already exists for this user.")
        
        return student_id



class ClassCreationForm(forms.ModelForm):
    """
    A ModelForm for the Class model. This form is used to create and update class records.
    """
    class Meta:
        model = Class
        fields = ['name', 'students']
        widgets = {
            'students': forms.SelectMultiple(attrs={
                'class': 'form-control select-multiple',
                'style': 'width: 100%; padding: 10px; border-radius: 4px; min-height: 150px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        if not self.request:
            raise ValueError("Request object is missing in ClassCreationForm")
        super(ClassCreationForm, self).__init__(*args, **kwargs)
        owner = self.request.user

        if self.instance and self.instance.pk:
            self.fields['name'].widget.attrs.update({
                'readonly': True,
                'class': 'form-control-plaintext',
                'style': 'width: 100%; padding: 10px; border-radius: 4px; background-color: #e9ecef;'
            })

            enrolled_students_ids = Student.objects.filter(
                created_by=owner, classes__isnull=False
            ).values_list('id', flat=True)
            
            current_class_students_ids = self.instance.students.values_list('id', flat=True)
            
            students_not_in_other_classes = Student.objects.filter(
                created_by=owner
            ).exclude(id__in=enrolled_students_ids)
            
            students_in_current_class = Student.objects.filter(id__in=current_class_students_ids)

            combined_students = students_in_current_class | students_not_in_other_classes
            self.fields['students'].queryset = combined_students.distinct()
        
        else:
            enrolled_students_ids = Student.objects.filter(
                created_by=owner, classes__isnull=False
            ).values_list('id', flat=True)
            self.fields['students'].queryset = Student.objects.filter(
                created_by=owner
            ).exclude(id__in=enrolled_students_ids)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        owner = self.request.user
        if self.instance.pk:
            if Class.objects.filter(created_by=owner,name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A class with this name already exists.")
        else:
            if Class.objects.filter(name=name,created_by=owner).exists():
                raise forms.ValidationError("A class with this name already exists.")
        return name

    def clean_students(self):
        students = self.cleaned_data.get('students')
        if students:
            enrolled_students_ids = Student.objects.filter(classes__isnull=False).values_list('id', flat=True)
            for student in students:
                if student.id in enrolled_students_ids and student not in self.instance.students.all():
                    raise forms.ValidationError(f"Student {student.name} is already enrolled in another class.")
        return students

    def save(self, commit=True):
        instance = super(ClassCreationForm, self).save(commit=False)

        if commit:
            instance.save()

        if commit:
            selected_students = self.cleaned_data.get('students')
            current_students = set(self.instance.students.all())
            new_students = set(selected_students)

            to_remove = current_students - new_students
            for student in to_remove:
                self.instance.students.remove(student)

            to_add = new_students - current_students
            for student in to_add:
                self.instance.students.add(student)

        return instance