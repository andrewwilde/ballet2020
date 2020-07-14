from __future__ import unicode_literals

import logging
import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe

from account.models import DanceClass

logger = logging.getLogger('ballet')

@api_view(['POST'])
def register_charge(request, *args, **kwargs):
    stripe_token = request.POST.get('stripeToken', None)
    if not stripe_token:
        Response("Error 101.", status_code=400)

    customer = stripe.Charge.create(
                   amount=1000,
                   currency="USD",
                   description="andrew.wilde@gmail.com",
                   card=stripe_token
               )

    return Response("Success")

@api_view(['GET'])
def register_payments(request):
    payment_schedule = { "fees": [], "classes": [] } 
    payment_schedule["fees"].append( {
        "title": "Registration Fee",
        "description": "One time non-refundable fee. Reserves spot in class.",
        "price": 20
    })

    payload = request.GET['payload']
    payload = json.loads(payload)
    for name, class_list in payload.items():
        for cls_id in class_list:
            my_class = DanceClass.objects.get(id=cls_id)
            payment_schedule["classes"].append({"level": my_class.level,
                                                "name": name,
                                                "type": my_class.dance_type,
                                                "day": my_class.get_day_display(),
                                                "start_time": my_class.start_time,
                                                "stop_time": my_class.stop_time,
                                                "price": my_class.price,
                                                "status": my_class.status,
                                                "id": my_class.id})

    total = 0
    for item in payment_schedule["fees"]:
        total = total + item["price"]

    for item in payment_schedule["classes"]:
        total = total + item["price"]

    payment_schedule["total"] = {"title": "Total", "description": "", "price": total}    

    return JsonResponse(payment_schedule, safe=False)
