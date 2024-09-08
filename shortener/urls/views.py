from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from shortener.models import ShortenedUrls, Users
from shortener.forms import UrlCreateForm


def url_list(request):
    get_list = ShortenedUrls.objects.order_by("-created_at").all()
    return render(request, "url_list.html", {"list": get_list})


@login_required
def url_create(request):
    msg = None
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('nick_name')} 생성 완료!"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("url_list")
        else:
            form = UrlCreateForm()
    else:
        form = UrlCreateForm()
    return render(request, "url_create.html", {"form": form})


@login_required
def url_change(request, action, url_id):
    user_profile = get_object_or_404(Users, user=request.user)
    if request.method == "POST":
        url_data = ShortenedUrls.objects.filter(id=url_id)
        if url_data.exists():
            if url_data.first().creator_id != user_profile.id:
                msg = "자신이 쇼유하지 않은 URL 입니다."
                messages.add_message(request, messages.ERROR, msg)
            else:
                if action == "delete":
                    msg = f"{url_data.first().nick_name} 삭제 완료!"
                    url_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{url_data.first().nick_name} 수정 완료!"
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)

                    messages.add_message(request, messages.INFO, msg)
        else:
            msg = "해당 URL 정보를 찾을 수 없습니다."
            messages.add_message(request, messages.ERROR, msg)
    elif request.method == "GET" and action == "update":
        url_instance = get_object_or_404(ShortenedUrls, pk=url_id, creator=user_profile)
        form = UrlCreateForm(instance=url_instance)
        return render(request, "url_create.html", {"form": form, "is_update": True})

    return redirect("url_list")
