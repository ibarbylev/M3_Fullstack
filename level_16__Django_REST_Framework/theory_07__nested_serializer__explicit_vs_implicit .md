# Зачем и когда во вложенном сериализаторе нужно указывать `many=True`) 

Всё зависит от модели.

В нашем случае:
- если нужен JSON книг, с полным указанием параметров автора - `many=True` указывать не нужно.
- если нужен JSON авторов, а у каждого автора будет список его книг - нужно указать  `many=True`

Пример:

```python
# models.py
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
```

```python
# serializers.py
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)  # 👈 список книг для каждого автора

    class Meta:
        model = Author
        fields = ["name", "books"]
```

Пример результата:

```json
[
  {
    "name": "Лев Толстой",
    "books": [
      {"title": "Война и мир"},
      {"title": "Анна Каренина"}
    ]
  },
  {
    "name": "Александр Пушкин",
    "books": [
      {"title": "Евгений Онегин"}
    ]
  }
]
```

💡 **Ключевой момент:** `many=True` говорит DRF, что `books` — это **список объектов**, а не один объект.  
Без `many=True` сериализатор ожидал бы **только одну книгу**, и JSON будет выглядеть иначе.

```json
[
  {
    "title": "Война и мир",
    "author": {
      "name": "Лев Толстой"
    }
  },
  {
    "title": "Анна Каренина",
    "author": {
      "name": "Лев Толстой"
    }
  },
  {
    "title": "Евгений Онегин",
    "author": {
      "name": "Александр Пушкин"
    }
  }
]

```

---

## Главное отличие

| Вариант                     | Когда использовать                                                 | Что получается                                                 |
| --------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- |
| `AuthorSerializer()`        | Один связанный объект (`OneToOne`, `ForeignKey`)                   | Вложенный JSON-объект (например, автор внутри книги)           |
| `BookSerializer(many=True)` | Коллекция связанных объектов (`ManyToMany`, обратный `ForeignKey`) | Список вложенных JSON-объектов (например, книги внутри автора) |

---

## Краткая аналогия

* `AuthorSerializer()` → как поле `author = models.ForeignKey(...)` внутри книги → **один объект**.
* `BookSerializer(many=True)` → как обратная связь `books = models.ForeignKey(Author, related_name="books")` → **список объектов**.
