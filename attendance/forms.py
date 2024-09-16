from django import forms
from .models import Student, Attendance, Class
from django.forms import inlineformset_factory


class AttendanceForm(forms.ModelForm):
    """
    A ModelForm for the Attendance model. This form is used to create and update 
    attendance records for students.
    """
    def __init__(self, *args, **kwargs):
        # Capture the class_instance passed from the view
        class_instance = kwargs.pop('class_instance', None)
        super().__init__(*args, **kwargs)
        
        # Filter the 'student' field by students in the given class_instance
        if class_instance:
            self.fields['student'].queryset = class_instance.students.all()

    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.RadioSelect
        }

class BulkAttendanceForm(forms.Form):

    """
    A basic form for bulk attendance entry. This form allows users to specify
    a date range and the attendance status for bulk updates.
    """
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('present', 'Present'), ('absent', 'Absent')]
    )

# This Formset that allows you to manage multiple Attendance records related to a single Class instance. 
AttendanceFormSet = inlineformset_factory(
    Class, Attendance,
    form=AttendanceForm,  # Form used to create/update Attendance records
    extra=1,  # Number of extra forms to display initially (for adding new records)
    can_delete=True  # Allows deletion of records from the formset
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
                'style': 'width: 100%; padding: 10px; border-radius: 4px;',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Name',
                'style': 'width: 100%; padding: 10px; border-radius: 4px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(StudentCreationForm, self).__init__(*args, **kwargs)
        # Set the student_id field to readonly if it's an existing object
        if self.instance and self.instance.pk:
            self.fields['student_id'].widget.attrs['readonly'] = True
            self.fields['student_id'].widget.attrs['class'] = 'form-control-plaintext'
            self.fields['student_id'].widget.attrs['style'] = 'width: 100%; padding: 10px; border-radius: 4px; background-color: #e9ecef;'

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not self.instance.pk and Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError(f"Student with ID {student_id} already exists")
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
        super(ClassCreationForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['name'].widget.attrs.update({
                'readonly': True,
                'class': 'form-control-plaintext',
                'style': 'width: 100%; padding: 10px; border-radius: 4px; background-color: #e9ecef;'
            })

            
            enrolled_students_ids = Student.objects.filter(classes__isnull=False).values_list('id', flat=True) # Get IDs of students already enrolled in any class
            # print(enrolled_students_ids,"THe enrolled students")
            current_class_students_ids = self.instance.students.values_list('id', flat=True)     # Get IDs of students currently in this class
            students_not_in_other_classes = Student.objects.exclude(id__in=enrolled_students_ids)
            students_in_current_class = Student.objects.filter(id__in=current_class_students_ids)

            # Combine both querysets
            combined_students = students_in_current_class | students_not_in_other_classes
            self.fields['students'].queryset = combined_students.distinct()
        else:
            # For new class, exclude students already enrolled in any class
            enrolled_students_ids = Student.objects.filter(classes__isnull=False).values_list('id', flat=True)
            self.fields['students'].queryset = Student.objects.exclude(id__in=enrolled_students_ids)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.instance.pk:
            if Class.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A class with this name already exists.")
        else:
            if Class.objects.filter(name=name).exists():
                raise forms.ValidationError("A class with this name already exists.")
        return name

    def clean_students(self):
        students = self.cleaned_data.get('students')
        if students:
            enrolled_students_ids = Student.objects.filter(classes__isnull=False).values_list('id', flat=True) # Get IDs of students already enrolled in any class
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