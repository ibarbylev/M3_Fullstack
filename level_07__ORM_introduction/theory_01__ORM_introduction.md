**Django ORM** (Object-Relational Mapping) — это система,  
которая позволяет программисту работать с базой данных через Python-код (без SQL-запросов).   
**Django ORM**  преобразует Python-объекты в таблицы базы данных и наоборот.   

---

## 🔹 Пример

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    published_year = models.IntegerField()
```

Теперь вы можете выполнять такие действия:

```python
# Добавление записи
Book.objects.create(title="1984", author="George Orwell", published_year=1949)

# Поиск
Book.objects.filter(author="George Orwell")

# Обновление
book = Book.objects.get(title="1984")
book.published_year = 1950
book.save()

# Удаление
book.delete()
```

---

## ✅ Преимущества Django ORM

| Преимущество                 | Описание                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| **1. Упрощение кода**        | Нет необходимости писать SQL — всё через Python-классы и методы.                    |
| **2. Безопасность**          | Django ORM экранирует параметры запросов, защищая от SQL-инъекций.                  |
| **3. Независимость от СУБД** | Вы можете сменить СУБД (например, с SQLite на PostgreSQL) без переписывания логики. |
| **4. Интеграция с Django**   | ORM тесно связан с формами, валидацией, админкой и другими частями фреймворка.      |
| **5. Миграции**              | Управление схемой базы данных через миграции (`makemigrations`, `migrate`).         |
| **6. Читабельность**         | Запросы легче читать, тестировать и сопровождать, чем чистый SQL.                   |
| **7. Кеширование**           | Повторные запросы могут кэшироваться, экономя время.                                |
| **8. Связи моделей**         | Удобная работа с отношениями (ForeignKey, ManyToMany и т.д.).                       |

