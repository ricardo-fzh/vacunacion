from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from datetime import date
from tablib import Dataset
from datetime import date
import datetime 
from django.core.exceptions import ObjectDoesNotExist
from .forms import HorasForm, PersonaForm
from django.http import HttpResponse
from .resources import HoraResource, CentroResource
import pandas as pd
import os.path

# Create your views here.

# Validación Rut


# Sistema
def user_login(request):
    if request.user.is_authenticated:
        return redirect(to="mantenedor-fechas")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(to='mantenedor-fechas')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'app/login.html')

def logout_user(request):
    logout(request)
    return redirect(to="login")

# Vista usuario


def index(request):
    centros = Centro.objects.all()
    data = {
        'centros': centros,
    }
    return render(request, 'app/index.html', data)


# Hardcore function
def reserva(request, pk):
    centro = get_object_or_404(Centro, pk=pk)
    
    dias = centro.horas.distinct('dia')
    horas = centro.horas.all()

    form = PersonaForm()
    data = {
        "form": form,
        'horas': horas,
        'dias': dias,
        'centro': centro,
    }

    if request.method == 'POST':
        form = PersonaForm(data=request.POST)
        hora_pk = request.POST.get('horas')

        if hora_pk == None or hora_pk == '':
            messages.error(request, "Debes seleccionar una hora valida")
            data['form'] = form
            return render(request, 'app/reserva.html', data)

        if form.is_valid():
            rut = form.cleaned_data.get('rut')
            existe_hora = Hora.objects.filter(pk=hora_pk).exists()

            if existe_hora == True:
                existe_hora_agendada = Persona.objects.filter(rut=rut).exists()
                hora = Hora.objects.get(pk=hora_pk)

                if existe_hora_agendada == False:
                    if hora.cupos > 0:
                        today = date.today()
                        form.centros = centro
                        form.save(data)
                        hora.cupos = hora.cupos-1
                        hora.save()
                        persona = Persona.objects.get(rut=rut)
                        persona.centros = centro
                        persona.fecha_vacunacion = hora.dia
                        persona.horas = hora
                        persona.save()
                        messages.success(request, "Hora agendada correctamente")
                        return redirect(to='/')
                    else:
                        messages.error(
                            request, "No quedan cupos para la hora seleccionada")
                        data['form'] = form
                else:                
                    persona = Persona.objects.get(rut=rut)
                    
                    fecha_primer_registro = persona.fecha_primer_registro
                    if persona.vacuna_disponible <= 0:
                        messages.error(request, "Ya se encuentra vacunado")
                        data['form'] = form
                        return render(request, 'app/reserva.html', data)
                    if hora.cupos > 0:
                        if persona.vacuna_disponible == 2:
                     
                            if persona.fecha_vacunacion == None:
                                form = PersonaForm(data=request.POST, instance=persona)
                                form.centros = centro
                                form.save(data)
                                hora.cupos = hora.cupos-1
                                hora.save()
                                persona.centros = centro
                                persona.fecha_vacunacion = hora.dia
                                persona.horas = hora
                                persona.save()
                                messages.success(request, "Hora agendada correctamente")
                                return redirect(to='/')
                            else:
                                messages.error(request, f"Ya tiene una hora agendada")
                                data['form'] = form
                        if persona.vacuna_disponible == 1:
                            today = datetime.datetime.today()
                            start_date = persona.fecha_primer_registro.strftime("%Y-%m-%d")
                            date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                            end_date = date_1 + datetime.timedelta(days=28)
                            x = datetime.datetime(2021, 3, 23)
                            #today
                            if persona.fecha_seg_vacunacion == None and today >= end_date:
                                primer_registro= persona.fecha_primer_registro
                                form = PersonaForm(data=request.POST, instance=persona)
                                form.centros = centro
                                form.save(data)
                                hora.cupos = hora.cupos-1
                                hora.save()
                                persona.centros = centro
                                persona.fecha_vacunacion = start_date
                                persona.fecha_seg_vacunacion = hora.dia
                                persona.fecha_primer_registro = primer_registro
                                persona.horas_seg_v = str(hora)
                                persona.save()
                                messages.success(request, "Hora agendada correctamente")
                                return redirect(to='/')
                            else: 
                                messages.error(request, f"Debe esperar 28 días para la proxima vacuna {end_date}")
                                data['form'] = form
                    else:
                        messages.error(
                            request, "No quedan cupos para la hora seleccionada")
                        data['form'] = form
            else:
                messages.error(
                    request, "No se encontraron horas para el registro")
                data['form'] = form
        else:
            data['form'] = form

    return render(request, 'app/reserva.html', data)

# mantenedor_fechas
def mantenedor_fecha(request):
    if not request.user.is_authenticated:
        return redirect(to='login')

    try:
        centros = Centro.objects.get(nombre__icontains=request.user.profile.centro.nombre)
        horas = centros.horas.all()
        data = {'centros': centros, 'horas': horas}
        return render(request, 'app/mantenedor_fechas.html', data)
    except ObjectDoesNotExist:
        logout(request)
        messages.error(request, 'Usuario no tiene un centro asociado')
        return redirect(to='login')

def update_fecha(request, pk):
    if not request.user.is_authenticated:
        return redirect(to='login')

    centro = Centro.objects.get(nombre__icontains=request.user.profile.centro.nombre)
    hora = get_object_or_404(Hora, pk=pk)
    form = HorasForm(instance=hora)

    data = {
        "horas": hora,
        "centros": centro,
        "form": form,
    }

    if request.method == 'POST':
        form = HorasForm(data=request.POST, instance=hora)
        if form.is_valid():
            form.save(data)
            return redirect(to='mantenedor-fechas')
        else:
            data['form'] = form
    return render(request, 'app/update-fecha.html', data)

def add_fecha(request):
    if not request.user.is_authenticated:
        return redirect(to='login')

    centro = Centro.objects.get(
        nombre__icontains=request.user.profile.centro.nombre)

    if request.method == 'POST':
        data = pd.read_csv(request.FILES['myfile'])
        data_ext = request.FILES['myfile']
        extension = os.path.splitext(str(data_ext))[1]

        if extension != '.csv':
            messages.error(request, 'El archivo debe ser de extensión .CSV')
            return redirect(to="add-fecha")

        horas = [
            Hora(
                hora=row['hora'],
                dia=row['dia'],
                cupos=row['cupos'],
                created_at=date.today(),
                updated_at=date.today(),
            )
            for i, row in data.iterrows()
        ]

        try:
            hora = Hora.objects.bulk_create(horas)
            for h in hora:
                centro.horas.add(h.id)
            messages.success(request, f"Horas cargadas exitosamente")
            return redirect(to="mantenedor-fechas")
        except:
            messages.error(
                request, f"Error al cargar archivo, verifique la estructura del archivo")
            return redirect(to="add-fecha")

    return render(request, 'app/add-fecha.html')

def delete_fecha(request, pk):
    if not request.user.is_authenticated:
        return redirect(to='login')
    hora = get_object_or_404(Hora, pk=pk)
    hora.delete()
    return redirect(to='mantenedor-fechas')

def mantenedor_persona(request):
    if not request.user.is_authenticated:
        return redirect(to='login')

    try:
        centros = Centro.objects.get(nombre__icontains=request.user.profile.centro.nombre)
        personas = Persona.objects.filter(centros__nombre=centros.nombre)
     
        data = {'centros': centros, 'usuarios': personas}

        if request.method == 'POST':
            user_id = request.POST.get('id')
            if user_id != None:
                persona = Persona.objects.get(id=user_id)


                if persona.vacuna_disponible == 2:

                    x = datetime.date(2021, 3, 26)
                    #date.today()
                    if date.today() >= persona.fecha_vacunacion  :
                        persona.vacuna_disponible = persona.vacuna_disponible - 1
                        persona.fecha_primer_registro = date.today()
                        persona.save()
                        messages.success(
                            request, 'Persona registrada en el sistema')
                    else:
                        messages.error(
                            request, f'Debe esperar 28 días para la proxima vacuna')
                elif  persona.vacuna_disponible == 1:
                    start_date = persona.fecha_primer_registro.strftime("%Y-%m-%d")
                    date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    end_date = date_1 + datetime.timedelta(days=28)
                    x = datetime.datetime(2021, 3, 23)
                    # datetime.datetime.today()
                    if datetime.datetime.today() >= end_date:
                        persona.vacuna_disponible = persona.vacuna_disponible - 1
                        persona.fecha_vacunacion =   persona.fecha_vacunacion
                        persona.fecha_primer_registro = persona.fecha_primer_registro 
                        persona.fecha_seg_vacunacion = persona.fecha_seg_vacunacion
                        persona.fecha_segundo_registro = date.today()
                        persona.save()
                        messages.success(
                            request, 'Persona registrada en el sistema')
                    else: 
                        messages.error(
                            request, f'Debe esperar 28 días para la proxima vacuna {end_date}')
                else:
                    messages.error(request, 'Persona ya se encuentra vacunada')
            else:
                messages.error(
                    request, 'Persona no se encuentra registrada sistema')
        return render(request, 'app/mantenedor_persona.html', data)

    except ObjectDoesNotExist:
        logout(request)
        messages.error(request, 'Usuario no tiene un centro asociado')
        return redirect(to='login')
