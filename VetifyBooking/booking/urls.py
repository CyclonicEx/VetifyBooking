from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/', views.booking_view, name='booking'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]