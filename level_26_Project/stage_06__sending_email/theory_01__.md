# Отправка почты из Django

Чтобы **проверить реальную отправку письма** через ваш конфиг в `settings.py`, проще всего использовать **Django shell**:

---

## 1. SMTP настройки в `settings.py` 

Удобно наиболее чувствительные данные хранить в `local_settings.py`

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_URL = 'http://127.0.0.1:8000'

# Дла загрузки приватных данных из local_settings.py
try:
    from .local_settings import *  # noqa: F401, F403
except ImportError as e:
    print(e)
```

Кстати, `SITE_URL = 'http://127.0.0.1:8000'` лучше задать в в `local_settings.py`.  

Чтобы на локальной машине был lokalhost, а на продакшн - имя домена.

---

## 2. Проверить работу почты можно через Django shell

```bash
./manage.py shell
```

---

## 3. Тестовое письмо (ручное)

```python
from django.core.mail import send_mail

send_mail(
    subject="Тестовое письмо",
    message="Если ты читаешь это — SMTP работает!",
    from_email=None,  # возьмётся DEFAULT_FROM_EMAIL
    recipient_list=["ваш_email@domain.com"],
)
```

Если всё настроено правильно — письмо придёт **реально**.

---

### Альтернатива: отправка HTML письма

```python
from django.core.mail import EmailMultiAlternatives

msg = EmailMultiAlternatives(
    subject="Тест HTML",
    body="Ваш почтовый клиент не поддерживает HTML",
    from_email=None,
    to=["ваш_email@domain.com"],
)
msg.attach_alternative("<h1>Привет!</h1><p>SMTP работает ✅</p>", "text/html")
msg.send()
```

## 4. Тестовое письмо (pytest)

`tests/test_email.py`

```python
import pytest
from django.core import mail
from django.core.mail import send_mail

from main.settings import *
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.mark.django_db
def test_send_email():

    # действие
    send_mail(
        subject="Тест",
        message="Проверка отправки письма.",
        from_email="no-reply@example.com",
        recipient_list=["user@example.com"],
    )

    # проверяем, что письмо попало в outbox
    assert len(mail.outbox) == 1

    email = mail.outbox[0]

    assert email.subject == "Тест"
    assert email.body == "Проверка отправки письма."
    assert email.from_email == "no-reply@example.com"
    assert email.to == ["user@example.com"]
   ```