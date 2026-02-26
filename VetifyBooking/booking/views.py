from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, AppointmentForm
from .models import Appointment
from django.utils import timezone

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
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Appointment booked for {appointment.pet.name}!')
            return redirect('appointments')
    else:
        form = AppointmentForm(user=request.user)

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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pet, Appointment

@login_required
def profile_view(request):
    """Vista del perfil de usuario con sus mascotas"""
    pets = Pet.objects.filter(owner=request.user)
    appointments_count = Appointment.objects.filter(user=request.user).count()
    
    # Próxima cita
    next_appointment = Appointment.objects.filter(
        user=request.user,
        date__gte=timezone.now().date()
    ).order_by('date', 'time').first()
    
    context = {
        'pets': pets,
        'appointments_count': appointments_count,
        'next_appointment': next_appointment,
        'pets_count': pets.count(),
    }
    return render(request, 'booking/profile.html', context)


@login_required
def register_pet_view(request):
    """Vista para registrar una nueva mascota"""
    if request.method == 'POST':
        # Crear nueva mascota
        pet = Pet(owner=request.user)
        
        # Información básica
        pet.name = request.POST.get('pet_name')
        pet.pet_type = request.POST.get('pet_type')
        pet.other_type = request.POST.get('other_type', '')
        
        # Características físicas
        pet.breed = request.POST.get('breed', '')
        pet.color = request.POST.get('color', '')
        pet.age = request.POST.get('age', 0)
        pet.weight = request.POST.get('weight', 0)
        
        # Información de salud
        pet.vaccination_status = request.POST.get('vaccination', 'updated')
        pet.allergies = request.POST.get('allergies', '')
        
        # Comportamiento
        pet.friendly_with_people = request.POST.get('friendly_people') == 'on'
        pet.friendly_with_animals = request.POST.get('friendly_animals') == 'on'
        pet.nervous_at_vet = request.POST.get('nervous') == 'on'
        pet.special_care = request.POST.get('special_care') == 'on'
        
        # Contacto de emergencia
        pet.emergency_contact_name = request.POST.get('emergency_name', '')
        pet.emergency_contact_phone = request.POST.get('emergency_phone', '')
        
        # Foto
        if 'photo' in request.FILES:
            pet.photo = request.FILES['photo']
        
        pet.save()
        messages.success(request, f'¡{pet.name} ha sido registrado exitosamente! 🎉')
        return redirect('profile')
    
    return render(request, 'booking/register_pet.html')


@login_required
def edit_pet_view(request, pet_id):
    """Vista para editar una mascota existente"""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    
    if request.method == 'POST':
        # Actualizar información
        pet.name = request.POST.get('pet_name')
        pet.pet_type = request.POST.get('pet_type')
        pet.other_type = request.POST.get('other_type', '')
        pet.breed = request.POST.get('breed', '')
        pet.color = request.POST.get('color', '')
        pet.age = request.POST.get('age', 0)
        pet.weight = request.POST.get('weight', 0)
        pet.vaccination_status = request.POST.get('vaccination', 'updated')
        pet.allergies = request.POST.get('allergies', '')
        pet.friendly_with_people = request.POST.get('friendly_people') == 'on'
        pet.friendly_with_animals = request.POST.get('friendly_animals') == 'on'
        pet.nervous_at_vet = request.POST.get('nervous') == 'on'
        pet.special_care = request.POST.get('special_care') == 'on'
        pet.emergency_contact_name = request.POST.get('emergency_name', '')
        pet.emergency_contact_phone = request.POST.get('emergency_phone', '')
        
        if 'photo' in request.FILES:
            pet.photo = request.FILES['photo']
        
        pet.save()
        messages.success(request, f'¡{pet.name} ha sido actualizado exitosamente!')
        return redirect('profile')
    
    context = {'pet': pet}
    return render(request, 'booking/register_pet.html', context)


@login_required
def delete_pet_view(request, pet_id):
    """Vista para eliminar una mascota"""
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet_name = pet.name
    pet.delete()
    messages.success(request, f'{pet_name} ha sido eliminado.')
    return redirect('profile')

from django.shortcuts import render
from .models import Service, Veterinarian, ClinicSchedule

# ... tus otras vistas existentes ...

def schedules_view(request):
    """Vista para mostrar horarios, servicios y veterinarios"""
    # Obtener todos los datos
    services = Service.objects.filter(is_active=True)
    veterinarians = Veterinarian.objects.filter(is_active=True)
    clinic_schedules = ClinicSchedule.objects.all().order_by('day_of_week')
    
    # Organizar horarios de clínica
    schedule_dict = {}
    day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    for schedule in clinic_schedules:
        schedule_dict[schedule.day_of_week] = schedule
    
    # Crear lista ordenada de horarios
    ordered_schedules = []
    for day in day_order:
        if day in schedule_dict:
            ordered_schedules.append(schedule_dict[day])
    
    context = {
        'services': services,
        'veterinarians': veterinarians,
        'clinic_schedules': ordered_schedules,
        'services_count': services.count(),
        'vets_count': veterinarians.count(),
    }
    
    return render(request, 'booking/schedules.html', context)