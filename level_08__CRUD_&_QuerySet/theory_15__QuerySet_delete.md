# Методы удаления данных


---

### 🗑️ Таблица: Методы удаления данных в Django

| Метод                            | Что делает                                      | Пример                                                                  | Вызывает сигналы  |
| -------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- |-------------------|
| `obj.delete()`                   | Удаляет **один объект**                         | `obj = Book.objects.get(id=1); obj.delete()`                            | ✅ Да              |
| `QuerySet.delete()`              | Удаляет **все записи по фильтру**               | `Book.objects.filter(year__lt=1900).delete()`                           | ⛔ Частично¹       |
| `Model.objects.all().delete()`   | Удаляет **все записи модели**                   | `Book.objects.all().delete()`                                           | ⛔ Частично¹       | 
| `bulk_delete()` (Django 5.0+)    | Быстро удаляет множество объектов               | `Book.objects.filter(active=False).bulk_delete()`                       | ❌ Нет             |
| Удаление каскадом (`CASCADE`)    | Удаляет связанные объекты при удалении родителя | `Author.objects.get(id=1).delete()` (удалит и связанные `Book`)         | ✅ Да (рекурсивно) |
| `TRUNCATE TABLE`                 | Полностью очищает таблицу (raw SQL)             | `cursor.execute("TRUNCATE TABLE myapp_book RESTART IDENTITY CASCADE;")` | ❌ Нет             |
| Удаление через админку           | Удаляет выбранные записи через Django Admin     | Выделение объектов в админке и нажатие "Удалить"                        | ✅ Да              |
| "Мягкое" удаление (`is_deleted`) | Помечает объект как удалённый, не удаляя из БД  | `obj.is_deleted = True; obj.save()` или `obj.safe_delete()`             | ✅ Да (`save()`)   |

---

### 🧾 Примечания

**¹ Частично** — `QuerySet.delete()` и `.all().delete()` не вызывают `Model.delete()`,   
поэтому **сигналы `pre_delete` и `post_delete` не срабатывают для каждого объекта**,  
а только один раз — на уровне QuerySet.

---


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
* Но это потребует изменение менеджера модели, чтобы исключить из фильтра поля,  где `is_deleted=True` 

### Пример создания менеджера для "мягкого удаления"

#### 1. Добавляем новое поле
```python
from django.db import models

class Book(models.Model):
    ...
    is_deleted = models.BooleanField(default=False)

```

#### 2. Создаём свой менеджер:

```python
from django.db import models

class BookManager(models.Manager):
    def get_queryset(self):
        # Исключаем помеченные на удаление
        return super().get_queryset().filter(is_deleted=False)
```


#### 3. Регистрируем новый менеджер в модели

```python

class Book(models.Model):
    ...
    is_deleted = models.BooleanField(default=False)
    
    # Указываем наш менеджер вместо default objects
    objects = BookManager()

```

---

## 🚨 Важно

* `delete()` **не вызывает** метод `save()` и **не обновляет** время (`auto_now`).
* Перед удалением не забывайте сделать резервное копирование!!!

