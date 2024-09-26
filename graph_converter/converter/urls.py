from django.urls import path
from . import views

urlpatterns = [
    path('', views.matrix_converter_view, name='matrix_converter'),
]
