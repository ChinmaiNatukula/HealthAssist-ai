from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('symptom-checker/', include('symptom_checker.urls')),
    path('skin-predictor/', include('skin_predictor.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('appointments/', include('appointments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
