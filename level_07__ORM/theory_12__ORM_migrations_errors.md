
## ⚠️ Типичные ошибки моделей, вызывающие ошибки миграций

| №  | Ошибка                                                                       | Пример или объяснение                                                                       |
| -- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1  | ❌ **Поле без `null=True`, но без значения по умолчанию**                     | Django требует значение при добавлении поля в таблицу, где уже есть данные                  |
|    | ✅ **Решение**: указать `null=True` или `default=...`                         | `models.CharField(max_length=100, null=True)`                                               |
| 2  | ❌ **Добавление `ForeignKey` без `on_delete`**                                | Django требует явно указать `on_delete` (например, `CASCADE`)                               |
|    | ✅ **Решение**: `models.ForeignKey(..., on_delete=models.CASCADE)`            |                                                                                             |
| 3  | ❌ **Модель без `primary_key`, если не используется `id` по умолчанию**       | При кастомных первичных ключах обязательно указывать `primary_key=True`                     |
| 4  | ❌ **Несуществующее поле в `ForeignKey`, `OneToOneField`, `ManyToManyField`** | Указана связь на модель или поле, которого нет                                              |
| 5  | ❌ **Круговая зависимость между моделями без `related_name` или `through`**   | Пример: два `ManyToManyField` между одними и теми же моделями                               |
| 6  | ❌ **Ошибки в типах полей** (например, строка в `IntegerField`)               | Ошибка может проявиться при миграции, если указано неправильное значение по умолчанию       |
| 7  | ❌ **Переименование модели/поля без `makemigrations --empty`**                | Django воспринимает это как удаление и создание заново (что может привести к потере данных) |
| 8  | ❌ **Имя таблицы уже существует в БД** (особенно при ручных изменениях)       | Django не может создать таблицу, если она уже есть                                          |
| 9  | ❌ **Опечатка в `Meta` (например, `db_table`, `ordering`)**                   | Может вызвать ошибку генерации SQL или несогласованность                                    |
| 10 | ❌ **Модель импортирована, но не зарегистрирована в `INSTALLED_APPS`**        | Миграции не создаются или не применяются                                                    |
| 11 | ❌ **Модель использует нестандартный тип поля, не поддерживаемый СУБД**       | Например, кастомные типы в SQLite                                                           |
| 12 | ❌ **Отсутствие миграции на предыдущие изменения**                            | Вы забыли `makemigrations`, и в `migrate` возникает ошибка несовпадения                     |

---

## 🛠 Примеры с пояснением

### Пример 1: Добавили поле без значения по умолчанию

```python
# models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()  # ошибка!
```

🔴 Ошибка при миграции:

```
You are trying to add a non-nullable field 'year' to book without a default...
```

✅ Правильно:

```python
year = models.IntegerField(default=2000)
# или
year = models.IntegerField(null=True)
```

---

### Пример 2: ForeignKey без on\_delete

```python
author = models.ForeignKey('Author')  # ошибка
```

🔴 Ошибка:

```
TypeError: __init__() missing 1 required positional argument: 'on_delete'
```

✅ Правильно:

```python
author = models.ForeignKey('Author', on_delete=models.CASCADE)
```

---

## 📌 Рекомендации

* Всегда проверяйте изменения перед миграциями: `python manage.py makemigrations` и `sqlmigrate`.
* Используйте `null=True`, если поле может быть пустым.
* Для новых обязательных полей — добавляйте `default=...`.
* Не переименовывайте поля/модели без фиксации миграции заранее.
* Избегайте ручного изменения базы данных без миграций.

