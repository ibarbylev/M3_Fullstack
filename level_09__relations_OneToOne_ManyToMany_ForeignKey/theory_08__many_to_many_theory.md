Связь **многие ко многим** (Many-to-Many) означает:
одна запись таблицы A может быть связана со многими записями таблицы B (один автор может иметь несколько книг).  
И наоборот: каждая запись модели B может быть связана со многими записями таблицы A.  
(ОДИН автор может иметь МНОГО книг, а ОДНА книга может иметь МНОГО авторов).


## 🔧 Django: как задать связь many-to-many?

В Django такая связь создаётся с помощью поля `ManyToManyField`,   
которое можно разместить В ЛЮБОЙ (подчёркнуто!!!) из моделей,  
и Django создаст промежуточную таблицу автоматически (если это не указана явно).

---

### 🔹 Модели

```python
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='books')
```

---

## Итак, зафиксируем эту ключевую идею:

`ManyToManyField` можно объявить В ЛЮБОЙ из связанных моделей и результат будет одинаковым:   
Django создаст промежуточную таблицу с двумя внешними ключами.


### 🔹 Вариант 1 — `ManyToManyField` в `Book` (наш пример выше)

```python
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='books')
```

Теперь:

* `book.genres.all()` — жанры книги
* `genre.books.all()` — книги этого жанра

---

### 🔹 Вариант 2 — `ManyToManyField` в `Genre`

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    books = models.ManyToManyField(Book, related_name='genres')
```

Теперь:

* `genre.books.all()` — книги жанра
* `book.genres.all()` — жанры книги

Имена одинаковы, потому что `related_name='genres'` теперь используется на стороне `Book`.

---

### ⚠️ Важно: нельзя дублировать связь

Нельзя объявить `ManyToManyField` В ОБЕИХ моделях ОДНОВРЕМЕННО:

```python
# ❌ Ошибка: обе модели содержат ManyToManyField
class Book(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

class Genre(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
```

---

## Явное (ручное) задание промежуточной таблицы в связи `ManyToMany`.


### Когда это нужно?

Иногда простого `ManyToManyField` недостаточно, например:

* нужно добавить **дополнительные поля** в связке (дата, роль, комментарий и т.д.)
* нужен **явный контроль** над промежуточной таблицей

В таких случаях используется параметр `through=<Model>`.

---

#### Пример: Книга, Жанр и Промежуточная таблица

**Наши требования**:
* Книга может относиться к нескольким жанрам
* Для каждой связи нужно сохранить **дату присвоения жанра**

---

##### Обновлённые модели

```python
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()
    
    genres = models.ManyToManyField(
        Genre,
        through='BookGenre',
        related_name='books'
    )

class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'genre')  # чтобы не было дубликатов
```

---

### Как добавить связь в это случае?

```python
# Создать объекты
author, _ = Author.objects.get_or_create(name="Артур Конан Дойл")
detective, _ = Genre.objects.get_or_create(name="Детектив")
book = Book.objects.create(author=author, title="Собака Баскервилей", year_published=1902)

# Установить связь вручную через промежуточную таблицу можно ТОЛЬКО явно обратившись к модели BookGenre!!!
# (стандартные инструменты Django для ManyToMany здесь уже не помогут)
BookGenre.objects.create(book=book, genre=detective)
```
Исправляем ошибку (так как у нас промежуточная модель задана по умолчанию:

```python
book.genres.set([detective])
```
---

#### ⚠️ Супер-важно!!!

При использовании `through=BookGenre`:

* нельзя использовать `book.genres.add(...)` или `set()`
* нужно работать напрямую через `BookGenre`

---

#### Примеры запросов

1. Получить жанры-книги:

```python
book.genres.all()
```

2. Получить книги-жанры:

```python
genre.books.all()
```

3. Получить дату присвоения жанра:

```python
bg = BookGenre.objects.get(book=book, genre=detective)
print(bg.assigned_at)
```

#### Резюмируем:

| Элемент                             | Назначение                                |
| ----------------------------------- | ----------------------------------------- |
| `ManyToManyField(..., through=...)` | Явная связка с таблицей                   |
| Промежуточная модель (`BookGenre`)  | Хранит связи и доп. данные                |
| `add()`, `set()`                    | Не работают — заменяются явным `create()` |

Как видим, явное создание своей промежуточной таблицы:
 - снижает удобство 
 - и уменьшает часть стандартных возможностей,  

которые Django предоставляет "из коробки" для связей типа ManyToManyField.