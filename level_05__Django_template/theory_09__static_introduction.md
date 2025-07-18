В Django есть два основных способа подключения и использования статики (CSS, JS, изображения):
* 1 Статика на уровне всего проекта
* 2 Статика внутри каждого приложения

---

## ✅ 1. **Статика на уровне всего проекта**

Это глобальные статические файлы, которые не относятся к конкретному приложению. Обычно сюда помещают общие стили, скрипты и картинки.

### Шаги:

#### 🔧 В `settings.py`:

```python
# Каталог, в котором будут собираться все статики (после collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# URL, по которому будет доступна статика
STATIC_URL = '/static/'

# Папки, из которых Django будет собирать статику
STATICFILES_DIRS = (
    BASE_DIR / "static",
)

# ВАЖНО: на забудьте создать папку 'static' в корне проекта
```

#### 📁 Структура:

```
myproject/
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── main/
│   └── settings.py
```

#### 🧩 В шаблоне (`base.html` или любом другом):

```html
{% load static %}  <!-- Должно быть в первой строке html-файла! -->
. . .
<!-- Должно быть внутри header -->
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.min.css' %}"></head>
. . .
<!-- Должно быть в самом конце body -->
<script src="{% static 'js/script.js' %}"></script>
```


#### Давайте теперь изменим index.html, чтобы увидеть результат:
```django
{% extends "base.html" %}
{% load static %}


{% block title %}Main page{% endblock %}


{% block content %}
    <div class="py-5 text-center">
        <h1 class="display-4">Добро пожаловать на сайт!</h1>
        <p class="lead">Это главная страница. Bootstrap подключён и работает 🎉</p>
    </div>

    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <img src="{% static 'img/sample.jpg' %}" class="card-img-top" alt="Пример">
                <div class="card-body">
                    <h5 class="card-title">Карточка 1</h5>
                    <p class="card-text">Пример карточки с Bootstrap. Можно использовать для товаров, профилей и прочего.</p>
                    <a href="#" class="btn btn-primary">Подробнее</a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Карточка 2</h5>
                    <p class="card-text">Просто пример второй карточки. Можешь скопировать и адаптировать под свой контент.</p>
                    <a href="#" class="btn btn-success">Действие</a>
                </div>
            </div>
        </div>
    </div>
{% endblock %}

```
---

## ✅ 2. **Статика внутри каждого приложения**

Каждое приложение может иметь свою собственную папку `static`, чтобы логически отделить ресурсы.

### 📁 Пример структуры:

```
blog/
├── static/
│   └── blog/
│       ├── css/
│       │   └── blog.css
│       └── js/
│           └── blog.js
```

> Обратите внимание: внутри папки `static/` должно быть подкаталог с **именем приложения** (`blog/`), иначе Django может не найти файлы корректно.

### 🔧 В `settings.py`:

Здесь ничего нового — `STATICFILES_DIRS` обычно не используется для таких стилей. Главное — `STATIC_URL` должен быть определён.

### 🧩 В шаблоне:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/blog.css' %}">
```

---

## ⚠️ Отличие между ними:

| Пункт         | Статика проекта             | Статика приложения                     |
| ------------- | --------------------------- | -------------------------------------- |
| Расположение  | В корне проекта (`/static`) | Внутри каждого app (`app/static/app/`) |
| Использование | Для общих файлов            | Для изолированных модулей              |
| Указывается в | `STATICFILES_DIRS`          | Нет (Django найдёт сам)                |

---

## 🔄 Команда `collectstatic`

Когда вы будете деплоить проект (например, на продакшн), нужно собрать все статики в одну папку:

```bash
python manage.py collectstatic
```

Все файлы из `STATICFILES_DIRS` и `app/static/app/` будут собраны в `STATIC_ROOT`.


