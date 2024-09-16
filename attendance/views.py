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

@login_required
def attendance_submission_class(request):
    return render(request, 'attendance/att_entry.html')
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

@login_required
def attendance_submission(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)

    # Define the formset for Attendance with extra=1 to ensure there's one empty form on load
    AttendanceFormSet = inlineformset_factory(
        Class, Attendance, 
        form=AttendanceForm, 
        extra=1,  # Show one empty form by default
        can_delete=True
    )

    if request.method == 'POST':
       
        formset = AttendanceFormSet(request.POST, instance=class_instance, form_kwargs={'class_instance': class_instance})
        
        if formset.is_valid():
            # Save valid data
            print(formset)
            formset.save()
            messages.success(request, 'Attendance submitted successfully.')
            return redirect('attendance_submission', class_id=class_instance.id)
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        formset = AttendanceFormSet(instance=class_instance, form_kwargs={'class_instance': class_instance})

    context = {
        'class_instance': class_instance,
        'formset': formset
    }
    return render(request, 'attendance/att_entry.html', context)
