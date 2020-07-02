from django.shortcuts import render
from account.models import Account

def index(request):
    return render(request, 'index.html')

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
