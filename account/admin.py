from . import models
from django.contrib.admin.options import BaseModelAdmin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import * 

# Register your models here.
@admin.register(ParentAccount)
class ParentAdmin(admin.ModelAdmin):

    list_display = ('username',
                    'phone_number',
                    'email',
                    'account_type',
                    'date_joined',)

@admin.register(TeacherAccount)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'phone_number',
                    'email',
                    'account_type',
                    'date_joined',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'student_type', 'parent', 'medical',)
    list_display_links = ('parent',)

@admin.register(DanceClass)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('level',
                    'dance_type',
                    'day',
                    'start_time',
                    'stop_time',
                    'teacher',
                    'status',) 

