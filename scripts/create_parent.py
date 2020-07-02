import requests

data = {'username': 'AAA',
        'password': 'password',
        'phone': '385-310-2683',
        'email': 'marybeth.wilde@gmail.com'}

r = requests.post("http://localhost:8100/parent/create/", data=data)
print(r)

