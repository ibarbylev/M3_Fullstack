## Links & HiperLinked

Этот модуль содержит сериализаторы для моделей `Author` и `Book`.   
С помощью них данные могут представляться в двух форматах:

1. **Вложенный список объектов книг**   
   — когда внутри каждого автора возвращается полный список его книг   
   — с подробной информацией (`AuthorWithListBooksSerializer`).
2. **Список гиперссылок на книги**   
   — когда вместо полной информации о книгах возвращаются    
   — ссылки на соответствующие объекты API (`AuthorWithBookLinksSerializer`).

Для выбора второго варианта нужного достаточно добавить `?mode=links`

---

### serializers.py

```python
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'year_published']


class AuthorWithListBooksSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


# --- вариант с гиперссылками ---
class AuthorWithBookLinksSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Author
        fields = ['url', 'id', 'name', 'books']
        extra_kwargs = {
            'url': {'view_name': 'author-detail', 'lookup_field': 'pk'}
        }
```

---

### views.py

```python
from rest_framework import viewsets
from .models import Author, Book
from .serializers import (
    AuthorWithListBooksSerializer,
    AuthorWithBookLinksSerializer,
    BookSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    def get_serializer_class(self):
        mode = self.request.query_params.get('mode')
        if mode == 'links':
            return AuthorWithBookLinksSerializer
        return AuthorWithListBooksSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

### urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
```

---

Теперь:

*  GET: `http://127.0.0.1:8000/api/authors/` → список авторов с **вложенными книгами (объекты)**
*  GET: `http://127.0.0.1:8000/api/authors/?mode=links` → список авторов с **гиперссылками на книги**

## Выводы

### 1. Плюсы разных форматов

**Список объектов (вложенные книги)**

* 🔹 **Плюсы:**

  * Полная информация о книгах сразу в ответе, не нужно делать дополнительные запросы.
  * Удобно для клиентских приложений, которые сразу отображают все данные.
* ⚠️ **Минусы:**

  * Если у автора много книг, ответ может быть большим → увеличивается трафик.
  * Сложнее обновлять отдельные книги через API (нужен отдельный PUT/PATCH на каждый объект книги).

**Список гиперссылок на книги**

* 🔹 **Плюсы:**

  * Ответ компактный — только ссылки на книги.
  * Легче масштабировать и работать с большим количеством данных.
  * Клиент может делать дополнительные запросы к отдельным книгам по мере необходимости.
* ⚠️ **Минусы:**

  * Нужно делать дополнительные запросы, чтобы получить данные каждой книги.

---

### 2. Добавление объектов через ViewSet

* **Автор с вложенными книгами (список объектов)**

  * Через текущий сериализатор `AuthorWithListBooksSerializer` добавление **нового автора возможно**,  
     но новые книги **не создаются автоматически** через поле `books`, потому что оно `read_only=True`.
  * Чтобы добавить книги при создании автора, нужно сделать кастомный метод `create` 
     или использовать `WritableNestedModelSerializer` из сторонних пакетов.

* **Автор с гиперссылками (список ссылок)**

  * Через `AuthorWithBookLinksSerializer` также можно создать автора,  
  но добавление книг через ссылки **не поддерживается напрямую**, т.к. поле `books` тоже `read_only=True`.

То есть, **в обоих вариантах добавлять книги сразу через сериализатор нельзя**, только отдельными запросами к `/books/`.

---

### 3. Примеры URL для разных форматов

* `GET: http://127.0.0.1:8000/api/authors/` → список авторов с **вложенными книгами (объекты)**
* `GET: http://127.0.0.1:8000/api/authors/?mode=links` → список авторов с **гиперссылками на книги**
* `GET: http://127.0.0.1:8000/api/authors/1/` → конкретный автор с книгами (объекты)
* `GET: http://127.0.0.1:8000/api/authors/1/?mode=links` → конкретный автор с книгами (гиперссылки)
* `POST: http://127.0.0.1:8000/api/authors/` → добавить нового автора
* `POST: http://127.0.0.1:8000/api/books/` → добавить новую книгу и привязать к автору



