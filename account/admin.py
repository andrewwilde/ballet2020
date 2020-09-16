from . import models
from django.contrib.admin.options import BaseModelAdmin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import * 

# Register your models here.
@admin.register(ParentAccount)
class ParentAdmin(admin.ModelAdmin):

    list_display = ('get_full_name',
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
    list_display = ('first_name', 'last_name', 'birth_date', 'student_type', 'get_parent', 'notes',)
    list_display_links = ('get_parent',)

    def get_parent(self, obj):
        return obj.parent.get_full_name()

@admin.register(DanceClass)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'level',
                    'dance_type',
                    'day',
                    'start_time',
                    'stop_time',
                    'teacher',
                    'status',
                    'curriculum',
                    'price_id',) 

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('dance_class',
                    'student',
                    'status',
                    'get_parent',
                    'get_price',
                    'id',)

    def get_parent(self, obj):
        return obj.student.parent.get_full_name()

    def get_price(self, obj):
        return obj.dance_class.price
