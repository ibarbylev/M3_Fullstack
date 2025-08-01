С помощью QuerySet можно создавать новые записи БД. 

---

### Варианты добавления рассмотрим на примере этой модели 

```python
from django.db import models

class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()
```

---

### 1. **`create()`**

```python
Book.objects.create(author="Толстой", title="Война и мир", year_published=1869)
```

* 💡 Создаёт и сохраняет объект в одну строку.

---

### 2. **Создание экземпляра, затем `save()`**

```python
book = Book(author="Достоевский", title="Преступление и наказание", year_published=1866)
book.save()
```

* 💡 Позволяет изменять объект перед сохранением.

---

### 3. **`update_or_create()`**

```python
Book.objects.update_or_create(
    title="Мастер и Маргарита",
    defaults={"author": "Булгаков", "year_published": 1967}
)
```

* 💡 Обновит, если существует, иначе создаст.

---

### 4. **`get_or_create()`**

```python
Book.objects.get_or_create(
    title="1984",
    defaults={"author": "Оруэлл", "year_published": 1949}
)
```

* 💡 Не обновляет, только получает или создаёт.

---

### 5. **`bulk_create()` — массовое добавление**

```python
Book.objects.bulk_create([
    Book(author="Пушкин", title="Евгений Онегин", year_published=1833),
    Book(author="Гоголь", title="Мёртвые души", year_published=1842),
])
```

* 💡 Быстрое массовое добавление, без вызова `save()` для каждой записи.

---

### 6. **Через `values()` и `Model(**dict)`**

```python
data = {"author": "Чехов", "title": "Вишнёвый сад", "year_published": 1904}
book = Book(**data)
book.save()
```

* 💡 Полезно при обработке словарей.

---

### 7. **Создание пользовательских методов добавления записей `from_queryset()`**
 

По умолчанию, обычный objects — это экземпляр класса `models.Manager`,   
который предоставляет стандартные методы (all(), filter(), create(), и т.д.).

Но Django позволяет добавлять собственные методы в QuerySet.  

Например, создадим метод `.my_personal_creator()`, который:
- создаёт объект `self.create(**kwargs)`;
- выводит лог `print(...)`;
- возвращает объект.

#### 7.1. Создаём новый метод:

```python
class BookQuerySet(models.QuerySet):
    def my_personal_creator(self, **kwargs):
        book = self.create(**kwargs)
        print("Создана книга:", book.title)
        return book
```
#### 7.2. Подключаем менеджер к модели Book

Метод `as_manager()` превращает BookQuerySet в полноценный Manager:

```
class Book(models.Model):
    ...
    objects = BookQuerySet.as_manager()
```

⚠️ Внимание!!!
Модели, где `objects` не добавлен, по-прежнему будут работать с дефолтным Менеджером.

#### 7.3. Теперь мы можем использовать этот метод в Менеджере:

```python
Book.objects.my_personal_creator(author="Замятин", title="Мы", year_published=1924)
```

#### Почему называется `from_queryset()`?

`as_manager()` — это просто обёртка над более универсальным методом from_queryset().

То есть:
```python
objects = BookQuerySet.as_manager()
# То же самое, что:
objects = models.Manager.from_queryset(BookQuerySet)()
```

Но `as_manager()` короче и чаще используется.