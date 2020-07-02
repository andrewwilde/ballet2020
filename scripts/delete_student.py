import requests
from account.models import ParentAccount, Student

ParentAccount.objects.all().delete()

data = {'username': 'AAA',
        'password': 'password',
        'phone': '385-310-2683',
        'email': 'marybeth.wilde@gmail.com'}

r = requests.post("http://localhost:8100/parent/create/", json=data)
print(r)

parent = ParentAccount.objects.get(email="marybeth.wilde@gmail.com")

student_data = {"name": "Penny Wilde",
                "medical": "None",
                "birth_date": "2012-01-31",
                "student_type": "Standard"}

data = {"account_id": str(parent.account_id),
        "student": student_data}

r = requests.post("http://localhost:8100/student/create/", json=data)
print(r)

student = Student.objects.filter(parent=parent)[0]

data = {"account_id": str(parent.account_id),
        "student_id": str(student.id)}

r = requests.delete("http://localhost:8100/student/delete/", json=data)
print(r)
