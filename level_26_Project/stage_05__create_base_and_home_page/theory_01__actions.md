Задача этого этапа — создать домашнюю страницу, которая будет отображать всю статику.

Добавляем папки:
* `templates`
* `static`
* `media`

В `media/products` сразу же переносим содержимое папки `static/img/products` из шаблона.

В `static` - всю статику.

В `templates` - файл `home.html`.

Наш план действий:

1. "Запустить" этот шаблон по имени домена (нулевой ссылке) без статики.
   * CBV должна отображать эту страницу пока без логики, как статичную страницу
2. Добавить ссылки на статику (сделать вид похожим на вид шаблона).
3. Добавить логику в CBV и сделать страницу полноценной
4. Выделить хэдеры и футеры в `base.html`, а `home.html` сделать вложенным шаблоном


## 1. "Запустить" этот шаблон по имени домена (нулевой ссылке) без статики.

Добавляем в HomeView имя шаблона

```python
class HomeView(generic.TemplateView):
    template_name = 'home.html'
```

Сайт запустился и страница отображается как в шаблоне!

Но рано радоваться — мы должны правильно раздать статику,  
иначе в продакшн мы увидим только голый HTML.

## 2. Добавить ссылки на статику (сделать вид похожим на вид шаблона).

В начале шаблона добавляем тег
```html
{% load static %}
```

И меняем:
```html
<link rel="stylesheet" href="../static/css/main.css">

...

<script src="../static/js/main.js"></script>
```

на:
```html
<link rel="stylesheet" href="{% static 'css/main.css' %}">

...

<script src="{% static 'js/main.js' %}"></script>
```

## 3. Добавить логику в CBV и сделать страницу полноценной

Меняем тип CBV и добавляем модель:

```python
from shop.models import Product

class HomeView(generic.ListView):
    model = Product
    template_name = 'home.html'
```

Теперь в шаблон автоматически уходит список всех объектов Продуктов.

```html
{% for product in object_list %}
    {{ product.name }}
{% endfor %}
```

Меняем вывод всех продуктов в шаблоне на более компактный:

```html
            <div class="product-grid">
                {% for product in object_list %}

                <!-- Card 1: Citra Hops -->
                    <a href="product-citra-hops.html" class="product-card-link">
                        <div class="product-card">
                                <img src="{{ product.image.url }}" alt="{{ product.name }}" class="product-card__image">                            <div class="product-card__info">
                                <h4 class="product-card__name">{{ product.name }}</h4>
                                <p class="product-card__price">${{ product.price }}</p>
                                <p class="product-card__description">{{ product.description|truncatechars:70 }}</p>
                            </div>
                        </div>
                    </a>
                
                {% endfor %}
            </div>
```

Для отображения фото продукта важно не забыть:
1. установить `pip install Pillow`
2. в `settings.py` установить путь к media:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

```

3. и добавить в `main/urls.py` следующий код:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**РЕЗУЛЬТАТ**:

Теперь главная страница отображается как на шаблоне и при этом статика раздаётся правильно.

Правда, мы пока не добавили пагинацию и ссылки на страницы продуктов.

## 4. Выделить хэдеры и футеры в `base.html`, а `home.html` сделать вложенным шаблоном

Делим страницу home.html на базовый шаблон и шаблон самой страницы.

В базовый шаблон включаем хэдеры и футеры по следующему принциу:

#### Базовый шаблон (base.html)

```html
{% load static %} %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мой сайт{% endblock %}</title>
</head>
<body>

    <header>
        <h1>Мой сайт</h1>
    </header>

{% block content %}
    <!-- класс main для авторизации отличается от прочих -->
    <main>
    </main>
{% endblock %}

    <footer>
        

</body>
</html>
```


## Шаблон страницы (hrml.html)

Использует базовый и заполняет блоки.

```html
{% load static %} %}
{% extends "base.html" %}

{% block title %}Страница{% endblock %}

{% block content %}
<h2>Это контент страницы</h2>
<p>Текст страницы...</p>
{% endblock %}
```

