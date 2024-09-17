from django.urls import path
from . import views

urlpatterns = [
    # path('attendance/', views.attendance_submission, name='attendance_submission'),
    # path('report/', views.AttendanceReportView.as_view(), name='attendance_report'),
    path('', views.home, name='home'),
    path('student/', views.StudentView.as_view(), name='student'),
    path('student/delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('student/edit/<int:pk>/', views.StudentEditView.as_view(), name='edit_student'),
    path('class/', views.ClassView.as_view(), name='class'),
    path('class/delete/<int:pk>/', views.class_delete, name='cls_delete'),
    path('class/edit/<int:pk>/', views.class_edit, name='cls_edit'),
    path('submit/<int:class_id>/', views.class_attendance, name='attendance_submission'),
    path('class-selection/', views.class_selection, name='class_selection'),

    ]
