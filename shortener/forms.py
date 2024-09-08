from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from shortener.models import Users, ShortenedUrls
from shortener.utils import url_count_changer


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=30, required=False, help_text="Optional.", label="이름"
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        label="이메일",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Users.objects.create(
                user=user,
                full_name=self.cleaned_data.get("full_name")
            )
        return user


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "이메일"}
        ),
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "패스워드"}
        ),
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"clas": "custom-control-input", "id": "_loginRememberMe"}
        ),
        required=False,
        disabled=False,
    )


class UrlCreateForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrls
        fields = ["nick_name", "target_url"]
        labels = {
            "nick_name": _("별칭"),
            "target_url": _("URL"),
        }
        widgets = {
            "nick_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "URL을 구분하기 위한 별칭",
                }
            ),
            "target_url": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "포워딩될 URL"}
            ),
        }

    def save(self, request, commit=True):
        instance = super(UrlCreateForm, self).save(commit=False)
        user_profile = get_object_or_404(Users, user=request.user)
        instance.creator = user_profile
        instance.target_url = instance.target_url.strip()
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        return instance

    def update_form(self, request, url_id):
        instance = super(UrlCreateForm, self).save(commit=False)
        instance.target_url = instance.target_url.strip()
        user_profile = get_object_or_404(Users, user=request.user)
        print(user_profile)
        ShortenedUrls.objects.filter(pk=url_id, creator=user_profile).update(
            target_url=instance.target_url, nick_name=instance.nick_name
        )
