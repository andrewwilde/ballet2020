import time

import logging
logger = logging.getLogger('ballet')

from ballet.stagingsecret import PIXEL_ID, CONVERSION_API_KEY
from facebook_business.adobjects.serverside.action_source import ActionSource
from facebook_business.adobjects.serverside.content import Content
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.delivery_category import DeliveryCategory
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi

FacebookAdsApi.init(access_token=PIXEL_ID)

def create_user(request, user=None):
    if user:
        emails = [user.email]
        phones = [user.phone_number]
    else:
        emails = []
        phones = []


    return UserData(
            emails=emails,
            phones=phones,
            client_ip_address=request.META.get('REMOTE_ADDR'),
            client_user_agent=request.headers['User-Agent'],
            fbc=request.COOKIES.get('_fbc'),
            fbp=request.COOKIES.get('_fbp'),
        )

def create_content(products):
    contents = []
    for product in products:
        content = Content(
                product_id = product.id,
                quantity=1
                )
        contents.append(content)

    return contents

def create_custom_data(facebook_data):
    enrollments = facebook_data.get('enrollments')
    if enrollments:
        content = create_content(enrollments)
    else:
        content = []

    return CustomData(
        contents=content,
        currency='usd',
        value=facebook_data.get("total", 0),
    )

def create_event(event_name, user_data, custom_data, url):
    event = Event(
        event_name=event_name,
        event_time=int(time.time()),
        user_data=user_data,
        custom_data=custom_data,
        event_source_url=url,
        action_source=ActionSource.WEBSITE,
    )

    return [event]

def create_event_request(events):
    return EventRequest(
                events=events,
                pixel_id=PIXEL_ID,
            )

def send_event(event_request):
    event_response = event_request.execute()
    logger.info("Event sent to facebook. response={}".format(event_response))

def create_facebook_event(request, facebook_data):
    try:
        user_data = create_user(request, facebook_data.get('parent'))
        custom_data = create_custom_data(facebook_data)
        event = create_event(
                    facebook_data.get("name"),
                    user_data,
                    custom_data,
                    request.path_info
                )
        event_request = create_event_request(event)
        send_event(event_request)
    except Exception as e:
       logger.error("Problem sending event to facebook. e=%s", str(e))

def create_facebook_data_free_event(request, facebook_data):
    try:
        user_data = create_user(request)
        event = create_event(
                    facebook_data.get("name"),
                    user_data,
                    None,
                    request.path_info
                    )
        event_request = create_event_request(event)
        send_event(event_request)
    except Exception as e:
       logger.error("Problem sending event to facebook. e=%s", str(e))

def create_facebook_email_event(request, facebook_data):
    try:
        user_data = UserData(
                emails=[facebook_data.get('email')],
                phones=[facebook_data.get('phone')],
                client_ip_address=request.META.get('REMOTE_ADDR'),
                client_user_agent=request.headers['User-Agent'],
                fbc=request.COOKIES.get('_fbc'),
                fbp=request.COOKIES.get('_fbp'),
            )

        event = create_event(
                    facebook_data.get('name'),
                    user_data,
                    None,
                    request.path_info
                    )

        event_request = create_event_request(event)
        send_event(event_request)
    except Exception as e:
        logger.error("Problem sending event to facebook. e=%s", str(e))

