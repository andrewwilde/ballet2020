import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import DanceClass, FreeClass, FreeClassRegistration
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.cache import cache_control

from account.models import Account
from facebook.api import create_facebook_data_free_event

logger = logging.getLogger('ballet')

@cache_control(max_age=300)
def index(request):
    #create_facebook_data_free_event(request, {"name": "visited home"})
    logger.info(str(request.COOKIES))
    return render(request, 'index.html')

def classes(request):
    context = { 'classes': [] }
    dance_classes = DanceClass.objects.all().order_by("dance_type", "level")
    for dance_class in dance_classes:
        context['classes'].append(dance_class)

    return render(request, 'classes.html', context=context)

def registration(request):
    #create_facebook_data_free_event(request, {"name": "clicked on register"})
    return render(request, 'registration.html')

def send_free_class_email(registration):
    from front.templates.email import free_html_template
    from front.templates.email import free_text_template
    append_file = []
    try:
            html_body = free_html_template().format(day=str(registration.free_class))
            text_body = free_text_template().format(day=str(registration.free_class))

            email = EmailMultiAlternatives(
                    "Petit Ballet Academy: Free Class Confirmation",
                    html_body,
                    settings.EMAIL_HOST_USER,
                    [registration.parent_email]
            )
            email.attach_alternative(text_body, 'text/plain')
            email.attach_file('/home/andrew/projects/ballet2020/static/docs/liability.pdf')
            email.send(fail_silently=False)
    except Exception as err:
        print("Error sending free class confirmation. e=%s" % str(err))


@api_view(["POST"])
def freeclass(request):
    email = request.data.get('parent-email')
    num_students = request.data.get("students-num")
    id = request.data.get('freeclassoption')

    try:
        free_class = FreeClass.objects.get(id=id)
    except:
        print("Free class does not exist.")
        return render(request, 'index.html')

    if email and num_students and id:
        registration = FreeClassRegistration.objects.create(free_class=free_class, num_students=num_students, parent_email=email)
        send_free_class_email(registration)
        return render(request, "freeclass.html")

    return render(request, 'index.html')

@api_view(["GET"])
def get_free_classes(request):
    free_classes = []
    for cls in FreeClass.objects.filter(status='Active'):
        registrations = FreeClassRegistration.objects.filter(free_class=cls)
        total_registered = 0
        for reg in registrations:
            total_registered = total_registered + reg.num_students

        if total_registered < cls.capacity:
            free_classes.append({'title': cls.title, 'id': cls.id})

    return JsonResponse(free_classes, safe=False)


@api_view(["POST"])
def filter_classes(request):
    dance_type = request.data.get('type')
    age = request.data.get('age')

    days = [ k for k in request.data.keys() if k not in ['type', 'age']]

    q_list = []
    if dance_type != 'all':
        q_list.append(Q(dance_type=dance_type))

    if age != 'all':
        q_list.append(Q(level=age))

    if days:
        q_list.append(Q(day__in=days))

    dance_classes = DanceClass.objects.filter(*q_list)

    return JsonResponse(list(dance_classes.values()), safe=False)


@api_view(["GET"])
def get_classes_by_category(request):
    classes_by_category = {}
    dance_classes = DanceClass.objects.exclude(status__in=["Inactive", "Closed for Season"]).order_by("min_age", "start_day", "dance_type", "level", "day", "start_time")
    for cls in dance_classes:
        dict_cls = model_to_dict(cls)
        dict_cls['day'] = cls.get_day_display()

        if cls.start_day:
            dict_cls['start_day'] = cls.start_day.strftime('%b %-d')
        if cls.end_day:
            dict_cls['end_day'] = cls.end_day.strftime('%b %-d')

        dict_cls['start_time'] = cls.start_time.strftime('%I:%M %p')
        dict_cls['stop_time'] = cls.stop_time.strftime('%I:%M %p')
        dance_category = dict_cls['dance_category'] = "%s %s" % (cls.level, cls.dance_type)
        if dance_category not in classes_by_category:
            classes_by_category[dance_category] = [dict_cls]
        else:
            classes_by_category[dance_category].append(dict_cls)

    sorted_list = sorted(classes_by_category.values(), key = lambda v: (v[0]['min_age'], v[0]['level']))

    return JsonResponse(sorted_list, safe=False)


def profile(request):
    if request.user.is_authenticated:
        user = Account.objects.get(pk=request.user.id)
        if user.account_type == 'Teacher':
            return render(request, 'teacher.html')
        elif user.account_type == 'Parent':
            return render(request, 'parent.html')
        elif user.account_type == 'Admin':
            return render(request, 'admin.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
