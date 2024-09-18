from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.StudentView.as_view(), name='student'),
    path('student/delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('student/edit/<int:pk>/', views.StudentEditView.as_view(), name='edit_student'),
    path('class/', views.ClassView.as_view(), name='class'),
    path('class/delete/<int:pk>/', views.class_delete, name='cls_delete'),
    path('class/edit/<int:pk>/', views.class_edit, name='cls_edit'),
    
    path('class-selection/', views.class_selection, name='class_selection'),
    path('attendance/submit/<int:class_id>/', views.class_attendance, name='attendance_submission'),
    path('attendance/delete/<int:pk>/', views.attendance_delete, name='delete_attendance'),

    path('report_class/', views.report_class, name='report_class'),
    path('report/generate/<int:pk>',views.ReportGenerate.as_view() , name='report'),


    ]
