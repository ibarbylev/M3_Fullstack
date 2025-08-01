Django Template Language (DTL) — это **встроенный язык шаблонов в Django**, предназначенный для генерации HTML (или других текстовых форматов).

---
**DTL** позволяет:

* вставлять данные в HTML (`{{ имя }}`),
* управлять логикой отображения (`{% if %}`, `{% for %}`),
* использовать шаблоны и наследование (`{% extends %}`, `{% block %}`, `{% include %}`),
* применять фильтры и теги (`{{ дата|date:"d.m.Y" }}`),
* изолировать логику представления от шаблона (иначе пришлось бы "собирать" шаблон с помощью `f-string` непосредственно в Python-коде).

---

### 🔍 Пример:

```html
    <ul>
      {% for book in books %}
        <li>
          {{ book.title }} — {{ book.author }}
          [<a href="{% url 'book-detail' book.pk %}">Детализация</a>]
          [<a href="{% url 'book-edit' book.pk %}">Изменить</a>]
          [<a style="color: red" href="{% url 'book-delete' book.pk %}">🗑️ Удалить книгу</a>]
        </li>
      {% empty %}
        <li>Книг нет</li>
      {% endfor %}
    </ul>
```

---

### 🎯 Особенности DTL:

| Особенность                | Описание                                                                 |
| -------------------------- |--------------------------------------------------------------------------|
| **Безопасность**           | По умолчанию экранирует HTML (меняет `<` на `&lt;` и т.д.).              |
| **Ограниченная логика**    | Нельзя выполнять произвольный (вредоносный) Python-код                   |
| **Шаблонное наследование** | Позволяет делать базовые шаблоны и переопределять блоки.                 |
| **Простота**               | Минимальный синтаксис, легко учить.                                      |
| **Интеграция**             | Глубоко встроен в Django: поддерживает `context_processors`, шаблоны в приложениях и пр. |

---



