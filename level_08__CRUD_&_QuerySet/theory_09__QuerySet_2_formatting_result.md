# Форматирование результата
---

| **Метод**       | **Описание**                           | **Возвращает**      | **Пример**                                                               |
| --------------- | -------------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| `values()`      | Возвращает словари с указанными полями | `QuerySet` словарей | `Book.objects.values('author', 'title')`                                 |
| `values_list()` | Возвращает кортежи с указанными полями | `QuerySet` кортежей | `Book.objects.values_list('author', flat=True)`                          |
| `raw()`         | Выполняет сырой SQL-запрос             | `RawQuerySet`       | `Book.objects.raw('SELECT * FROM app_book WHERE year_published > 2000')` |

---

* **`values()`**
  Возвращает выборку в виде словарей, где ключи — имена полей, значения — их значения. Удобно, если нужны только отдельные поля.

  ```python
  books_data = Book.objects.values('author', 'title')
  for book in books_data:
      print(book['author'], book['title'])
  ```

---

* **`values_list()`**
  Возвращает выборку в виде кортежей, содержащих указанные поля. Если используется `flat=True` и выбран одно поле, возвращается плоский список значений.

  ```python
  authors = Book.objects.values_list('author', flat=True)
  for author in authors:
      print(author)
  ```


---
 
* **`raw()`**
  Позволяет выполнить произвольный SQL-запрос и получить объекты модели.

  ```python
  recent_books = Book.objects.raw('SELECT * FROM app_book WHERE year_published > 2000')
  for book in recent_books:
      print(book.title, book.year_published)
  ```


