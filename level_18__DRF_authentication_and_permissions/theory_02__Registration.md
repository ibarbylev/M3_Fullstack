## 🔹 Как сделать регистрацию под разные типы аутентификации

### 1. `BasicAuthentication`

* **Регистрация**: обычный `POST /register/`, создаём пользователя.
* **Аутентификация**: клиент в каждом запросе шлёт `Authorization: Basic <base64(login:password)>`.
* **Плюс**: регистрация максимально простая, ничего дополнительно не требуется.

---

### 2. `SessionAuthentication`

* **Регистрация**: та же (создание пользователя через API или админку).
* **Логин**: отдельный эндпоинт `/login/`, который вызывает `django.contrib.auth.login()`.
* После успешного логина у клиента появляется **cookie `sessionid`**, которая автоматически используется в следующих запросах.
* **Выход**: `django.contrib.auth.logout()`.

Пример (в `urls.py`):

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

---

### 3. `TokenAuthentication`

* Используем **DRF TokenAuth** (`rest_framework.authtoken`).
* **Регистрация**: стандартная (создаём `User`).
* **После регистрации** можно выдать токен:

  ```python
  from rest_framework.authtoken.models import Token
  from django.contrib.auth.models import User

  user = User.objects.create_user("alex", password="pass123")
  token = Token.objects.create(user=user)
  print(token.key)  # Этот ключ юзер будет использовать
  ```
* Клиент шлёт:

  ```
  Authorization: Token <ключ>
  ```

Можно настроить автоматическую выдачу токена при регистрации (через сигнал `post_save`).

---

### 4. `JWT (JSON Web Token)`

* Устанавливаем **djangorestframework-simplejwt**.
* **Регистрация**: создаём `User`.
* **Логин**: отдельный эндпоинт `/api/token/`, куда клиент передаёт `username` и `password`.
  В ответ DRF выдаёт:

  ```json
  {
    "access": "<jwt_access_token>",
    "refresh": "<jwt_refresh_token>"
  }
  ```
* В следующих запросах клиент шлёт:

  ```
  Authorization: Bearer <jwt_access_token>
  ```

---

### 5. `OAuth2` (через django-oauth-toolkit)

* Здесь регистрация пользователей та же.
* Но кроме пользователя, создаётся ещё **OAuth-приложение** (client_id, client_secret).
* Логин происходит по стандарту OAuth2 (`/o/token/`, grant types: password, refresh, client credentials и т.д.).
* Токены (`access_token`, `refresh_token`) выдаёт сервер, а клиент сохраняет их.

---

### 6. `Custom Authentication`

* Регистрация — стандартная.
* Но на этапе входа ты сам решаешь, что выдавать пользователю:

  * HMAC-ключ,
  * API key,
  * одноразовый токен,
  * или даже требовать второй фактор (TOTP, SMS, email).

---

## ⚡ Итог

* **Регистрация (создание пользователя) всегда одна и та же**.
* **Различие только в том, что происходит после регистрации:**

  * `BasicAuth` → сразу используешь `username:password`.
  * `SessionAuth` → нужен вход (`/login/`) и сессионный cookie.
  * `TokenAuth` → после регистрации генеришь токен.
  * `JWT` → отдельный эндпоинт для выдачи токенов.
  * `OAuth2` → клиент получает токен через стандартный OAuth flow.

