"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from . import views



urlpatterns = [
    path('admin/', admin.site.urls),

    # ex: /
    path("", views.home, name="home"),
    # ex: /weather_ajax
    path("weather_ajax", views.weather_ajax, name="weather_ajax"),
    # ex: /polls/5/results/
    # path("<int:question_id>/results/", views.results, name="results"),
]

# only when not testing, activate django debug toolbar urls
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
