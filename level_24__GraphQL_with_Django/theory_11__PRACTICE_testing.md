## 9. Тестирование GraphQL с pytest

### 9.1 Установка необходимых пакетов

```bash
pip install pytest pytest-django graphene-django
```

* `pytest-django` — интеграция pytest с Django.
* `graphene-django` уже нужен для GraphQL, чтобы тестировать схему.

В `pytest.ini` добавьте:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = main.settings
python_files = tests.py test_*.py *_tests.py
```

---

### 9.2 Настройка клиента для GraphQL

Создадим фикстуру для клиента GraphQL:

```python
# myapp/tests/test_graphql.py
import pytest
from graphene_django.utils.testing import graphql_query
from django.contrib.auth import get_user_model
from myapp.models import Author, Book, BookDetail

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")

@pytest.fixture
def author(db):
    return Author.objects.create(name="Толстой")

@pytest.fixture
def book(db, author):
    book = Book.objects.create(title="Война и мир", author=author, year_published=1869)
    BookDetail.objects.create(book=book, summary="Описание", page_count=1225)
    return book
```

* `db` — позволяет использовать базу данных для тестов.
* Фикстуры `user`, `author`, `book` создают тестовые объекты.

---

### 9.3 Тестирование запроса

```python
def test_all_books_query(client, book):
    query = """
    query {
        allBooks {
            id
            title
            detail {
                summary
                pageCount
            }
        }
    }
    """
    response = client.post("/graphql/", {"query": query}, content_type="application/json")
    data = response.json()["data"]["allBooks"]
    
    assert len(data) == 1
    assert data[0]["title"] == "Война и мир"
    assert data[0]["detail"]["pageCount"] == 1225
```

* Используем `client.post` для отправки запроса на `/graphql/`.
* Проверяем, что данные возвращаются корректно.

---

### 9.4 Тестирование мутации

```python
def test_create_book_mutation(client, author, user):
    client.force_login(user)
    mutation = f"""
    mutation {{
        createBook(
            title: "Анна Каренина",
            authorId: {author.id},
            yearPublished: 1877,  # ← добавили
            summary: "Описание",
            pageCount: 864
        ) {{
            book {{
                id
                title
                detail {{ summary pageCount }}
            }}
        }}
    }}
    """

    response = client.post("/graphql/", {"query": mutation}, content_type="application/json")
    json_data = response.json()
    assert "errors" not in json_data, json_data.get("errors")
```

* `client.force_login(user)` — авторизуем пользователя для мутации.
* Проверяем, что книга и её детали создались корректно.

---

### 9.5 Тестирование обновления и удаления

Пример обновления книги:

```python
def test_update_book_mutation(client, book, user):
    client.force_login(user)
    mutation = f"""
    mutation {{
        updateBook(id: {book.id}, title: "Новая Война и мир") {{
            book {{ id title }}
        }}
    }}
    """
    response = client.post("/graphql/", {"query": mutation}, content_type="application/json")
    data = response.json()["data"]["updateBook"]["book"]
    assert data["title"] == "Новая Война и мир"
```

Пример удаления книги:

```python
def test_delete_book_mutation(client, book, user):
    client.force_login(user)
    mutation = f"""
    mutation {{
        deleteBook(id: {book.id}) {{ ok }}
    }}
    """
    response = client.post("/graphql/", {"query": mutation}, content_type="application/json")
    assert response.json()["data"]["deleteBook"]["ok"] is True
    assert not Book.objects.filter(id=book.id).exists()
```

---

### 9.6 Итог

* Через pytest можно тестировать **и запросы, и мутации GraphQL**.
* Фикстуры позволяют создавать тестовые объекты (книги, авторы, пользователи).
* Используем `client.post("/graphql/", {"query": ...})` и проверяем JSON-ответ.
* Можно проверять 
  * аутентификацию, 
  * разрешения, 
  * создание, 
  * обновление 
  * и удаление объектов.
