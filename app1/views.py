from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from app1.models import UserInfo

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
    from app1.self_functions.forms_functions import UserForm
    if request.method == "POST":
        response = {"user": None, "msg": None}
        formdata = UserForm(request.POST)
        if formdata.is_valid():
            response["user"] = formdata.cleaned_data.get("user")
            username = formdata.cleaned_data.get("user")
            pwd = formdata.cleaned_data.get("pwd")
            email = formdata.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            extral = {}
            if avatar_obj:
                extral = {"avatar": avatar_obj}
            UserInfo.objects.create_user(username=username, password=pwd, email=email, **extral)
        else:
            response["msg"] = formdata.errors
        return JsonResponse(response)
    form = UserForm()
    return render(request, "register.html", {"form": form})


def index(request):
    return render(request, "index.html")



