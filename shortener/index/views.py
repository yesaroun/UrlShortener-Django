from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required

from shortener.models import Users
from shortener.forms import RegisterForm, LoginForm


def index(request):
    return render(request, "base.html", {"welcome_msg": "Hello!"})


@csrf_exempt
def get_user(request, user_id):
    if request.method == "GET":
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method!"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터입니다."
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                User = get_user_model()
                user = User.objects.get(email=email)
                user_profile = Users.objects.get(user=user)
            except Users.DoesNotExist:
                pass
            else:
                if user_profile.user.check_password(raw_password):
                    msg = None
                    login(request, user_profile.user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
    else:
        msg = None
        form = LoginForm()
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})
