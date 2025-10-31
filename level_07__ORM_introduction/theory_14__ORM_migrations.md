В Django **миграции** — это способ внесения изменений в структуру БД,   
синхронизируя её с текущими моделями Python. 

---

### 🔹 **Определение**

**Миграции** — это файлы, генерируемые Django для отражения изменений в моделях (`models.py`) в структуре базы данных. 

Создаются на уровне приложения.  
Являются альтернативой ручному написанию SQL по созданию / изменению модели (таблицы).

---

### 🔹 **Задачи миграций**

| Задача                              | Описание                                                            |
| ----------------------------------- | ------------------------------------------------------------------- |
| 📦 Отражение изменений в моделях    | Добавление, изменение или удаление полей и моделей                  |
| 🔄 Управление версионированием БД   | Позволяет переходить вперёд и назад по изменениям (как git-коммиты) |
| 🛡 Безопасность и воспроизводимость | Стандартизированное и безопасное применение изменений в любой среде |
| 🗂 Автоматическое создание SQL      | Django сам генерирует SQL-запросы под нужную СУБД                   |

---

### 🔹 **Команды миграций**

#### ✅ 1. Создание миграций на основе изменений в `models.py`

```bash
python manage.py makemigrations
```

#### ✅ 2. Применение миграций (изменения БД)

```bash
python manage.py migrate
```

#### ✅ 3. Применение конкретного приложения

```bash
python manage.py migrate <app_name>
```

#### ✅ 4. Просмотр SQL-кода миграции (до выполнения)

```bash
python manage.py sqlmigrate <app_name> <migration_name>
```

Пример:

```bash
python manage.py sqlmigrate myapp 0001
```

#### ✅ 5. Просмотр статуса миграций

```bash
python manage.py showmigrations
```

---

### 🔹 Пример работы

1. Изменили модель:

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
```

2. Создали миграции:

```bash
python manage.py makemigrations
```

3. Посмотрели SQL:

```bash
python manage.py sqlmigrate myapp 0001
```

Пример вывода:

```sql
CREATE TABLE "myapp_book" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" varchar(100) NOT NULL,
    "author" varchar(100) NOT NULL
);
```

4. Применили миграции:

```bash
python manage.py migrate
```

