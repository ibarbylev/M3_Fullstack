# Регистрация и аутентификация

На этом этапе создаём всё, что нужно для Регистрации и аутентификации,  
включая подтверждения email по почте и сервис сброса и обновления пароля.

Хорошо, давайте сделаем **полную, рабочую реализацию** регистрации, подтверждения e-mail, логина, логаута, восстановления пароля — **используя только CBV**, встроенные формы там, где уместно, и нашу модель `UserToken` для email-верификации и восстановления.

## 1. `forms.py`

# user/forms.py

```python
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from user.models import UserToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Пожалуйста, введите правильное имя пользователя",
        "inactive": "Этот аккаунт отключён.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-классы и placeholder только в виджеты
        self.fields['username'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Логин'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Пароль'
        })


class RegistrationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "Введённые пароли не совпадают.",
    }
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "Input",
            "placeholder": "E-mail"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "Input",
            "placeholder": "Никнейм"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "Input",
            "placeholder": "Пароль"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "Input",
            "placeholder": "Повторите пароль"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким username уже существует.")
        return username



class MyPasswordResetForm(PasswordResetForm):
    error_messages = {
        "email": "Пользователь с таким email не найден.",
        "inactive": "Этот аккаунт отключён.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Введите ваш email'
        })

    def save(self, **kwargs):
        email = self.cleaned_data.get("email")
        # Получаем пользователей
        users = list(self.get_users(email))
        request = kwargs.get("request")
        use_https = kwargs.get("use_https", False)
        protocol = "https" if use_https else "http"
        domain = request.get_host() if request else "example.com"

        for user in users:
            token_obj = UserToken.generate(user, token_type="password_reset", expires_in_minutes=60)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{protocol}://{domain}{reverse('auth_password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token_obj.token})}"
            try:
                send_mail(
                    subject="Сброс пароля",
                    message=f"Ссылка для сброса пароля: {reset_url}",
                    from_email=kwargs.get("from_email"),  # None → DEFAULT_FROM_EMAIL
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"[ERROR] Failed to send email to {user.email}: {e}")


class MySetPasswordForm(SetPasswordForm):
    """
    Просто кастомная форма с CSS-классами
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Повторите пароль'
        })

```

---

## 2. `user/utils.py`

Функции для отправки email и генерации токенов:

```python
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import UserToken

def send_email_verification(user):
    token = UserToken.generate(user, token_type="email_verify", expires_in_minutes=60)
    verify_url = settings.SITE_URL + reverse("auth_email_verify") + f"?token={token.token}"

    send_mail(
        subject="Подтверждение email",
        message=f"Перейдите по ссылке для подтверждения: {verify_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

```

> В `settings.py` должны быть:

```
SITE_URL = "http://127.0.0.1:8000"
DEFAULT_FROM_EMAIL = "noreply@example.com"  # Ваша почта отправителя (почта сервера)
```

---

## 3. `user/views/views_auth.py`


```python
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from user.models import UserToken
from user import forms
from user.utils import send_email_verification


class LoginView(auth_views.LoginView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("home")


class RegistrationView(generic.FormView):
    template_name = "auth/register.html"
    form_class = forms.RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        send_email_verification(user)
        messages.success(self.request, "Регистрация успешна! Проверьте email для подтверждения.")

        # Сохраняем емейл в сессии, чтобы отправить запрос на повторную отправку подтверждающего емейл
        self.request.session['pending_verification_email'] = user.email

        return super().form_valid(form)


class EmailVerifyView(generic.TemplateView):
    template_name = "auth/email_verify.html"

    def get(self, request, *args, **kwargs):
        token_value = request.GET.get("token")
        if not token_value:
            messages.error(request, "Токен подтверждения не указан.")
            return redirect("home")

        try:
            token = UserToken.objects.get(token=token_value, token_type="email_verify")
        except UserToken.DoesNotExist:
            messages.error(request, "Неверный токен подтверждения.")
            return redirect("home")

        if not token.is_valid():
            messages.error(request, "Токен истёк или был отозван.")
            return redirect("home")

        # Всё ок, подтверждаем email
        token.user.is_active = True  # если вы создаёте пользователей как неактивных до подтверждения
        token.user.save()
        token.revoke()
        messages.success(request, "Email успешно подтвержден!")
        return redirect("auth_login")


class ResendVerificationView(generic.FormView):
    """Повторная отправка емейл со ссылкой на подтверждение регистрации"""

    def get(self, request, *args, **kwargs):
        # Берём email из сессии
        email = request.session.get("pending_verification_email")
        if not email:
            messages.error(request, "Email для повторной отправки не найден.")
            return redirect("auth_login")

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, "Email уже подтверждён.")
            else:
                send_email_verification(user)
                messages.success(request, "Письмо для подтверждения email отправлено повторно.")
            # Очищаем email из сессии, чтобы не отправлять снова случайно
            request.session.pop("pending_verification_email", None)
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")

        # Редирект на страницу логина после обработки
        return redirect("auth_login")

""" ============================= Сброс и восстановление пароля ================================ """

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset_form.html'
    form_class = forms.MyPasswordResetForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Инструкции по сбросу пароля отправлены на email")
        return super().form_valid(form)


class PasswordResetConfirmView(generic.FormView):
    form_class = forms.MySetPasswordForm
    template_name = "auth/password_reset_confirm.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.uidb64 = kwargs.get("uidb64")
        self.token = kwargs.get("token")

        # Получаем пользователя
        try:
            uid = urlsafe_base64_decode(self.uidb64).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None

        if self.user is None:
            messages.error(request, "Неверная ссылка для сброса пароля")
            return redirect("/password_reset/")

        # Проверяем токен через UserToken
        token_obj = UserToken.objects.filter(
            token=self.token, user=self.user, token_type="password_reset"
        ).first()

        if not token_obj or not token_obj.is_valid():
            messages.error(request, "Ссылка истекла или недействительна")
            return redirect("/password_reset/")

        self.token_obj = token_obj
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Передаём user в форму, чтобы SetPasswordForm корректно работала"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        self.token_obj.revoke()
        messages.success(self.request, "Пароль успешно изменён")
        return super().form_valid(form)

```

---

## 4) urls.py

`user/urls_auth.py`

```python
from django.urls import path
from user.views import views_auth

urlpatterns = [
    path('registration/', views_auth.RegistrationView.as_view(), name='auth_registration'),
    path('login/', views_auth.LoginView.as_view(), name='auth_login'),
    path('logout/', views_auth.LogoutView.as_view(), name='auth_logout'),
    path('email_verify/', views_auth.EmailVerifyView.as_view(), name='auth_email_verify'),
    path('email_resend_verification/', views_auth.ResendVerificationView.as_view(), name='auth_email_resend_verification'),
    path('password_reset/', views_auth.PasswordResetView.as_view(), name='auth_password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views_auth.PasswordResetConfirmView.as_view(), name='auth_password_reset_confirm'),
]
```

