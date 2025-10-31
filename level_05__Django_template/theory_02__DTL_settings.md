## 📍 Где `DTL` указывается в `settings.py`

Хорошая новость - DTL установлен в Django по умолчанию:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # DTL
        'DIRS': [BASE_DIR / 'templates'],  # директории с вашими шаблонами
        'APP_DIRS': True,  # искать шаблоны в папке templates внутри приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Здесь важно:

* `'BACKEND': 'django.template.backends.django.DjangoTemplates'` — это указание на использование **DTL**.


---

`'APP_DIRS': True` указывает на возможность создавать свою папку `templates` внутри КАЖДОГО приложения.  
Например:
```
shop/
├── templates/
│   └── shop/
│       └── product_list.html
├── views.py

```

---


## ✅ Альтернативы DTL

### 1. **Jinja2**

Самая популярная альтернатива.

Чтобы использовать **Jinja2** в Django:

#### Установка:

```bash
pip install Jinja2
```

#### Добавление в `settings.py`:

Возможно одновременное использование DTL и другие языки шаблонов в одном проекте:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'jinja_templates'],
        'APP_DIRS': False,  # Jinja2 не поддерживает APP_DIRS
        'OPTIONS': {
            'environment': 'main.jinja2.environment',  # путь к функции настройки окружения
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]
```
Помимо этого нужен дополнительный py-файл в той же папке, что и `settings.py`:
```
main/
├── jinja2.py  ← вот он
├── settings.py
```

#### Пример файла `jinja2.py` в корне проекта:

```python
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
```

Вы можете использовать оба шаблонизатора в одном проекте: `.html` в `templates/` — через DTL, а шаблоны в `jinja_templates/` — через Jinja2.

---

### 2. **Mako** (реже используется)

```python
'BACKEND': 'django.template.backends.mako.MakoTemplates'
```

Для этого потребуется сторонняя библиотека [django-mako-plus](https://github.com/dcramer/django-mako-plus).

---

### 3. **Chameleon**, **Cheetah** и другие

Менее популярны и требуют ручной интеграции.

---

## 🟡 Сравнение DTL и Jinja2 (вкратце)

| Особенность        | DTL       | Jinja2                       |
| ------------------ | --------- | ---------------------------- |
| Скорость           | Умеренная | Быстрая                      |
| Поддержка в Django | Встроена  | Требует настройки            |
| Функциональность   | Базовая   | Расширенная (макросы и т.п.) |
| Поддержка фильтров | Есть      | Гибкая и расширяемая         |

---

## 📊 Сравнение DTL vs Jinja2

| **Критерий**                 | **Django Template Language (DTL)**                                       | **Jinja2**                                                               |
| ---------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| **Разработчик**              | Встроен в Django                                                         | Отдельная библиотека, интегрируется через Django backend                 |
| **Скорость**                 | Медленнее (меньше возможностей компиляции)                               | Быстрее за счёт компиляции шаблонов в байткод                            |
| **Синтаксис**                | Упрощённый, ограниченный                                                 | Более мощный, похож на Python                                            |
| **Вызов функций**            | Запрещён (напрямую)                                                      | Разрешён: можно вызывать функции, передавать аргументы                   |
| **Работа со списками**       | Ограниченная: нет list slicing, генераторов и т.д.                       | Полная: поддержка срезов, фильтрации, генераторов                        |
| **Фильтры и теги**           | Ограничены, строго контролируются Django                                 | Расширяемые и гибкие                                                     |
| **Безопасность (XSS)**       | HTML экранирование по умолчанию                                          | Тоже экранирует HTML по умолчанию                                        |
| **Шаблон-наследование**      | Есть `{% extends %}`, `{% block %}`                                      | Есть те же конструкции                                                   |
| **Кастомные фильтры/теги**   | Использует `@register.filter`, `@register.simple_tag` и отдельный модуль | Использует обычные Python-функции                                        |
| **Логика в шаблоне**         | Очень ограничена (и это хорошо)                                          | Поддерживает более сложную логику, включая циклы, `if/elif`, `set`       |
| **Работа с `static`, `url`** | Через `{% static %}`, `{% url %}`                                        | Используются функции `static()` и `url()` через `jinja2_env.environment` |
| **Поддержка `APP_DIRS`**     | Да                                                                       | Нет (нужно указывать `DIRS` явно)                                        |
| **Типичный стиль проекта**   | Легче удерживать шаблоны "глупыми"                                       | Позволяет больше логики, но требует самодисциплины                       |

---

## 📝 Примеры шаблонов

### ▶️ DTL-пример (`templates/shop/product.html`):

```django
{% extends "base.html" %}

{% block content %}
  <h1>{{ product.name }}</h1>
  <p>{{ product.description }}</p>
  <p>Цена: {{ product.price }} ₽</p>

  {% if product.available %}
    <p>В наличии</p>
  {% else %}
    <p>Нет в наличии</p>
  {% endif %}

  <a href="{% url 'shop:cart_add' product.id %}">Добавить в корзину</a>
{% endblock %}
```

---

### ▶️ Jinja2-пример (`jinja2/shop/product.html`):

```jinja2
{% extends "base.html" %}

{% block content %}
  <h1>{{ product.name }}</h1>
  <p>{{ product.description }}</p>
  <p>Цена: {{ product.price }} ₽</p>

  {% if product.available %}
    <p>В наличии</p>
  {% else %}
    <p>Нет в наличии</p>
  {% endif %}

  <a href="{{ url('shop:cart_add', product.id) }}">Добавить в корзину</a>
{% endblock %}
```

---

### 🔍 Замечания по примерам:

| Что                | DTL                         | Jinja2                        |
| ------------------ | --------------------------- | ----------------------------- |
| Вызов `url`        | `{% url 'имя' аргументы %}` | `{{ url('имя', аргументы) }}` |
| Наследование/блоки | Одинаково                   | Одинаково                     |
| Условия/циклы      | Очень похожи                | Очень похожи                  |

---

