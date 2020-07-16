from __future__ import unicode_literals

import logging
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe

from account.models import (DanceClass,
                            ParentAccount,
                            Student,
                            StudentEnrollment)

logger = logging.getLogger('ballet')
stripe.api_key = settings.STRIPE_KEY

def stripe_charge(parent, stripe_token, total, description):
    #name = "%s %s" % (parent.first_name, parent.last_name)
    #if parent.stripe_id == "":
    #    customer = stripe.Customer.create(
    #        email=parent.email,
    #        name=name,
    #        phone=parent.phone_number)

    #    parent.stripe_id = customer.id
    #    parent.save()
    #    logger.info("New stripe customer created. %s=%s" % (parent.email, parent.stripe_id))

    #else:
    #    customer = stripe.Customer.retrieve(parent.stripe_id)


    logger.info("Attempting to charge credit card. Email=%s, Total=%i" % (parent.email, total))
    stripe.Charge.create(
        amount=total*100,
        currency="USD",
        description=parent.email,
        card=stripe_token,
        receipt_email=parent.email 
    )
    logger.info("Credit card successful.")

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
                                                "start_time": my_class.start_time.strftime('%I:%M %p'),
                                                "stop_time": my_class.stop_time.strftime('%I:%M %p'),
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

@api_view(['POST'])
def confirm_registration(request):
    context = {'message': ''}
    data = request.POST
    required_fields = ['acceptTerms',
                       'p_last',
                       'p_phone',
                       'p_first',
                       'p_email',
                       'student_count',
                       'stripeToken',
                       'total']

    #Validating required fields
    for field in required_fields:
        if field not in data:
            logger.error("There is a missing required field: %s" % field)
            context['message'] = 'Form is missing field.'
            return render(request, 'failed_registration.html', context)

        if not data.get(field):
            logger.error("A required field has an empty value: %s" % field)
            context['message'] = 'Required field was missing a value.'
            return render(request, 'failed_registration.html')

    stripe_token = data.get('stripeToken')

    #Creating Parent
    parent_first_name = data.get('p_first')
    parent_last_name = data.get('p_last')
    parent_email = data.get('p_email')
    parent_phone = data.get('p_phone')

    try:
        parent = ParentAccount.objects.get(username=parent_email)
        logger.info("This parent has already registered. parent_email=%s" % parent_email)
    except ObjectDoesNotExist as e:
        try: 
            parent = ParentAccount.objects.create(first_name=parent_first_name,
                                         last_name=parent_last_name,
                                         phone_number=parent_phone,
                                         email=parent_email,
                                         username=parent_email)
            logger.info("Parent created: %s %s" % (parent.first_name, parent.last_name))
        except Exception as e:
            context['message'] = 'We were unable to create a parent account. Please contact us, since this should never happen!'
            logger.error("Error creating the parent account: %s" % str(e))
            return render(request, 'failed_registration.html', context)
    except Exception as e:
        context['message'] - 'We had an unexpected error, which should never happen. Please contact us!'
        logger.error("Unknown error. e=%s" % str(e))
        return render(request, 'failed_registration.html', context)

    #Create Students
    total = settings.REGISTRATION_FEE
    student_count = int(data.get('student_count'))
    try:
        for student_num in range(1, student_count + 1):
            student_first_id = "first_name_%i" % student_num
            student_last_id = "last_name_%i" % student_num
            student_dob_id = "dob_%i" % student_num
            student_notes_id = "notes_%i" % student_num
            student_class_id = "student_class_%i" % student_num
 
            student_first = data.get(student_first_id)
            student_last = data.get(student_last_id)
            student_dob = data.get(student_dob_id)
            student_notes = data.get(student_notes_id)
            student_classes = data.getlist(student_class_id)
 
            student = Student.objects.create(first_name=student_first,
                                             last_name=student_last,
                                             birth_date=student_dob,
                                             notes=student_notes,
                                             parent=parent)
            logger.info("Created a student: %s %s (%i)" % (student.first_name, student.last_name, student.id))
            #Create Enrollments
            for id in student_classes:
                dance_class = DanceClass.objects.get(id=int(id))
                enrollment = StudentEnrollment.objects.create(dance_class=dance_class,
                                                              student=student,
                                                              status='Active')
                logger.info("%s %s (%i) is now enrolled in %s %s (%i)" % (student.first_name,
                                                                          student.last_name,
                                                                          student.id,
                                                                          dance_class.level,
                                                                          dance_class.dance_type,
                                                                          dance_class.id))
                total = total + dance_class.price

    except Exception as e:
        context['message'] = "We were unable to enroll your student to the class. This should never happen, please contact us!"
        logger.error("There was an unknown exception during the student/enrollment creation process. e=%s" % str(e))
        return render(request, 'failed_registration.html', context)

    if total != int(data.get('total')):
        context['message'] = "Their were some inconsistencies with the form. This should never happen, please contact us!"
        logger.error("The POSTed price does not match what we'd expect. POST price=%s, Calculated=%i" % (data.get('total'), total))
        return render(request, 'failed_registration.html', context)

    try:
        name = "%s %s" % (parent.first_name, parent.last_name)
        stripe_charge(parent, stripe_token, total, "registration costs") 
    except stripe.error.StripeError as e:
        context['message'] = "Credit card transaction failed: %s" % e.error.message 
        logger.error("Credit card transaction failed(100): e=%s" % str(e))
        return render(request, 'failed_registration.html', context)
    except Exception as e:
        context['message'] = "We have a problem handling your credit card transaction. Please call us!"
        logger.error("Credit card transaction failed(101): e=%s" % str(e))
        return render(request, 'failed_registration.html', context)
    else:
        return render(request, 'confirmed.html')
