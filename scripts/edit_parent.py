import requests
from account.models import ParentAccount

account_id = ParentAccount.objects.all()[0].account_id

data = {'account_id': str(account_id),
        'phone_number': '555-555-8885' }

r = requests.post("http://localhost:8100/parent/edit/", json=data)
print(r)

