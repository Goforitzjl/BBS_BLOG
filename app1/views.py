from django.shortcuts import render, HttpResponse, redirect
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
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
    def get_random_color():
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
    img = Image.new("RGB", (262, 34), color=get_random_color())
    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype("static/font/bold.otf", size=35)
    valid_code_str = ""
    for i in range(5):
        random_number = str(random.randint(0, 9))
        random_lower_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_selected = random.choice([random_number, random_lower_alpha, random_upper_alpha])
        draw.text((i*30+20, -7), random_selected, get_random_color(), font=font_style)
        valid_code_str += random_selected
    request.session['valid_code_str'] = valid_code_str
    width = 262
    height = 34
    for i in range(10):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(200):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return HttpResponse(data)


def index(request):
    return render(request, "index.html")
