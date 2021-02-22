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
    mapa = models.TextField('Mapa')
    estado = models.BooleanField('Estado', default=False)
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Centro'
        verbose_name_plural = 'Centros'

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    nombre = models.CharField('nombres', max_length=100,  validators=[RegexValidator(r'\w', 'Formato incorreccto')])
    apellido_paterno = models.CharField('apellido paterno', max_length=100, validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')] )
    apellido_materno = models.CharField('apellido materno', max_length=100,  validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')])
    rut = models.CharField('Rut',max_length=8, validators=[RegexValidator(r'^[0-9]{7}', 'Formato incorrecto')] )
    dv = models.CharField('Dv', max_length=1, validators=[RegexValidator(r'[0-9kK]{1}', 'Formato incorrecto debe ser digito o K')])
    fecha_nac = models.DateField('fecha nacimiento')
    genero = models.CharField('Género',max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField('email', max_length=250)
    celular = models.CharField('Celular',max_length=12)
    vacuna_disponible = models.IntegerField('Vacunas disponibles', default=2, validators=[MinValueValidator(0)])
    centros = models.ForeignKey(Centro, on_delete=models.CASCADE, null=True, blank=True) 
    horas = models.ForeignKey(Hora, verbose_name="Hora primera vacuna", on_delete=models.CASCADE, null=True, blank=True)
    horas_seg_v = models.TimeField('Hora segunda vacuna', default='00:00')
    fecha_vacunacion = models.DateField('Fecha primera vacunación', null=True, blank=True)
    fecha_seg_vacunacion = models.DateField('Fecha segunda vacunación', null=True, blank=True)
    fecha_primer_registro = models.DateField('Fecha primera asistencia', null=True, blank=True)
    fecha_segundo_registro = models.DateField('Fecha segunda asistencia', null=True, blank=True)
    edad_primer_registro = models.IntegerField('Edad en el primer registro', null=True, blank=True)
    edad_segundo_registro = models.IntegerField('Edad en el segundo registro', null=True, blank=True)
    direccion = models.CharField('Dirección', max_length=255)
    fecha_primera_ino = models.DateField('Fecha primera inoculación', null=True, blank=True)
    fecha_segunda_ino = models.DateField('Fecha segunda inoculación', null=True, blank=True)
    block = models.CharField('Block', max_length=255, null=True, blank=True)
    departamento = models.CharField('Departamento', max_length=255, null=True, blank=True)
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

class PersonaHabilitada(models.Model):
    rut = models.CharField('Rut',max_length=8, validators=[RegexValidator(r'^[0-9]{7}', 'Formato incorrecto')] )
    dv = models.CharField('Dv', max_length=1, validators=[RegexValidator(r'[0-9kK]{1}', 'Formato incorrecto debe ser digito o K')])
    fecha_vacunacion = models.DateField('Fecha primera vacunación', null=True, blank=True)
    created_at = models.DateTimeField('Fecha creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

class PersonaFila(models.Model):
    nombre = models.CharField('nombres', max_length=100,  validators=[RegexValidator(r'\w', 'Formato incorreccto')])
    apellido_paterno = models.CharField('apellido paterno', max_length=100, validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')] )
    apellido_materno = models.CharField('apellido materno', max_length=100,  validators=[RegexValidator(r'[a-z]', 'Formato incorreccto')])
    rut = models.CharField('Rut',max_length=8, validators=[RegexValidator(r'^[0-9]{7}', 'Formato incorrecto')] )
    dv = models.CharField('Dv', max_length=1, validators=[RegexValidator(r'[0-9kK]{1}', 'Formato incorrecto debe ser digito o K')])