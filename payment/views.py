from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe

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

