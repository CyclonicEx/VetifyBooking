from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, AppointmentForm
from .models import Appointment

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'booking/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'booking/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'booking/home.html')

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Appointment booked for {appointment.pet_name}!')
            return redirect('appointments')
    else:
        form = AppointmentForm()
    
    return render(request, 'booking/booking.html', {'form': form})

@login_required
def appointments_view(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'booking/appointments.html', {'appointments': appointments})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    appointment.delete()
    messages.success(request, 'Appointment deleted successfully!')
    return redirect('appointments')