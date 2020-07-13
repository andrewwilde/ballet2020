import logging
import math
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import DanceClass

logger = logging.getLogger('ballet')

START_DATE = datetime.date(2020, 9, 10)

@api_view(['POST'])
def send_email(request):
    logger.info(request.data)
    message = request.data.get('message')
    email_from = request.data.get('email_from')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone = request.data.get('phone')
    body = """
    Name: %s %s
    Email: %s
    Phone: %s
    Message: %s""" % (first_name,
                      last_name,
                      email_from,
                      phone,
                      message)

    logger.info("Website Contact Form submitted: %s." % body)

    send_mail("Website Contact Form",
              body,
              email_from,
              [settings.EMAIL_HOST_USER],
              fail_silently=False)

    return Response(status=200)

@api_view(['GET'])
def available_classes(request):
    dob = request.GET['dob']
    age = get_age_by_first_day(dob)
    available_classes = get_classes_by_age(age)

    return JsonResponse(list(available_classes.values()), safe=False)
def get_classes_by_age(age):
    return DanceClass.objects.filter(max_age__gte=age, min_age__lte=age, status="Active")

def get_age_by_first_day(dob):
    year, month, day = dob.split("-")
    dob_datetime = datetime.date(int(year), int(month), int(day))

    time_difference = START_DATE - dob_datetime
    age = math.floor(time_difference.days/365) 

    return age
