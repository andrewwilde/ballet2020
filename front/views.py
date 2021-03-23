import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import DanceClass
from django.shortcuts import render
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from account.models import Account

logger = logging.getLogger('ballet')

def index(request):
    logger.info("We have a visitor!")
    return render(request, 'index.html')

def classes(request):
    context = { 'classes': [] }
    dance_classes = DanceClass.objects.all().order_by("dance_type", "level")
    for dance_class in dance_classes:
        context['classes'].append(dance_class)

    return render(request, 'classes.html', context=context)

def registration(request):
    logger.info("Someone is using the registration page!")
    return render(request, 'registration.html')

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
    dance_classes = DanceClass.objects.exclude(status="Inactive").order_by("dance_type", "level", "day", "start_time")
    for cls in dance_classes:
        dict_cls = model_to_dict(cls)
        dict_cls['day'] = cls.get_day_display()

        if cls.start_day:
            dict_cls['start_day'] = cls.start_day.strftime('%b %-d')
        if cls.end_day:
            dict_cls['end_day'] = cls.end_day.strftime('%b %-d')

        dict_cls['start_time'] = cls.start_time.strftime('%I:%M %p')
        dict_cls['stop_time'] = cls.stop_time.strftime('%I:%M %p')
        dance_category = "%s %s" % (cls.level, cls.dance_type)
        if dance_category not in classes_by_category:
            classes_by_category[dance_category] = [dict_cls]
        else:
            classes_by_category[dance_category].append(dict_cls)

    return JsonResponse(classes_by_category, safe=False)


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
