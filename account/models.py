import uuid
import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

DEFAULT_SEMESTER='Fall'

class Account(User):
    phone_number = models.CharField(max_length=20)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=50, blank=True, null=True)

class AdminAccount(Account):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    account_type = models.CharField(max_length=20, default="Admin")

class TeacherAccount(Account):
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    account_type = models.CharField(max_length=20, default="Teacher")

class ParentAccount(Account):
    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

    account_type = models.CharField(max_length=20, default="Parent")
    stripe_id = models.CharField(max_length=50, default="", null=True, blank=True)
    is_late = models.BooleanField(default=False)

class DanceClass(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Full', 'Class is Full'),
    ]

    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    DANCE_TYPES = [
        ('Ballet', 'Ballet'),
        ('Jazz', 'Jazz'),
        ('Tap', 'Tap'),
        ('Modern', 'Modern'),
        ('Irish', 'Irish'),
        ('Ballroom', 'Ballroom'),
        ('Hip Hop', 'Hip Hop'),
        ('Creative Dance', 'Creative Dance'),
    ]

    LEVELS = [
        ('Pre', 'Pre'),
        ('Kinder', 'Kinder'),
        ('Beginning 1', 'Beginning 1'),
        ('Beginning 2', 'Beginning 2'),
        ('Intermediate 1', 'Intermediate 1'),
        ('Intermediate 2', 'Intermediate 2'),
        ('Advanced 1', 'Advanced 1'),
        ('Advanced 2', 'Advanced 2'),
        ('Adult All Levels', 'Adult All Levels'),
        ('Adult Beginning', 'Adult Beginning'),
        ('Adult Advanced', 'Adult Advanced'),
    ]

    STUDIO_TYPES = [
        ('Studio 1', 'Studio 1'),
        ('Studio 2', 'Studio 2'),
    ]

    PAYMENT_FREQUENCY = [
        ('each month', 'each month'),
        ('one-time payment', 'one-time payment'),
    ]

    PRICE_ID = [
        ('price_1HRWnQIQ4hPK7zxOAOwjHQvv', 'Pre Creative Dance'),
        ('price_1HRWn3IQ4hPK7zxOb64qqBCG', 'Kinder Tap'),
        ('price_1HRWmmIQ4hPK7zxOQ8GKSplt', 'Intermediate Jazz'),
        ('price_1HmWiPIQ4hPK7zxOxdtqzmtJ', 'Kinder Jazz'),
        ('price_1HRWmYIQ4hPK7zxOEcN1irzM', 'Beginning 1 Jazz'),
        ('price_1HRWm7IQ4hPK7zxOh8w1Ksqy', 'Beginning 2 Ballet'),
        ('price_1HRWlgIQ4hPK7zxO3I0rUBCQ', 'Beginning 1 Ballet'),
        ('price_1HRWjxIQ4hPK7zxOxZKgZTg1', 'Pre Ballet'),
        ('price_1HRWHPIQ4hPK7zxOW0DfgEpX', 'Kinder Ballet'),
    ]

    docs_path = os.path.join(settings.BASE_DIR, 'front/static/docs')

    image = models.CharField(max_length=50)
    secondary_image = models.CharField(max_length=50, null=True, blank=True)
    max_students = models.IntegerField()
    start_time = models.TimeField()
    stop_time = models.TimeField()
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    studio = models.CharField(max_length=20, choices=STUDIO_TYPES)
    level = models.CharField(max_length=20, choices=LEVELS)
    dance_type = models.CharField(max_length=20, choices=DANCE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default="Inactive")
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.DO_NOTHING) 
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    price = models.IntegerField()
    curriculum = models.FilePathField(path=docs_path, null=True, blank=True)
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY, default='each month')
    price_id = models.CharField(max_length=50, choices=PRICE_ID, default="")

    def __str__(self):
        return "%s %s on %s @ %s with %s" % (self.level, self.dance_type, self.get_day_display(), str(self.start_time), self.teacher.first_name)

class Student(models.Model):
    STUDENT_TYPES = [
        ('Standard', 'Standard'),
        ('Scholarship', 'Scholarship'),
        ('Agreement', 'Agreement'),
    ]

    student_id = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    notes = models.TextField()
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES)
    parent = models.ForeignKey(ParentAccount, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class ClassAssignment(models.Model):
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE)

class TeacherAssignment(ClassAssignment):
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE)

class StudentEnrollment(ClassAssignment):
    SEMESTER_PERIOD = [
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer')
    ]
    ENROLLMENT_STATES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,
                              choices=ENROLLMENT_STATES,
                              default= 'Inactive')
    semester = models.CharField(max_length=10,
                               choices=SEMESTER_PERIOD,
                               default=DEFAULT_SEMESTER)


