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
        (1, 'Monday, Wednesday, Friday'),
        (2, 'Monday - Friday'),
        (3, 'Tuesday'),
        (4, 'Tuesday, Thursday'),
        (5, 'Wednesday'),
        (6, 'Thursday'),
        (7, 'Friday'),
        (8, 'Saturday'),
        (9, 'Sunday'),
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
        ('Dance Camp', 'Dance Camp'),
        ('Dance', 'Dance'),
        ('Contemporary', 'Contemporary'),
    ]

    CLASS_TYPES = [
            ('Fall Classes', 'Fall Classes'),
            ('Summer Camp', 'Summer Camp'),
            ('Winter Classes', 'Winter Classes'),
    ]

    LEVELS = [
        ('Mom & Tots', 'Mom & Tots'),
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
        ('None', 'None'),
        ('price_1Kwg8qIQ4hPK7zxOi4TiHUwj', 'Pre Creative Dance'),
        ('price_1Kwg5wIQ4hPK7zxOgI3lmQal', 'Kinder Tap'),
        ('price_1Kwg83IQ4hPK7zxO7zguIJxj', 'Intermediate Jazz'),
        ('price_1Kwg7PIQ4hPK7zxO6aMvc50D', 'Kinder Jazz'),
        ('price_1Kwg7dIQ4hPK7zxOFKam9nGi', 'Beginning 1 Jazz'),
        ('price_1Kwg5LIQ4hPK7zxOHOL8CiP1', 'Beginning 2 Ballet'),
        ('price_1Kwg54IQ4hPK7zxOVPpGKX6r', 'Beginning 1 Ballet'),
        ('price_1KwfyPIQ4hPK7zxOXBDsG5lN', 'Pre Ballet'),
        ('price_1Kwg32IQ4hPK7zxOZf3YKCph', 'Kinder Ballet'),
        ('price_1Kwg94IQ4hPK7zxOFOEInfyP', 'Kinder Creative'),
        ('price_1Kwg6vIQ4hPK7zxOKy6JSVp1', 'Beginning 1 Tap'),
        ('price_1Kwg5fIQ4hPK7zxOjkeTDxb4', 'Intermediate 1 Ballet'),
        ('price_1Kwg8OIQ4hPK7zxOQXjBKzBC', 'Mom & Tots Creative Dance'),
        ('price_1Kwg9XIQ4hPK7zxOrLgcCiHa', 'Beginning 1 Creative Dance'),
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
    class_type = models.CharField(max_length=40, choices=CLASS_TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default="Inactive")
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.DO_NOTHING) 
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    price = models.IntegerField()
    curriculum = models.FilePathField(path=docs_path, null=True, blank=True)
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY, default='each month')
    price_id = models.CharField(max_length=50, choices=PRICE_ID, default="")
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if "Camp" in self.dance_type:
            return "%s %s: %s - %s from %s - %s on %s" % (self.level,
                                                    self.dance_type,
                                                    self.start_day.strftime('%B %-d'),
                                                    self.end_day.strftime('%B %-d'), 
                                                    self.start_time.strftime('%I:%M %p'),
                                                    self.stop_time.strftime('%I:%M %p'),
                                                    self.get_day_display())
        else:
            return "%s %s on %s @ %s with %s" % (self.level,
                                                 self.dance_type,
                                                 self.get_day_display(),
                                                 str(self.start_time),
                                                 self.teacher.first_name)

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


