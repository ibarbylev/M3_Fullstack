# Оптимизация запросов
---
📌 Суть проблемы "неоптимальности" запросов:

Когда мы обращаемся к связанным моделям (через ForeignKey, ManyToMany и т.п.),  
то Django по умолчанию делает **отдельный(!)** SQL-запрос для каждой связи.   
Это может вызвать проблему N+1 запросов, особенно в циклах.

---

Эти методы решают проблему так:

    `select_related()` — делает SQL JOIN и загружает связанные объекты сразу в одном запросе.
    🔸 Эффективно при связях ForeignKey / OneToOne.

    `prefetch_related()` — делает отдельный запрос к связанным объектам и связывает их в Python.
    🔸 Подходит для ManyToMany и обратных связей.


### В чём смысл?
Меньше запросов → быстрее выполнение кода и меньше нагрузка на базу данных.

| **Метод**            | **Описание**                                                            | **Возвращает** | **Пример**                                       |
| -------------------- | ----------------------------------------------------------------------- | -------------- | ------------------------------------------------ |
| `select_related()`   | Делает JOIN и кэширует связанный объект (FK)                            | `QuerySet`     | `Book.objects.select_related('publisher')`       |
| `prefetch_related()` | Загружает связанные объекты через отдельный запрос и связывает в Python | `QuerySet`     | `Publisher.objects.prefetch_related('book_set')` |

###  Пример моделей для обоих методов:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

class Publisher(models.Model):
    name = models.CharField(max_length=100)
```

---

##  `select_related()`

Используется для **ForeignKey** и **OneToOne** связей.   
Выполняет **SQL JOIN** и сразу загружает связанные объекты.   
Работает эффективно, но **только для "один-к-одному"** или **"многие-к-одному"**.

---


Допустим, вы хотите отобразить список книг **вместе с названием издателя**:

```python
for book in Book.objects.all():
    print(book.title, book.publisher.name)
```

---

## ❌ Без `select_related()`

```
Запрос 1:
SELECT * FROM book;

Цикл по книгам:
┌──────────────────────┐
│ Book 1 (publisher_id=3) │
└──────────────────────┘
  └─ Запрос 2: SELECT * FROM publisher WHERE id=3;

┌──────────────────────┐
│ Book 2 (publisher_id=5) │
└──────────────────────┘
  └─ Запрос 3: SELECT * FROM publisher WHERE id=5;

...

┌──────────────────────┐
│ Book N (publisher_id=X) │
└──────────────────────┘
  └─ Запрос N+1: SELECT * FROM publisher WHERE id=X;
```

🛑 Итого: **1 + N запросов** — неэффективно, особенно при большом количестве книг.

---

## ✅ С `select_related('publisher')`

```python
books = Book.objects.select_related('publisher')
for book in books:
    print(book.title, book.publisher.name)
```

```
Запрос 1:
SELECT book.*, publisher.*
FROM book
JOIN publisher ON book.publisher_id = publisher.id;

Результат:
┌────────────────────────────────────────────┐
│ Book 1 + Publisher.name                    │
│ Book 2 + Publisher.name                    │
│ ...                                        │
│ Book N + Publisher.name                    │
└────────────────────────────────────────────┘
```

✅ Всего: **1 SQL-запрос с JOIN'ом**
🔥 Очень эффективно при связях **ForeignKey** и **OneToOne**

---


## `prefetch_related()`

### Модели:

```python
class Publisher(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
```

Теперь попробуем вывести список издательств и названия их книг:

```python
for publisher in Publisher.objects.all():
    for book in publisher.book_set.all():
        print(publisher.name, book.title)
```

---

## ❌ Что происходит без `prefetch_related()`?

1. Django делает **один запрос** на `Publisher.objects.all()`.
2. Потом — **отдельный запрос на каждое `publisher.book_set.all()`**.
3. Итого: **1 + N** запросов (если 100 издательств — будет 101 запрос).

---

### ✅ Что делает `prefetch_related('book_set')`?

Прежде всего, [что такое `book_set`](./theory_12__what_is_book_set.md)?
```python
publishers = Publisher.objects.prefetch_related('book_set')
for publisher in publishers:
    for book in publisher.book_set.all():
        print(publisher.name, book.title)
```

Django делает:

1. Один запрос на `Publisher.objects.all()`
2. Один запрос на все связанные `Book` (где `publisher_id` в список id)

 Затем Django **в памяти связывает книги с нужными издателями**.  
 Это намного эффективнее: **только 2 SQL-запроса**, независимо от количества издательств.

---

### ❌ Без `prefetch_related()`

(типичная проблема N+1 запросов):

```
Запрос 1:
SELECT * FROM publisher;

Цикл по издателям:
┌─────────────────────┐
│ Publisher 1         │
└─────────────────────┘
  └─ Запрос 2: SELECT * FROM book WHERE publisher_id = 1;

┌─────────────────────┐
│ Publisher 2         │
└─────────────────────┘
  └─ Запрос 3: SELECT * FROM book WHERE publisher_id = 2;

...

┌─────────────────────┐
│ Publisher N         │
└─────────────────────┘
  └─ Запрос N+1: SELECT * FROM book WHERE publisher_id = N;
```

🛑 Всего: **1 + N** SQL-запросов (очень неэффективно при большом количестве данных)

---

### ✅ С `prefetch_related('book_set')`

```
Запрос 1:
SELECT * FROM publisher;

Запрос 2:
SELECT * FROM book WHERE publisher_id IN (1, 2, ..., N);

Связь объектов:
┌──────────────┬──────────────────────────────┐
│ Publisher 1  │ [Book A, Book B]             │
│ Publisher 2  │ [Book C]                     │
│ ...          │ ...                          │
│ Publisher N  │ [Book X, Book Y, Book Z]     │
└──────────────┴──────────────────────────────┘
```

✅ Всего: **2 запроса**, Django сам объединяет в Python связанные объекты.
🔥 Быстро, масштабируемо, удобно.

---

### 📌 Краткое сравнение:

|              | `select_related()`              | `prefetch_related()`                |
| ------------ | ------------------------------- | ----------------------------------- |
| Как работает | SQL JOIN                        | Отдельный SQL + связывание в Python |
| Тип связи    | `ForeignKey`, `OneToOne`        | `ManyToMany`, обратные `ForeignKey` |
| Запросов     | 1                               | 2 (или больше, если много связей)   |
| Когда лучше  | Когда нужен доступ к "родителю" | Когда нужен доступ к "детям"        |



