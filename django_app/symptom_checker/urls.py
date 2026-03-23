from django.urls import path
from . import views

urlpatterns = [
    path('', views.symptom_checker_view, name='symptom_checker'),
    path('predict/', views.predict_view, name='symptom_predict'),
]
