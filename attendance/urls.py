from django.urls import path
from . import views

urlpatterns = [
    # path('attendance/', views.attendance_submission, name='attendance_submission'),
    # path('report/', views.AttendanceReportView.as_view(), name='attendance_report'),
    path('', views.home, name='home')
]
