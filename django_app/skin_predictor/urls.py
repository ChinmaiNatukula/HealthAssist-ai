from django.urls import path
from . import views

urlpatterns = [
    path('', views.skin_predictor_view, name='skin_predictor'),
    path('predict/', views.predict_view, name='skin_predict'),
]
