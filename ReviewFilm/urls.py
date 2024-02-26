"""
URL configuration for ReviewFilm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from Film import views
from Film.views import FilmViewSet
from ReviewFilm import settings

router = routers.SimpleRouter()
router.register(r'film', FilmViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Film.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('api/v1/', include(router.urls)),
    path('api/v1/random/', views.RandomFilm.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)