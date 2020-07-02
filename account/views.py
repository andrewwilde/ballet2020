from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ParentAccount, Student

# Create your views here
@api_view(['POST'])
def create_parent(request):
    new_account = ParentAccount.objects.create_user(username=request.data["username"],
                                              password=request.data["password"],
                                              email=request.data["email"],
                                              phone_number=request.data["phone"])

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def edit_parent(request):
    account_id = request.data.get("account_id", None)
    if not account_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    account = ParentAccount.objects.filter(account_id=account_id)
    account.update(**request.data)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def create_or_update_student(request):
    account_id = request.data.get("account_id", None)
    if not account_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    account = get_object_or_404(ParentAccount, account_id=account_id)
    request.data["student"]["parent"] = account

    try:
        student = Student.objects.update_or_create(**request.data.get("student"))
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)



@api_view(['DELETE'])
@login_required
def delete_student(request):
    account_id = request.data.get("account_id", None)
    if not account_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    account = get_object_or_404(ParentAccount, account_id=account_id)
    student_id = request.data.get("student_id", None)

    Student.objects.get(parent=account, id=student_id).delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if not (username and password):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
        #TODO: Redirect to a success page.
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        #TODO: Return an 'invalid login' error message.


@api_view(['POST'])
@login_required
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def create_class(request):
    account_id = request.data.get("account_id", None)
    if not account_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    account = User.objects.get(account_id=account_id)
    if account.type != "Admin":
        return Response(status=status.HTTP_403_FORBIDDEN)


def is_admin(user):
    return user.account_type == "Admin"


@api_view(['GET'])
@login_required
@user_passes_test(is_admin)
def admin_page(request):
    #render admin page
    return Response(status=status.HTTP_200_OK)


def is_teacher(user):
    valid_account_types = ["Teacher", "Admin"]
    return user.account_type in valid_account_types


@api_view(['GET'])
@login_required
@user_passes_test(is_teacher)
def teacher_page(request):
    #render teacher page
    return Response(status=status.HTTP_200_OK)


