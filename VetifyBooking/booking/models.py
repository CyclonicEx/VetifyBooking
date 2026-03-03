from django.db import models
from django.contrib.auth.models import User


# =========================
#        PET MODEL
# =========================
class Pet(models.Model):
    PET_TYPE_CHOICES = [
        ('dog', 'Perro'),
        ('cat', 'Gato'),
        ('other', 'Otro'),
    ]

    VACCINATION_STATUS_CHOICES = [
        ('updated', 'Al día'),
        ('pending', 'Pendiente'),
        ('none', 'Sin vacunas'),
    ]

    # Relación con usuario
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    # Información básica
    name = models.CharField(max_length=100, verbose_name="Nombre")
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES, verbose_name="Tipo")
    other_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Especificar tipo")

    # Características físicas
    breed = models.CharField(max_length=100, blank=True, verbose_name="Raza")
    color = models.CharField(max_length=50, blank=True, verbose_name="Color")
    age = models.IntegerField(verbose_name="Edad (años)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso (kg)")

    # Salud
    vaccination_status = models.CharField(
        max_length=10,
        choices=VACCINATION_STATUS_CHOICES,
        default='updated',
        verbose_name="Estado de vacunación"
    )
    allergies = models.TextField(blank=True, verbose_name="Alergias o condiciones médicas")

    # Comportamiento
    friendly_with_people = models.BooleanField(default=True)
    friendly_with_animals = models.BooleanField(default=True)
    nervous_at_vet = models.BooleanField(default=False)
    special_care = models.BooleanField(default=False)

    # Emergencia
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    # Foto
    photo = models.ImageField(upload_to='pets/', blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_pet_type_display()})"

    def get_emoji(self):
        emojis = {
            'dog': '🐕',
            'cat': '🐈',
            'other': '🐰'
        }
        return emojis.get(self.pet_type, '🐾')

    def get_last_appointment(self):
        return self.appointments.order_by('-date', '-time').first()


# =========================
#     APPOINTMENT MODEL
# =========================
class Appointment(models.Model):

    SERVICES = [
        ('checkup', 'General Checkup'),
        ('vaccination', 'Vaccination'),
        ('dental', 'Dental Cleaning'),
        ('grooming', 'Grooming'),
        ('surgery', 'Surgery Consultation'),
        ('emergency', 'Emergency Visit'),
    ]

    # Usuario dueño de la cita
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')

    # 🔥 Relación REAL con la mascota
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')

    # Datos de la cita
    service = models.CharField(max_length=20, choices=SERVICES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.pet.name} - {self.date} at {self.time}"
    
class Service(models.Model):
    """Servicios que ofrece la veterinaria"""
    name = models.CharField(max_length=100, verbose_name="Nombre del servicio")
    description = models.TextField(verbose_name="Descripción")
    duration = models.IntegerField(verbose_name="Duración (minutos)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio")
    icon = models.CharField(max_length=10, default="💉", verbose_name="Icono emoji")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Veterinarian(models.Model):
    """Veterinarios disponibles"""
    SPECIALTIES = [
        ('general', 'Medicina General'),
        ('surgery', 'Cirugía'),
        ('dental', 'Odontología'),
        ('dermatology', 'Dermatología'),
        ('cardiology', 'Cardiología'),
        ('emergency', 'Emergencias'),
    ]
    
    # Información personal
    name = models.CharField(max_length=200, verbose_name="Nombre completo")
    specialty = models.CharField(max_length=20, choices=SPECIALTIES, verbose_name="Especialidad")
    license_number = models.CharField(max_length=50, verbose_name="Número de cédula")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    
    # Experiencia
    years_experience = models.IntegerField(verbose_name="Años de experiencia")
    bio = models.TextField(verbose_name="Biografía", blank=True)
    
    # Disponibilidad
    available_days = models.JSONField(
        default=list,
        verbose_name="Días disponibles",
        help_text="Lista de días disponibles"
    )
    start_time = models.TimeField(verbose_name="Hora de inicio", default="09:00")
    end_time = models.TimeField(verbose_name="Hora de fin", default="17:00")
    
    # Foto
    photo = models.ImageField(upload_to='vets/', blank=True, null=True, verbose_name="Foto")
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"
        ordering = ['name']
    
    def __str__(self):
        return f"Dr(a). {self.name} - {self.get_specialty_display()}"
    
    def get_emoji(self):
        """Retorna emoji según especialidad"""
        emojis = {
            'general': '🩺',
            'surgery': '🏥',
            'dental': '🦷',
            'dermatology': '💊',
            'cardiology': '❤️',
            'emergency': '🚑',
        }
        return emojis.get(self.specialty, '👨‍⚕️')


class ClinicSchedule(models.Model):
    """Horarios de la clínica"""
    DAYS_OF_WEEK = [
        ('monday', 'Lunes'),
        ('tuesday', 'Martes'),
        ('wednesday', 'Miércoles'),
        ('thursday', 'Jueves'),
        ('friday', 'Viernes'),
        ('saturday', 'Sábado'),
        ('sunday', 'Domingo'),
    ]
    
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True, verbose_name="Día")
    is_open = models.BooleanField(default=True, verbose_name="Abierto")
    opening_time = models.TimeField(verbose_name="Hora de apertura", default="09:00")
    closing_time = models.TimeField(verbose_name="Hora de cierre", default="17:00")
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")
    
    class Meta:
        verbose_name = "Horario de Clínica"
        verbose_name_plural = "Horarios de Clínica"
        ordering = ['day_of_week']
    
    def __str__(self):
        if self.is_open:
            return f"{self.get_day_of_week_display()}: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"
        return f"{self.get_day_of_week_display()}: Cerrado"
    
class Document(models.Model):
    """Modelo para documentos PDF subidos por el administrador"""
    CATEGORY_CHOICES = [
        ('general', 'Información General'),
        ('care', 'Cuidado de Mascotas'),
        ('health', 'Salud y Vacunación'),
        ('nutrition', 'Nutrición'),
        ('training', 'Entrenamiento'),
        ('other', 'Otros'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción", blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general', verbose_name="Categoría")
    file = models.FileField(upload_to='documents/', verbose_name="Archivo PDF")
    icon = models.CharField(max_length=10, default='📄', verbose_name="Icono")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Subido por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
    
    def __str__(self):
        return self.title
    
    def get_file_size(self):
        """Retorna el tamaño del archivo en formato legible"""
        try:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        except:
            return "Desconocido"
        
# models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username