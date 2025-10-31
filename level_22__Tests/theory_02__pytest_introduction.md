## Описание пакета**

**`pytest-django`** — это плагин для **pytest**, который добавляет поддержку тестирования Django-проектов.

[https://pytest-django.readthedocs.io/en/latest/](https://pytest-django.readthedocs.io/en/latest/)

**Установка:**

```bash
pip install pytest-django
```

---

## **Основные возможности**

Пакет не просто запускает Django-тесты — он глубоко интегрирован с фреймворком:

| Возможность                           | Что делает                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 🔹 **Настройка Django окружения**     | Автоматически поднимает Django-среду перед тестами (`settings`, `INSTALLED_APPS`, `DATABASES` и т.д.)   |
| 🔹 **Интеграция с ORM**               | Создаёт и очищает тестовую базу данных; позволяет использовать ORM напрямую (модели, запросы, миграции) |
| 🔹 **Фикстуры для Django**            | Предоставляет готовые фикстуры (`db`, `transactional_db`, `client`, `admin_client`, `rf` и т.д.)        |
| 🔹 **Поддержка DRF**                  | Можно тестировать REST API через `APIClient`, `APIRequestFactory`, сериализаторы и вьюхи                |
| 🔹 **Работа с settings**              | Через фикстуру `settings` можно временно изменять конфигурацию Django в тестах                          |
| 🔹 **Совместимость с pytest-plugins** | Работает с другими плагинами pytest (`pytest-cov`, `pytest-xdist`, `pytest-mock` и др.)                 |

---

## Что именно можно проверить с помощью `pytest-django`?`

### Django-часть:

* **Модели и ORM:**

  * сохранение, валидацию, каскадное удаление;
  * сигналы (`post_save`, `pre_delete` и т.д.);
  * запросы и фильтрацию (`Model.objects.filter(...)`).

* **Формы и шаблоны:**

  * корректность форм, валидации и рендеринга;
  * контекст шаблонов, содержимое HTML.

* **Views и middleware:**

  * ответы клиентских запросов (`client.get()`, `client.post()` и т.п.);
  * редиректы, коды статусов, контекст.

* **Админка:**

  * доступ к страницам, CRUD через `admin_client`.

---

### DRF-часть:

* Проверять **эндпоинты API** через `APIClient`:
* Тестировать **сериализаторы**:
* Проверять **права доступа**, **аутентификацию** и **фильтры**.
* Использовать `APIRequestFactory` для низкоуровневых unit-тестов без базы данных.

---

## Основные настройки

Создайте файл **`pytest.ini`** в корне проекта:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
python_files = tests.py test_*.py *_tests.py
addopts = --reuse-db
```

🔸 `DJANGO_SETTINGS_MODULE` — обязательная настройка; указывает, где взять `settings.py`.

🔸 `python_files` — шаблон имен тестовых файлов.

🔸 `--reuse-db` — ускоряет тесты, повторно используя базу данных (если схема не изменилась).

---

## Фикстуры и конструкторы тестов

`pytest-django` предоставляет специальные **фикстуры** (тестовые данные для проверки):

| Фикстура                                | Назначение                                                                      |
| --------------------------------------- | ------------------------------------------------------------------------------- |
| `db`                                    | Подключает тестовую базу данных; очищается после теста                          |
| `transactional_db`                      | Использует транзакции; подходит для тестов, где нужно проверить откат изменений |
| `client`                                | Django-тестовый клиент (имитация HTTP-запросов)                                 |
| `admin_client`                          | Авторизованный клиент от имени администратора                                   |
| `rf`                                    | `RequestFactory` — создаёт объект запроса для unit-тестов views                 |
| `settings`                              | Позволяет временно менять `settings`                                            |
| `django_user_model`                     | Доступ к модели пользователя (Custom User)                                      |
| `django_db_setup` / `django_db_blocker` | Управление созданием БД вручную                                                 |

---

## Примеры тестов

### Тест модели:

```python
import pytest
from myapp.models import Book

@pytest.mark.django_db
def test_book_creation():
    book = Book.objects.create(title="Pytest Guide")
    assert Book.objects.count() == 1
    assert book.title == "Pytest Guide"
```

### Тест view:

```python
@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.content
```

### Тест DRF API:

```python
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_books_api():
    client = APIClient()
    response = client.get('/api/books/')
    assert response.status_code == 200
```

### Использование фикстуры `settings`:

```python
def test_debug_is_false(settings):
    settings.DEBUG = False
    assert not settings.DEBUG
```

---

## ⚡ **Дополнительно**

* **Параметризация:**

  ```python
  @pytest.mark.parametrize('title', ['One', 'Two'])
  def test_create_books(title):
      book = Book.objects.create(title=title)
      assert book.title == title
  ```

* **Использование mock:**

  ```python
  from unittest.mock import patch

  @patch('myapp.views.send_email')
  def test_send_email(mock_send, client):
      client.post('/contact/', {'name': 'Test'})
      mock_send.assert_called_once()
  ```

