"""ballet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views

from account import views as account
from front import views as front
from utils import views as utils

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', front.index),
    path('classes/', front.classes),
    path('create/parent/', account.create_parent),
    path('edit/parent/', account.edit_parent),
    path('create_update/student/', account.create_or_update_student),
    path('delete/student/', account.delete_student),
    path('profile/', front.profile),
    path('filter_classes/', front.filter_classes),
    path('class_levels/', front.get_classes_by_category),
    path('available_classes/', utils.available_classes),
    path('register/', front.registration),
    path('email/', utils.send_email),
]
