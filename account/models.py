import uuid

from django.db import models
from django.contrib.auth.models import User

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

class DanceClass(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
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

    image = models.CharField(max_length=50)
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

    def __str__(self):
        return "%s %s @ %s with %s" % (self.level, self.dance_type, str(self.start_time), self.teacher.first_name)
class Student(models.Model):
    STUDENT_TYPES = [
        ('Standard', 'Standard'),
        ('Scholarship', 'Scholarship'),
        ('Agreement', 'Agreement'),
    ]

    student_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    birth_date = models.DateField()
    medical = models.TextField()
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES)
    parent = models.ForeignKey(ParentAccount, on_delete=models.CASCADE)

class ClassAssignment(models.Model):
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE)

class TeacherAssignment(ClassAssignment):
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE)

class StudentEnrollment(ClassAssignment):
    ENROLLMENT_STATES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,
                              choices=ENROLLMENT_STATES,
                              default= 'Inactive')


