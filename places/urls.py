# places.urls

from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

# place actions
app_name='places'
urlpatterns = [

    # will eventually take purl
    path('<int:id>/portal', views.PlacePortalView.as_view(), name='place-portal'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
