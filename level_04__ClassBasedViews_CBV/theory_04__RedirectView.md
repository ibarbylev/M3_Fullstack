### 🔁 Django RedirectView — краткий обзор и пример

`RedirectView` — это встроенное представление (`django.views.generic.base.RedirectView`), которое используется для перенаправления пользователя с одного URL на другой. Очень удобно для простых редиректов без логики.

---

### 📌 Основные особенности `RedirectView`:

* Используется для HTTP-редиректов (по умолчанию — `301 Permanent`)
* Можно задать фиксированный `url`, либо сгенерировать его динамически через `get_redirect_url()`
* Можно включать параметры из URL

---

### ✅ Простой пример — редирект на внешний сайт

**views.py (необязателен, если не нужно ничего переопределять):**

```python
from django.views.generic.base import RedirectView
```

**urls.py:**

```python
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("github/", RedirectView.as_view(url="https://github.com/", permanent=False)),
]
```

➡ При переходе на `/github/` пользователь будет перенаправлен на GitHub с кодом `302 Found`.
➡ Если `permanent=True`, то редирект на GitHub будет с кодом 301 

### 💡 А в чём разница между 301 и 302?:
- 301 кэшируется браузерами и поисковиками. Используйте только если уверены, что путь навсегда изменился.
- 302 безопаснее для временных или условных переадресаций.

---

### ✅ Пример с динамическим URL и `get_redirect_url()`

**views.py:**

```
from django.views.generic.base import RedirectView
from django.urls import reverse

class ProfileRedirectView(RedirectView):
    permanent = False  # 302 редирект

    def get_redirect_url(self, *args, **kwargs):
        username = self.request.user.username
        return reverse("profile", kwargs={"username": username})
```

**urls.py:**

```
from django.urls import path
from .views import ProfileRedirectView

urlpatterns = [
    path("my-profile/", ProfileRedirectView.as_view(), name="my-profile"),
    path("user/<str:username>/", some_view, name="profile"),  # сюда будет редирект
]
```

➡ При заходе на `/my-profile/` пользователя перебросит на `/user/<его_имя>/`.

---
### 💡 А может ли быть редирект с POST, а не GET запросом?:
- Нет: по стандарту HTTP редиректы всегда обрабатываются через GET-запросы, независимо от исходного метода (POST, PUT и т.п.).

---

### 📝 Когда использовать:

* Для перенаправления на другой сайт или страницу
* Для упрощения маршрутов (`/go-to-login/` → `/accounts/login/`)
* Для обратной совместимости (устаревшие URL)

