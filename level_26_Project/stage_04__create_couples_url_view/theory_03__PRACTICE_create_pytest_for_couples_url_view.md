```python
# TODO продумать реальные ссылки, имена вью и шаблонов
```

Отделяем данные тестов (список URL, вью, шаблон, статус) от самих тестов, чтобы:

1. Один набор тестов проверял только **маршрутизацию (url → view)**.
2. Второй — **HTTP-код и шаблон** (уже после того, как view-ы готовы).

---

## Новая структура файлов

```
tests/
│
├── data/
│   ├── urls_user_data.py
│   ├── urls_shop_data.py
│   └── urls_admin_data.py
│
├── test_urls_resolve.py        # только проверка маршрутов
└── test_urls_response.py       # проверка статуса и шаблонов
```

---

## Содержимое файлов данных

### `tests/data/urls_user_data.py`

```python
# TODO продумать реальные ссылки, имена вью и шаблонов



from user.views import views_auth, views_account

user_urls = [
    # Аутентификация
    ("auth_registration", views_auth.RegistrationView, "users/auth/registration.html", 200),
    ("auth_login", views_auth.LoginView, "users/auth/login.html", 200),
    ("auth_logout", views_auth.LogoutView, None, 200),
    ("auth_email_verify", views_auth.EmailVerifyView, "???", 200),
    ("auth_email_resend_verification", views_auth.ResendVerificationView, "???", 200),
    ("auth_password_reset", views_auth.PasswordResetView, "???", 200),
    ("auth_password_reset_confirm", views_auth.PasswordResetConfirmView, "???", 200),
    ("auth_password_change", views_auth.PasswordChangeView, "???", 200),

    # Управление аккаунтом
    ("account_profile", views_account.ProfileView, "???", 200),
    ("account_orders", views_account.OrderHistoryView, "???", 200),
]
```

---

### `tests/data/urls_shop_data.py`

```python
from shop import views as shop_views

shop_urls = [
    # Home Page
    ("home", shop_views.HomeView, "???", 200),

    # Products
    ("shop_home", shop_views.HomeView, "???", 200),
    ("shop_products", shop_views.ProductListView, "???", 200),
    ("shop_products_search", shop_views.ProductSearchView, "???", 200),
    ("shop_product_detail", shop_views.ProductDetailView, "{'pk': 1}", 200),
    ("shop_product_review_add", shop_views.ProductReviewAddView, "???", 200),
    ("shop_product_reviews", shop_views.ProductReviewListView, "???", 200),

    # Orders
    ("shop_order", shop_views.OrderListView, "???", 200),
    ("shop_order_add", shop_views.OrderAddView, "???", 200),
    ("shop_order_remove", shop_views.OrderRemoveView, "???", 200),
    ("shop_order_update", shop_views.OrderUpdateView, "???", 200),
    ("shop_order_checkout", shop_views.OrderCheckoutView, "???", 200),
    ("shop_order_detail", shop_views.OrderDetailView, "???", 200),
    ("shop_orders", shop_views.OrderHistoryView, "???", 200),

    # Payments
    ("shop_payment_process", shop_views.PaymentProcessView, "???", 200),
    ("shop_payment_confirm", shop_views.PaymentConfirmView, "???", 200),
    ("shop_payment_cancel", shop_views.PaymentCancelView, "???", 200),
    
    # Reviews
    ("shop_review_add", shop_views.ReviewAddView, "???", 200),
    ("shop_review_update", shop_views.ReviewUpdateView, "???", 200),
    ("shop_review_delete", shop_views.ReviewDeleteView, "???", 200),
]
```

---

### `tests/data/urls_admin_data.py`

```python
from adminapp import views as admin_views

admin_urls = [
    ("admin", admin_views.AdminDashboardView, "???", 200),
    ("admin_stats", admin_views.AdminStatsView, "???", 200),
    ("admin_search", admin_views.AdminSearchView, "???", 200),
    ("admin_permissions", admin_views.AdminPermissionsView, "???", 200),
]
```

---

## 1. Тест маршрутизации (`test_urls_resolve.py`)

Тесть только проверяем соответствие url и имени вью.  
Т.е. базовая проверка скелета маршрутизации.

```python
import pytest
from django.urls import reverse, resolve
from tests.data.urls_user_data import user_urls
from tests.data.urls_shop_data import shop_urls
from tests.data.urls_admin_data import admin_urls


@pytest.mark.parametrize("url_name, view_func, kwargs, expected_status",
                         user_urls + shop_urls + admin_urls)
def test_url_resolves_correct_view(url_name, view_func, kwargs, expected_status):
    """
    Проверяет, что reverse(url_name) соответствует правильному классу view.
    """
 
    if isinstance(kwargs, dict):
        url = reverse(url_name, kwargs=kwargs)
    else:
        url = reverse(url_name)
    resolved = resolve(url)
    
    assert resolved.func.view_class == view_func, (
        f"{url_name}: ожидался {view_func.__name__}, "
        f"получен {resolved.func.view_class.__name__}"
    )
```

---

## 2. Тест отклика (`test_urls_response.py`)

Этот тест уже проверяет полноценную работу вью (в будущем!)

```python
import pytest
from django.urls import reverse, resolve
from tests.data.urls_user_data import user_urls
from tests.data.urls_shop_data import shop_urls
from tests.data.urls_admin_data import admin_urls


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, view_func, kwargs, expected_status",
                         user_urls + shop_urls + admin_urls)
def test_url_response_and_view(client, url_name, view_func, kwargs, expected_status):
    """
    Проверяет:
    1) URL корректно реверсится (с kwargs если нужно)
    2) URL резолвится в ожидаемую view
    3) Сервер отвечает ожидаемым статус-кодом
    """
    # Реверс с/без kwargs
    if isinstance(kwargs, dict):
        url = reverse(url_name, kwargs=kwargs)
    else:
        url = reverse(url_name)

    # Проверяем, что resolve(url) → правильная View
    resolved = resolve(url)
    assert resolved.func.view_class == view_func, (
        f"{url_name}: ожидалась View {view_func.__name__}, "
        f"получена {resolved.func.view_class.__name__}"
    )

    # Проверка ответа
    response = client.get(url)
    assert response.status_code == expected_status, (
        f"{url_name}: ожидался статус {expected_status}, "
        f"получен {response.status_code}"
    )
```

---

## Как запускать:

```bash
pytest tests/test_urls_resolve.py      # только проверка маршрутов
pytest tests/test_urls_response.py     # проверка статусов и шаблонов
```

## Порядок запуска тестов

1. На начальном этапе: 
   * ставим `_` перед `test_urls_response.py`
   * запускаем `test_urls_resolve.py`,  
   * и постепенно добавляем (исправляем) код до тех пор, пока не пройдут все тесты.
   
2. На следующем этапе наоборот - работаем с `test_urls_response.py`:
   * ставим `_` перед `test_urls_resolve.py`
   * убираем `_` у `_test_urls_response.py`
   * и снова постепенно добавляем (исправляем) код до тех пор, пока не пройдут все тесты.