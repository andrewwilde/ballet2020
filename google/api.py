import logging

from ga4mp import Ga4mp
import requests

from ballet import secret

log = logging.getLogger('ballet')

def send_google_conversion(value, transaction_id, request, enrollments, parent_id):
    client_id = request.COOKIES.get('_ga')
    ip_address = request.META.get('REMOTE_ADDR', '')
    utm_source = request.query_params.get('utm_source', '')
    utm_medium = request.query_params.get('utm_medium', '')
    utm_campaign = request.query_params.get('utm_campaign', '')
    
    items = [ {'item_id': e.id, 'item_name': str(e.dance_class) } for e in enrollments ]
    ga = Ga4mp(measurement_id = secret.MEASUREMENT_ID, api_secret = secret.GOOGLE_API_SECRET, client_id = client_id)
    event = {
            "name": "purchase",
            "params": {
                "value": value,
                "transaction_id": transaction_id,
                "currency": "USD",
                "items": items,
                "cip": ip_address,
                "uid": parent_id,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign
            }
    }
    ga.send([event])
    log.info("Google conversion event sent: {}".format(str(event)))
