import logging
import math
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.models import DanceClass
#from facebook.api import (
#        create_facebook_data_free_event,
#        create_facebook_email_event
#        )

logger = logging.getLogger('ballet')

START_DATE = datetime.date(2024, 9, 1)

@api_view(['POST'])
def send_email(request):
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

    if first_name == 'woguets' and last_name == 'woguets':
        return render(request, 'failed_email.html')

    if not message or "http" in message or "www" in message:
        #create_facebook_data_free_event(request, {"name": "discarded email"})
        return render(request, 'failed_email.html')

    try:
        send_mail("Website Contact Form",
                  body,
                  email_from,
                  [settings.EMAIL_HOST_USER],
                  fail_silently=False)
        #create_facebook_email_event(request, {"name": "sent email", "first_name": first_name, "last_name": last_name, "phone": phone, 'email': email_from})
    except Exception as e:
        logger.error("Problem sending an email. e=%s" % str(e))
        return render(request, 'failed_email.html')

    return render(request, 'email.html') 

@api_view(['GET'])
def available_classes(request):
    dob = request.GET['dob']
    age = get_age_by_first_day(dob)
    available_classes = get_classes_by_age(age)

    filtered_classes = []
    for cls in available_classes:
        dict_cls = model_to_dict(cls)
        dict_cls['start_time'] = cls.start_time.strftime('%I:%M %p')
        dict_cls['stop_time'] = cls.stop_time.strftime('%I:%M %p')
        if cls.start_day:
            dict_cls['start_day'] = cls.start_day.strftime('%B %-d')
        if cls.end_day:
            dict_cls['end_day'] = cls.end_day.strftime('%B %-d')
        dict_cls['day'] = cls.get_day_display()
        dict_cls['camp'] = False 

        if 'Camp' in cls.dance_type:
            dict_cls['camp'] = True

        dict_cls['class_type'] = cls.get_class_type_display()

        filtered_classes.append(dict_cls)

    #create_facebook_data_free_event(request, {"name": "pulled available classes"})
    return JsonResponse(filtered_classes, safe=False)

def get_classes_by_age(age):
    return DanceClass.objects.filter(max_age__gte=age, min_age__lte=age, status="Active").order_by("dance_type", "start_day", "day", "start_time")

def get_age_by_first_day(dob):
    year, month, day = dob.split("-")
    dob_datetime = datetime.date(int(year), int(month), int(day))

    time_difference = START_DATE - dob_datetime
    age = math.floor(time_difference.days/365) 

    return age
