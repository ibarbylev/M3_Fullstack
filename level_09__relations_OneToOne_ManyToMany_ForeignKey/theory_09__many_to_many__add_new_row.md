## Создание и связывание объектов для связи ManyToMany

Эта "необычная" связь имеет свои "необычные" методы, которых нет ни в OneToOne, ни в OneToMany.

## 📦 Модели 

(Берём вариант без `through` — обычный случай, чтобы по-максимyму рассмотреть "коробочные" методы Django)
```python
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    year_published = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='books')
```

---


### 🔹 Способ 1: создать книгу, а потом добавить жанры

```python
# 1. Создаём жанры
author, _ = Author.objects.get_or_create(name="Джон Р. Р. Толкин")
fantasy, _ = Genre.objects.get_or_create(name="Фантастика")
drama, _ = Genre.objects.get_or_create(name="Драма")

# 2. Создаём книгу
book = Book.objects.create(author=author, title="Хоббит, или Туда и обратно", year_published=1937)

# 3. Метод .add добавляет новые жанры к книге
#    (если fantasy и drama уже были — метод .add просто проигнорирует их)
book.genres.add(fantasy, drama)
```

---

### 🔹 Способ 2: создать жанры, создать книгу, потом связать списком

```python
# Создаём автора и книгу
author, _ = Author.objects.get_or_create(name="Олдос Хаксли")
book, _  = Book.objects.get_or_create(author=author, title="О дивный новый мир", year_published=1932)

# Добавляем жанры сразу списком
# метод .set полностью заменит список жанров у данной книги
book.genres.set([fantasy, drama]) 
```

---

### 🔹 Способ 3: создать книгу без жанров, потом очистить и добавить

```python
author, _ = Author.objects.get_or_create(name="Кормак Маккарти")
book = Book.objects.create(author=author, title="Дорога", year_published=2006)

# Добавить жанр
book.genres.add(fantasy)

# Очистить жанры
book.genres.clear()
book.genres.set([fantasy, drama]) 
```

---

## 📌 Альтернатива: через жанр получить книги

```python
# Найти все книги жанра
genre = Genre.objects.get(name="Фантастика")
books = genre.books.all()
```

---

## ⚠️ Важно

| Метод                  | Что делает                         |
| ---------------------- | ---------------------------------- |
| `add(obj1, obj2, ...)` | Добавляет связь (не удаляя старые) |
| `set([obj1, obj2])`    | Заменяет все существующие связи    |
| `remove(obj)`          | Удаляет конкретную связь           |
| `clear()`              | Удаляет все связи                  |


