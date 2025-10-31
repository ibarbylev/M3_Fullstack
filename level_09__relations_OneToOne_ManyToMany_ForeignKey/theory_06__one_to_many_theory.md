Связь **один ко многим** (One-to-Many) означает:
одна запись таблицы A может быть связана со многими записями таблицы B (один автор может иметь несколько книг),  
но каждая запись модели B связана только с одной записью модели A (книга может иметь ТОЛЬКО одного автора).

Если же книга тоже может иметь несколько авторов, то это уже не наш случай (Many-to-Many).

---

## 📘 Теория: Один ко многим в Django

### 🔹 Пример: Автор и Книги

### 🔧 Модели

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

---

## 🔍 Объяснение ключевых моментов

### `ForeignKey`

* Задаётся в модели, которая находится **на стороне "много"**
* Указывает на модель, с которой установлена связь (на сторону "один")
* `on_delete=models.CASCADE` — поведение при удалении автора:

  * если удалить автора, удалятся и все связанные с ним книги

---

## 🔄 Обратный доступ (обратно — от "одного" ко "многим")

### Пример:

```python
author = Author.objects.get(id=1)
books = author.book_set.all()
```

* `book_set` — это **обратный менеджер** по умолчанию, добавляемый Django
* Можно задать имя для обратной связи через параметр `related_name`

### С `related_name`:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

Теперь доступ к книгам автора будет:

```python
books = author.books.all()
```

---

## 🧠 Кратко

| Что                   | Где                                              | Пример                        |
| --------------------- | ------------------------------------------------ | ----------------------------- |
| Установить связь      | в модели "много"                                 | `author = ForeignKey(Author)` |
| Получить автора книги | `book.author`                                    |                               |
| Получить книги автора | `author.book_set.all()` или `author.books.all()` |                               |

