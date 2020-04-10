from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from app1.models import *
from django.db.models import F
from django.http import JsonResponse
import json


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
    article_list = Article.objects.all()
    return render(request, "index.html", locals())


def logout(request):
    auth.logout(request)
    return redirect("/index/")


def home_site(request, username, **kwargs):
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("Not Found")

    article_list = Article.objects.filter(user=user).all()
    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "category":
            article_list = article_list.filter(category__title=param)
        elif condition == "tag":
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split("-")
            article_list = article_list.filter(create_time__year=year,
                                               create_time__month=month)

    context = {"user": user, "article_list": article_list}
    return render(request, "home_site.html", context)


def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    article = Article.objects.filter(user=user).filter(pk=article_id).first()
    context = {"user": user, "article": article}
    return render(request, "article_detail.html", context)


def digg(request):
    user_id = request.user.pk
    article_id = request.POST.get("article_id")
    is_comment_user = ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id)
    is_up = json.loads(request.POST.get("is_up"))
    response = {"state": None, "handled": None}
    if not is_comment_user:
        response["state"] = False
        ArticleUpDown.objects.create(article_id=article_id, is_up=is_up, user_id=user_id)
        if is_up:
            Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
            response["handled"] = True

        else:
            Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
            response["handled"] = False

    else:
        response["state"] = True
        handle = is_comment_user.values("is_up").first()
        # print("handle",handle["is_up"])
        if handle["is_up"]:
            response["handled"] = True
        else:
            response["handled"] = False
    return JsonResponse(response)
