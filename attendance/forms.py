from django import forms
from .models import Student, Attendance, Class
from django.forms import inlineformset_factory

class AttendanceForm(forms.ModelForm):
    """
    A ModelForm for the Attendance model. This form is used to create and update 
    attendance records for students.
    """
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