# Агрегация и аннотация

---

| **Метод**     | **Описание**                                    | **Возвращает** | **Пример**                                                  |
| ------------- | ----------------------------------------------- | -------------- | ----------------------------------------------------------- |
| `aggregate()` | Вычисляет общее значение (сумма, среднее, макс) | `dict`         | `Book.objects.aggregate(Avg('year_published'))`             |
| `annotate()`  | Добавляет вычисляемое поле к каждому объекту    | `QuerySet`     | `Book.objects.values('author').annotate(count=Count('id'))` |
| `count()`     | Количество объектов в выборке                   | `int`          | `Book.objects.filter(author='Пушкин').count()`              |

---

### 🔹 `aggregate()`

Выполняет **агрегацию по всей выборке**.  
Возвращает словарь с одним или несколькими агрегатами.

Например, средний год публикации всех книг:

```python
from django.db.models import Avg

result = Book.objects.aggregate(Avg('year_published'))
print(result['year_published__avg'])  # например: 1987.4
```

---

### 🔹 `annotate()`

Добавляет **вычисляемое поле** к каждому объекту или группе.  
Например, число книг у каждого автора:

```python
from django.db.models import Count

author_counts = Book.objects.values('author').annotate(count=Count('id'))
for item in author_counts:
    print(item['author'], item['count'])
```

---

### 🔹 `count()`

Возвращает количество объектов в QuerySet.  
Это сокращённая форма агрегата `Count(*)`.

Например, сколько книг написал Пушкин:

```python
book_count = Book.objects.filter(author='Пушкин').count()
print(book_count)
```

