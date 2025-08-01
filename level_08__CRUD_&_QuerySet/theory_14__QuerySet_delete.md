# Методы удаления данных

## 1. `delete()`: Удаление конкретного объекта

```python
obj = MyModel.objects.get(id=1)
obj.delete()
```

* Удаляет **одну запись**.
* Вызывает `delete()` всех связанных объектов (если есть `on_delete=CASCADE`).

---

## 2. `QuerySet.delete()`: Удаление нескольких объектов

```python
MyModel.objects.filter(status='inactive').delete()
```

* Удаляет **все объекты**, подходящие под фильтр.
* Работает **на уровне базы данных**, минуя вызов `Model.delete()` у каждого объекта (что может пропустить сигналы).

---

## 3. `Model.objects.all().delete()`: Удаление всех записей модели

```python
MyModel.objects.all().delete()
```

* Полностью очищает таблицу.
* Обычно используется в тестах или для сброса данных.

---

## 4. Удаление через `bulk_delete()` (с Django 5.0)

```python
MyModel.objects.filter(active=False).bulk_delete()
```

* **Быстрее**, чем `QuerySet.delete()`, но **не вызывает сигналы** (`pre_delete`, `post_delete`).
* Доступно только с Django 5.0+.

---

## 5. Удаление связанных объектов (ForeignKey / CASCADE)

Если у вас есть модель с внешним ключом:

```python
class Author(models.Model):
    name = models.CharField(...)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

Удаляя автора:

```python
Author.objects.get(id=1).delete()
```

— удаляются и все связанные книги (`Book`) — если установлен `on_delete=models.CASCADE`.

---

## 6. Очистка таблицы без удаления (обнуление)

Иногда нужно **"удалить" данные**, но оставить саму таблицу:

```python
MyModel.objects.all().delete()
# или через raw SQL:
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE myapp_mymodel RESTART IDENTITY CASCADE;")
```
- `RESTART IDENTITY` - Сбрасывает счётчики автоинкремента (`id`, `serial`, `BIGSERIAL` и т.п.) до 1
- `CASCADE` - автоматически очищает связанные по `FK` таблицы
---

## 7. Удаление через админку

* Можно выделить записи в Django Admin и удалить через интерфейс.
* Вызывает `ModelAdmin.delete_model()` и `Model.delete()`.

---

## 8. Безопасное ("мягкое") удаление

* Можно переопределить `delete()`и добавить поле `is_deleted`
* Тогда при удалении это поле будет становиться `True`
* Но это потребует изменение менеджера модели, чтобы исключить из фильтра поля,  
  где `is_deleted=True`

---

## 🚨 Важно

* `delete()` **не вызывает** метод `save()` и **не обновляет** время (`auto_now`).
* Перед удалением не забывайте сделать резервное копирование!!!

