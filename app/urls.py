from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('mantenedor-fechas/', mantenedor_fecha, name='mantenedor-fechas'),
    path('mantenedor-personas/', mantenedor_persona, name='mantenedor-personas'),
    path('add-fecha/', add_fecha, name='add-fecha'),
    path('update-fecha/<pk>/', update_fecha, name='update-fecha'),
    path('delete-fecha/<pk>/', delete_fecha, name='delete-fecha'),
]
