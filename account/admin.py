from . import models
from django.contrib.admin.options import BaseModelAdmin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from .models import * 

# Register your models here.
@admin.register(ParentAccount)
class ParentAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'first_name',
                    'get_full_name',
                    'phone_number',
                    'email',
                    'account_type',
                    'date_joined',)
    search_fields = ('first_name', 'email')


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
    search_fields = ('first_name', 'last_name',)

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
                    'price_id',
                    'class_type',) 
    search_fields = ('level', 'dance_type', 'day', 'teacher__first_name', 'status', 'class_type',)

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):

    def class_name(self, obj):
        return str(obj.dance_class)

    def student_name(self, obj):
        return str(obj.student)

    def parent_name(self, obj):
        return obj.student.parent.get_full_name()

    def get_price(self, obj):
        return obj.dance_class.price

    list_display = ('id',
                    'class_name',
                    'student_name',
                    'status',
                    'parent_name',
                    'get_price',)

    search_fields = ('student__first_name','student__last_name','student__parent__first_name', 'student__parent__last_name',)
    #list_filter = ['class_name']
    ordering = ('dance_class__status','dance_class__id')

@admin.register(FreeClass)
class FreeClassAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'capacity',
                    'status',)

@admin.register(FreeClassRegistration)
class FreeClassRegistrationAdmin(admin.ModelAdmin):
    list_display = ('parent_email',
                    'num_students',
                    'free_class',)

