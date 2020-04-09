from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from app1.models import *
from django.db.models import Count, Avg, Min, Max


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

    # 将每一个站点的category的title和category中的文章数量给分组查询出来
    category_list = Category.objects.filter(blog=user.blog).values("pk").annotate(
        c=Count("article__title")).values_list("title", "c")
    # 将每一个站点的tag的title和tag中的文章数量给分组查询出来
    tag_list = Tag.objects.filter(blog=user.blog).values("pk").annotate(
        c=Count("article__title")).values_list("title", "c")
    # 将每一个站点的文章按年月来分类,
    # 方法1
    # y_m_date = Article.objects.extra(select={
    #     "y_m_date": "date_format(create_time,'%%Y-%%m')"}).values_list("title", "y_m_date")
    # 方法2
    from django.db.models.functions import TruncMonth
    date_list = Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")
                                                           ).values("month").annotate(c=Count("nid")).values_list(
        "month", "c")
    print("date_list",date_list)
    return render(request, "home_site.html", locals())
