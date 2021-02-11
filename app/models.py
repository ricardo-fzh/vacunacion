from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.

class Hora(models.Model):
    hora = models.TimeField('Horas', default='00:00')
    dia = models.DateField('Día', default=datetime.date.today)
    cupos = models.IntegerField('Cupos', validators=[MinValueValidator(0)] )
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Hora'
        verbose_name_plural = 'Horas'

    def __str__(self):
        return str(self.hora)

class Centro(models.Model):
    nombre = models.CharField('Centro', max_length=180)
    horas = models.ManyToManyField(Hora, blank=True)
    direccion = models.CharField('Dirección', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Centro'
        verbose_name_plural = 'Centros'

    def __str__(self):
        return self.nombre

class Location(models.Model):
    latitude = models.FloatField(null=True, default=None, verbose_name="location latitude")
    longitude = models.FloatField(null=True, default=None, verbose_name="location longitude")
    street = models.CharField(max_length=100, verbose_name="street")
    zip_code = models.CharField(max_length=100, verbose_name="zip code")
    city = models.CharField(max_length=100, verbose_name="city")
    country = models.CharField(max_length=100, verbose_name="country")

class Persona(models.Model):
    nombre = models.CharField('nombres', max_length=100,  validators=[RegexValidator(r'\w', 'Formato incorreccto')])
    apellido_paterno = models.CharField('apellido paterno', max_length=100, validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')] )
    apellido_materno = models.CharField('apellido materno', max_length=100,  validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')])
    rut = models.CharField('Rut',max_length=8, validators=[RegexValidator(r'^[0-9]{7}', 'Formato incorrecto')] )
    dv = models.CharField('Dv', max_length=1, validators=[RegexValidator(r'[0-9kK]{1}', 'Formato incorrecto debe ser digito o K')])
    fecha_nac = models.DateField('fecha nacimiento')
    email = models.EmailField('email', max_length=250)
    celular = models.CharField('Celular',max_length=15, validators=[RegexValidator(r'^([+]56)?(\s?)(0?9)(\s?)[987654]\d{7}$', 'Formato debe ser: +569xxxxxxxx')])
    vacuna_disponible = models.IntegerField('Vacunas disponibles', default=2, validators=[MinValueValidator(0)])
    centros = models.ForeignKey(Centro, on_delete=models.CASCADE, null=True, blank=True) 
    horas = models.ForeignKey(Hora, verbose_name="Hora primera vacuna", on_delete=models.CASCADE, null=True, blank=True)
    horas_seg_v = models.TimeField('Hora segunda vacuna', default='00:00')
    fecha_vacunacion = models.DateField('Fecha primera vacunación', null=True, blank=True)
    fecha_seg_vacunacion = models.DateField('Fecha segunda vacunación', null=True, blank=True)
    fecha_primer_registro = models.DateField('Fecha primer registro', null=True, blank=True)
    fecha_segundo_registro = models.DateField('Fecha segundo registro', null=True, blank=True)
    locations = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return str(self.user)