# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('generate_cpf/', generated_cpf),
    path('validate_cpf/', validate_cpf)
]
