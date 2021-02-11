from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here
# .


class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno' , 'centros','horas','fecha_vacunacion' , 'created_at', 'updated_at') 
 
    def hora_cupo(self, obj):
        return obj.horas.cupos
    
    hora_cupo.allow_tags = True
    hora_cupo.short_description = 'Cupos'

# class HoraAdmin(admin.ModelAdmin):
#     list_display = ('hora', 'cupos')

@admin.register(Hora)
class HoraAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Persona, PersonaAdmin)
# admin.site.register(Hora, HoraAdmin)
admin.site.register(Centro) 
admin.site.register(Profile)

