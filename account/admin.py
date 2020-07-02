from . import models
from django.contrib.admin.options import BaseModelAdmin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import ParentAccount, Student

# Register your models here.
@admin.register(models.ParentAccount)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'phone_number',
                    'email',
                    'account_type',
                    'date_joined',)

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'student_type', 'parent', 'medical',)
    list_display_links = ('parent',)
