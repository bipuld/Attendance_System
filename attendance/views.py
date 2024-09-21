from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from attendance.serializers.attendance_serializer import AttendanceSerializer
from .forms import *
from .models import *
from django.urls import reverse
from django.utils.http import urlencode
# Create your views here.
@login_required
def home(request):
    return render(request, 'attendance/home.html')


@method_decorator(login_required, name='dispatch')
class StudentView(CreateView):
    model = Student
    form_class = StudentCreationForm
    template_name = 'attendance/student.html' 
    success_url = reverse_lazy('student') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_list'] = Student.objects.filter(created_by=self.request.user)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)





@method_decorator(login_required, name='dispatch')
class StudentEditView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentCreationForm
    template_name = 'attendance/student_edit.html'
    success_url = reverse_lazy('student')

    def get_object(self):
        student = get_object_or_404(Student, id=self.kwargs.get('pk'))
        # print(student.created_by, self.request.user)
        if student.created_by != self.request.user:
            messages.error(self.request, 'You do not have permission to edit this student.')
            raise PermissionDenied

        return student
        
    def get_form_kwargs(self):

        kwargs = super(StudentEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Student updated successfully.')
        return response


@method_decorator(login_required, name='dispatch')
class StudentDeleteView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        if student.created_by == request.user:
            student.delete()
            messages.success(request, 'Student deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this student.')
            raise PermissionDenied
        return redirect('student')  


@method_decorator(login_required, name='dispatch')
class ClassView(CreateView):
    model = Class
    form_class = ClassCreationForm
    template_name = 'attendance/class.html'
    success_url = reverse_lazy('class')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_list'] = Class.objects.filter(created_by=self.request.user)
        return context
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
@login_required
def class_delete(request, pk):
    try:
        if Class.objects.get(id=pk).created_by != request.user:
            messages.error(request, 'You do not have permission to delete this class.')
            raise PermissionDenied
        class_instance = Class.objects.get(id=pk)
        class_instance.delete()
        messages.success(request, 'Class deleted successfully.')
    except Class.DoesNotExist:
        messages.error(request, 'Class not found.')
    return redirect('class')

@login_required
def class_edit(request, pk):
    class_instance = get_object_or_404(Class, id=pk)
    if class_instance.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this class.')
        raise PermissionDenied

    if request.method == 'POST':
        form = ClassCreationForm(request.POST, instance=class_instance, request=request)
    else:
        form = ClassCreationForm(instance=class_instance, request=request)

    if form.is_valid():
        form.save()
        messages.success(request, 'Class updated successfully.')
        return redirect('class') 
    return render(request, 'attendance/class_edit.html', {'form': form, 'class': class_instance})

# class selection view
@login_required
def class_selection(request):
    class_list=Class.objects.filter(created_by=request.user)
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        return redirect('attendance_submission', class_id=class_id)
    context = {
        'list':class_list
        }
    return render(request, 'attendance/class_select.html', context)


@login_required
def class_attendance(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    if class_instance.created_by != request.user:
        messages.error(request, 'You do not have permission to submit attendance for this class.')
        raise PermissionDenied
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
        # print(request.POST)
        i=0
        form_data=request.POST
        std_data=[]
        while True:
            student_key=f'form-{i}-student'
            date_key=f'form-{i}-date'
            status_key=f'form-{i}-status'

            if student_key in form_data and date_key in form_data and status_key in form_data:
                student_id=form_data[student_key]
                date=form_data[date_key]
                status=form_data[status_key]
                std_data.append({'student':student_id,'date':date,'status':status}) # append the data to the list of dictionaries 
                i+=1
            else:
                break
        for data in std_data:
            student_id=data['student']
            date=data['date']
            status=data['status']
            try:
                student_instance = Student.objects.get(pk=student_id)
                if date:
                    Attendance.objects.update_or_create(
                        student=student_instance,
                        class_instance=class_instance,
                        date=date,
                        status=status
                    )
                else:
                    messages.error(request, "Date is required for all attendance records.")
                    return redirect('attendance_submission', class_id=class_id)
            except Student.DoesNotExist:
                messages.error(request, f"Student with ID {student_id} does not exist.")
                return redirect('attendance_submission', class_id=class_id)
            
        return redirect('home')

    context = {
        'class_instance': class_instance,
        'students': class_instance.students.all(),
        'status_choices': Attendance.status_choices,
        'attendance_records': attendance_records
    }
    
    return render(request, 'attendance/attendance_submit.html', context)


@login_required
def attendance_delete(request, pk):
    try:
        class_id=Attendance.objects.get(id=pk).class_instance
        if class_id.created_by != request.user:
            messages.error(request, 'You do not have permission to delete this attendance.')
            raise PermissionDenied
        attendance = Attendance.objects.get(id=pk)
        attendance.delete()
        messages.success(request, 'Attendance deleted successfully.')
        return redirect('attendance_submission', class_id=class_id.id)
    except Attendance.DoesNotExist:
        messages.error(request, 'Attendance not found.')
    return redirect('home')



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


@login_required
def report_class(request):
    class_list = Class.objects.filter(created_by=request.user)
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        if class_id:
                url = reverse('report', kwargs={'pk': class_id})
                return redirect(url)
        else:
            messages.error(request, 'No class selected.')
    context = {
        'list': class_list
    }
    return render(request, 'attendance/report_class.html', context)


@method_decorator(login_required, name='dispatch')
class ReportGenerate(View):
    def get(self, request, pk):
        class_data = get_object_or_404(Class, id=pk)
        if class_data.created_by != request.user:
            messages.error(request, 'You do not have permission to view this report.')
            raise PermissionDenied
        attendance_records = class_data.attendance_set.all()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
     
        if start_date and end_date:
            attendance_records = class_data.attendance_set.filter(date__range=[start_date, end_date]).select_related('student')
        else:
            attendance_records = class_data.attendance_set.all()
        serializer_data=AttendanceSerializer(attendance_records, many=True).data

        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        # print(serializer_data,"The JSON data")
        context = {
            'class': class_data,
            'students': class_data.students.all(),
            'attendance_records': attendance_records,
            'start_date': start_date,
            'end_date': end_date,
            'serialized_data':serializer_data,
            'present_count': present_count,
            'absent_count': absent_count
        }
        return render(request, 'attendance/report.html', context)
    
    def post(self, request, pk):
        pass
        # class_instance = get_object_or_404(Class, id=pk)
        # start_date = request.POST.get('start_date')
        # end_date = request.POST.get('end_date')
        # if start_date and end_date:
        #     attendance_records = class_instance.attendance_set.filter(date__range=[start_date, end_date])
        # else:
        #     attendance_records = class_instance.attendance_set.all()
        # # API call to generate the report
        # serialized_records=AttendanceSerializer(attendance_records, many=True).data
        # # print(attendance_records.data)

        # context = {
        #     'class': class_instance,
        #     'students': class_instance.students.all(),
        #     'attendance_records': serialized_records 
        # }
        # return render(request, 'attendance/report.html', context)


class WeeklyReport(LoginRequiredMixin, View):
    def generate_report(self, selected_class, start_date, end_date):
        attendance_records = Attendance.objects.filter(
            class_instance=selected_class,
            date__range=[start_date, end_date]
        )
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        print(attendance_records, "The attendance records are weekly")
        return attendance_records, present_count, absent_count

    def get(self, request):
        class_data = Class.objects.filter(created_by=request.user)
        selected_class_id = request.GET.get('class_id')
        attendance_records = None
        present_count = absent_count = 0
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)

        if selected_class_id:
            try:
                selected_class = Class.objects.get(id=selected_class_id)
                attendance_records, present_count, absent_count = self.generate_report(
                    selected_class, start_date, end_date
                )
            except Class.DoesNotExist:
                messages.error(request, 'Class not found.')

        context = {
            'attendance_records': attendance_records,
            'start_date': start_date,
            'end_date': end_date,
            'class_data': class_data,
            'selected_class_id': selected_class_id,
            'present_count': present_count,
            'absent_count': absent_count,
        }

        return render(request, 'attendance/weekly_report.html', context)

class MonthlyReport(LoginRequiredMixin, View):
    def generate_report(self, selected_class, start_date, end_date):
        attendance_records = Attendance.objects.filter(
            class_instance=selected_class,
            date__range=[start_date, end_date]
        )
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()

        return attendance_records, present_count, absent_count

    def get(self, request):
        class_data = Class.objects.filter(created_by=request.user)
        selected_class_id = request.GET.get('class_id')
        attendance_records = None
        present_count = absent_count = 0
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)

        if selected_class_id:
            try:
                selected_class = Class.objects.get(id=selected_class_id)
                attendance_records, present_count, absent_count = self.generate_report(
                    selected_class, start_date, end_date
                )
            except Class.DoesNotExist:
                messages.error(request, 'Class not found.')

        context = {
            'attendance_records': attendance_records,
            'start_date': start_date,
            'end_date': end_date,
            'class_data': class_data,
            'selected_class_id': selected_class_id,
            'present_count': present_count,
            'absent_count': absent_count,
        }

        return render(request, 'attendance/weekly_report.html', context)
# @login_required
# def report_generate_date(request, pk):
#     class_instance = get_object_or_404(Class, id=pk)
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     if start_date and end_date:
#         attendance_records = class_instance.attendance_set.filter(date__range=[start_date, end_date])
#     else:
#         attendance_records = class_instance.attendance_set.all()
#     present_count = attendance_records.filter(status='Present').count()
#     absent_count = attendance_records.filter(status='Absent').count()
#     context = {
#         'class': class_instance,
#         'students': class_instance.students.all(),
#         'attendance_records': attendance_records,
#         'start_date': start_date,
#         'end_date': end_date,
#         'present_count': present_count,
#         'absent_count': absent_count
#     }
#     return render(request, 'attendance/report.html', context