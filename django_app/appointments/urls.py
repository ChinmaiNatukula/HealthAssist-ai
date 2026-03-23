from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]
