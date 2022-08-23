from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .DINO_model import dino_views

app_name = 'dino'
urlpatterns = [
    # two paths: with or without given image
    path('', views.index, name='index'),
    path('pinterest', views.pinterest, name = 'pinterest'),
    path('api', views.api, name='api'),
    path('dino_api', dino_views.dino_api, name='dino_api'),
    path('new', views.new, name = 'new')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)