DTL позволяет избежать избыточности HTML кода с помощью наследования шаблонов.

Для этого создаётся основной (базовый) шаблон, где обозначаются места для вставок:

## 🧱 1. `base.html` (базовый шаблон)

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мой сайт{% endblock %}</title>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

Теперь, в шаблоне  наследника достаточно прописать ТОЛЬКО содержимое мест вставок.  
(И, разумеется, указать родителя в самом начале)


## 🧱 2. `index.html` (наследуемый шаблон)

```django
{% extends "base.html" %}


{% block title %}Main page{% endblock %}


{% block content %}
    <h1>Main page</h1>
{% endblock %}
```