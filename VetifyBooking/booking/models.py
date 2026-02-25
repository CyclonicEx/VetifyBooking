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