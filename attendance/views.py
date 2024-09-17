from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views import View

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from .models import *

# Create your views here.
@login_required
def home(request):
    return render(request, 'attendance/home.html')

# @login_required
# def attendance_submission_class(request):
#     return render(request, 'attendance/att_entry.html')
@method_decorator(login_required, name='dispatch')
class StudentView(CreateView):
    model = Student
    form_class = StudentCreationForm
    template_name = 'attendance/student.html' 
    success_url = reverse_lazy('student') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        return context
@method_decorator(login_required, name='dispatch')   
class StudentDeleteView(View):
    def get(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
            student.delete()
            messages.success(request, 'Student deleted successfully.')
        except Student.DoesNotExist:
            messages.error(request, 'Student not found.')
        return redirect('student')  # Redirect to the student list view
    
@method_decorator(login_required, name='dispatch')
class StudentEditView(UpdateView):
    model = Student
    form_class = StudentCreationForm
    template_name = 'attendance/student_edit.html'
    success_url = reverse_lazy('student')
    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Student, id=id)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Student updated successfully.')
        return response
    
@method_decorator(login_required, name='dispatch')
class ClassView(CreateView):
    model = Class
    form_class = ClassCreationForm
    template_name = 'attendance/class.html'
    success_url = reverse_lazy('class')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_list'] = Class.objects.all()
        return context
    
@login_required
def class_delete(request, pk):
    try:
        class_instance = Class.objects.get(id=pk)
        class_instance.delete()
        messages.success(request, 'Class deleted successfully.')
    except Class.DoesNotExist:
        messages.error(request, 'Class not found.')
    return redirect('class')

@login_required
def class_edit(request, pk):
    class_instance = get_object_or_404(Class, id=pk)
    form = ClassCreationForm(request.POST or None, instance=class_instance)
 

    if form.is_valid():
        form.save()
        messages.success(request, 'Class updated successfully.')
        return redirect('class')
    
    return render(request, 'attendance/class_edit.html', {'form': form, 'class': class_instance})

# class selection view
@login_required
def class_selection(request):
    class_list=Class.objects.all()
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        return redirect('attendance_submission', class_id=class_id)
    context = {
        'list':class_list
        }
    return render(request, 'attendance/class_select.html', context)



def class_attendance(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        try:
            attendance_records = class_instance.attendance_set.filter(date__range=[start_date, end_date])
        except ValueError:
            attendance_records = class_instance.attendance_set.none()  
    else:
        attendance_records = class_instance.attendance_set.all()

    if request.method == 'POST':
        student_ids = request.POST.getlist('form-0-student')
        dates = request.POST.getlist('dates')
        statuses = request.POST.getlist('form-0-status')

        if len(student_ids) == len(dates) == len(statuses):
            for student_id, date, status in zip(student_ids, dates, statuses):
                try:
                    student_instance = Student.objects.get(pk=student_id)
                    if date:  
                        Attendance.objects.update_or_create(
                            student=student_instance,
                            class_instance=class_instance,
                            date=date,
                            defaults={'status': status}
                        )
                    else:
                        print(f"Date is missing for student ID {student_id}.")
                except Student.DoesNotExist:
                    print(f"Student with ID {student_id} does not exist.")
            return redirect('home')
        else:
            print("Mismatch in the number of student IDs, dates, and statuses.")

    context = {
        'class_instance': class_instance,
        'students': class_instance.students.all(),
        'status_choices': Attendance.status_choices,
        'attendance_records': attendance_records
    }
    
    return render(request, 'attendance/attendance_submit.html', context)

# @login_required
# def class_attendance(request, class_id):
#     class_instance = get_object_or_404(Class, id=class_id)

#     # if request.method == 'POST':
#     #     formset = AttendanceFormSet(request.POST, instance=class_instance, form_kwargs={'class_instance': class_instance})
#     #     if formset.is_valid():
#     #         formset.save()
#     #         return redirect('home')
#     #     else:
#     #         print(formset.errors)
#     # else:
#     #     formset = AttendanceFormSet(instance=class_instance, form_kwargs={'class_instance': class_instance})

#     # context = {
#     #     'formset': formset,
#     #     'class_instance': class_instance
#     # }

#     class_instance = get_object_or_404(Class, id=class_id)
#     choice_status=Attendance.status_choices
    
#     context={
#         'student_att':class_instance.students.all(),
#         'class_instance':class_instance,
#         'status_choices':choice_status
#     }
    
#     return render(request, 'attendance/attendance_submit.html', context)