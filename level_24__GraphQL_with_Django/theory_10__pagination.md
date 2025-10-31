## 8. Пагинация

### 8.1 Зачем нужна пагинация

* Если в базе много книг, возвращать их все сразу неэффективно.
* Пагинация позволяет отдавать данные **частями**, например по 10 записей на страницу.
* GraphQL не навязывает способ пагинации, но есть два популярных подхода:

  1. **Limit / Offset** — простая реализация “страницы N по M элементов”.
  2. **Cursor-based** — более гибкая для больших или постоянно изменяющихся списков.

---

### 8.2 Простая пагинация через аргументы limit и offset

В `schema.py` для списка книг добавим аргументы:

```python
class Query(graphene.ObjectType):
    all_books = graphene.List(
        BookType,
        limit=graphene.Int(),
        offset=graphene.Int()
    )

    def resolve_all_books(root, info, limit=None, offset=None):
        qs = Book.objects.filter(is_deleted=False).order_by("id")
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        return qs
```

* `limit` — сколько записей вернуть.
* `offset` — сколько пропустить с начала.
* Пример запроса:

```graphql
query {
  allBooks(limit: 5, offset: 10) {
    id
    title
  }
}
```

* Этот запрос вернёт **5 книг, начиная с 11-й** (смещение 10).

---

### 8.3 Cursor-based пагинация (Graphene Relay)

Для больших списков лучше использовать Relay:

```python
from graphene import relay
from graphene_django import DjangoObjectType

class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node,)
        fields = ("id", "title", "author")
```

* `relay.Node` добавляет уникальный `id` и поддерживает курсоры.
* Теперь можно создавать соединения (`Connection`) для постраничного запроса:

```python
class Query(graphene.ObjectType):
    book = relay.Node.Field(BookNode)
    all_books = relay.ConnectionField(BookNode.Connection)

    def resolve_all_books(root, info, **kwargs):
        return Book.objects.filter(is_deleted=False).order_by("id")
```

* Пример запроса с курсорами:

```graphql
query {
  allBooks(first: 5, after: "cursor_строка") {
    edges {
      node {
        id
        title
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

* `first` — сколько записей вернуть.
* `after` — курсор, от которого начать.
* `edges` — сами записи + их курсоры.
* `pageInfo` — информация о следующей странице (`hasNextPage`) и курсоре последнего элемента (`endCursor`).

---

### 8.4 Итог

* Для небольших проектов можно использовать **limit/offset**.
* Для больших и динамических данных лучше использовать **cursor-based пагинацию (Relay)**.
* Пагинация в GraphQL позволяет клиенту управлять, **сколько и какие записи** получать.

