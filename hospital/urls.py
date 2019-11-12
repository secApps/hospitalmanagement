from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('user_list/', views.user_list_view)
]
