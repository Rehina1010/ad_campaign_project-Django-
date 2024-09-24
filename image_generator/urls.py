from django.urls import path
from . import views

app_name = 'image_generator'

urlpatterns = [
    path('', views.generate_image, name='generate_image'),
]
