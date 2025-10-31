Разберём по шагам устройство `urls.py` в **каждом приложении Django**, с акцентом на:

1. **Синтаксис `urlpatterns`**
2. **Содержимое функции `path()`**
3. **Динамические URL-адреса**
4. **Обработка ошибок адресации**

---

## 🔹 1. `urlpatterns` — список маршрутов

Это **главная переменная** в каждом `urls.py`, содержащая список всех маршрутов:

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
```

* Это **обязательное имя переменной** — Django будет искать именно `urlpatterns`.
* Это обычный **список**, куда можно добавлять маршруты с помощью `path()` или `re_path()`.

---

## 🔹 2. Содержимое `path()` (и/или `re_path()`)

```
path(route, view, kwargs=None, name=None)
```

| Аргумент | Назначение                                                        |
| -------- | ----------------------------------------------------------------- |
| `route`  | Относительный URL-шаблон (без слэша в начале)                     |
| `view`   | Обработчик запроса: функция или CBV (через `.as_view()`)          |
| `kwargs` | Необязательные аргументы для view (редко используется)            |
| `name`   | Имя маршрута, удобно для ссылок `{% url 'имя' %}` или `reverse()` |

### Пример:

```
path('contact/', views.contact_view, name='contact')
```

---

## 🔹 3. Динамические URL-адреса

Позволяют извлекать значения из URL и передавать их в `view`:

```
# blog/urls.py
urlpatterns = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/', views.post_by_slug, name='post_by_slug'),
]
```

| Синтаксис     | Тип                   | Пример в URL      |
| ------------- |-----------------------| ----------------- |
| `<int:id>`    | Целое число           | `/123/`           |
| `<str:name>`  | Строка без `/` внутри | `/john/`          |
| `<slug:slug>` | Слаг                  | `/my-first-post/` |
| `<uuid:uid>`  | UUID                  | `/550e8400-.../`  |
| `<path:sub>`  | Строка с `/` внутри   | `/folder/file/`   |

### Соответствующий view:

```
def post_detail(request, post_id):
    # post_id уже приведён к int
    ...
```

---

## 🔹 4. Обработка ошибок адресации (404 и др.)

Если путь не совпал ни с одним маршрутом из `urlpatterns`, Django автоматически вызывает ошибку `404 Not Found`.

Вы можете переопределить стандартные обработчики:

```
# main/urls.py
handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'
```

### Пример собственного 404:

```
# myapp/views.py
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
```

> ⚠️ Эти обработчики работают **только в режиме DEBUG = False** (иначе показывается отладочная страница).

---

## 🔹 Альтернатива: `re_path()`

Для сложных регулярных выражений:

```
from django.urls import re_path

urlpatterns = [
    re_path(r'^archive/(?P<year>[0-9]{4})/$', views.archive),
]
```

> Обычно `path()` предпочтительнее: проще читать и использовать.

---

## 🔹 Итог: структура `urls.py` в приложении

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:id>/', views.article_detail, name='article'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
```

Хорошая практика — **всегда давать имена маршрутам**, использовать `include()` на уровне проекта, и обрабатывать ошибки красиво.

