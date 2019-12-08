from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('user_list/', views.user_list),
    path('patient_list/', views.patient_list),
    path('appointment_list/', views.appointment_list),
    path('doctor_appointment_list/', views.doctor_appointment_list),
    path('todo_diagnosis_report_for_diagnostician/', views.todo_diagnosis_report_for_diagnostician),
    path('update_user/', views.update_user),
    path('update_prescription/', views.update_prescription),
    path('add_people/', views.add_people),
    path('update_appointments/', views.update_appointments),
    path('medicine_list/', views.medicine_list),
    path('doctor_list/', views.doctor_list),
    path('diagnosis_list/', views.diagnosis_list),
    path('role_list/', views.role_list),
    path('create/', views.create_user_view),
    path('update/<int:pk>', views.update_user_view),
    path('read/<int:pk>', views.read_user_view, name='read_user'),
    path('delete/<int:pk>', views.delete_user_view)
]
