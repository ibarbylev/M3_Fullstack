## Создаём первое приложение `blog`

### Создаём приложение:

```bash
./manage.py startapp blog
```

### Обновлённая структура проекта:

```commandline
tree
.
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── wsgi.py
├── db.sqlite3
├── main
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt

```


---


## 📁 Папка `blog/`

Это Django-приложение, в котором будет находиться логика блога.


---

### `views.py`

**Назначение:**
Содержит функции-представления (views), которые обрабатывают HTTP-запросы и возвращают ответы.

**Пример содержимого:**

```
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать в наш блог!")
```

---

### Что нужно сделать, чтобы `blog` заработал?

#### 1. Зарегистрировать `blog` в `settings.py`

Откройте `main/settings.py` и добавьте `blog` в список `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...
    'blog',
]
```

---

#### 2. Подключить маршруты `blog` к `urls.py`

Обновите файл `main/urls.py`:

```

from django.contrib import admin
from django.urls import path
from blog.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Подключаем маршруты нашего приложения]
```


#### 3. Создать маршруты в самом приложении `blog`

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница нашего блога
]
```

#### 4. Запуск проекта


Теперь при открытии [http://localhost:8000/](http://localhost:8000/) в браузере будет отображаться:

```
Добро пожаловать в наш блог!
```

### Обновлённая структура проекта:

```commandline
tree
.
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── main
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt

```
