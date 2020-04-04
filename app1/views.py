from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth


def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code_user = request.POST.get("valid_code")
        valid_code_service = request.session.get("valid_code_str")
        if valid_code_user.upper() == valid_code_service.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                response["user"] = user.username
            else:
                response["msg"] = "user or password wrong"
        else:
            response["msg"] = "valid code wrong"
        return JsonResponse(response)
    return render(request, "login.html")


def get_valid_image(request):
    from app1.self_functions.valid_image_function import get_valid_image_function
    data = get_valid_image_function(request)
    return HttpResponse(data)


def register(request):
    from app1.self_functions.forms_functions import UserInfo
    form = UserInfo()
    return render(request, "register.html", {"form": form})


def index(request):
    return render(request, "index.html")



