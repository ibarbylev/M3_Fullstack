Начиная с версии 1.8+ Django (чаще всего) распознаёт, что поле будет переименовано.  
Поэтому на этапе миграции, задаст вам уточняющий вопрос:
```django
Was myappmodel.code renamed to myappmodel.my_code (a CharField)? [y/N] 
```
Но может и не распознать.  
Что будет в этом случае?

---

## ❌ **Переименование модели или поля без указания, что это именно переименование**

Когда вы **переименовываете поле или модель в `models.py`**, Django **не знает**, что это было именно *переименование*, а не:

* удаление старого поля/модели и
* создание нового с другим именем.

### 🔴 Что происходит по умолчанию?

Вы, например, переименовали поле:

```python
# было
name = models.CharField(max_length=100)

# стало
title = models.CharField(max_length=100)
```

Когда вы запускаете:

```bash
python manage.py makemigrations
```

Django создаёт миграцию **с удалением `name` (и данных!) и созданием `title`**, то есть:

```python
migrations.RemoveField(
    model_name='book',
    name='name',
),
migrations.AddField(
    model_name='book',
    name='title',
    field=models.CharField(max_length=100),
),
```

---

## ✅ Как правильно переименовывать поле или модель

Используйте `makemigrations --empty`, чтобы **создать пустую миграцию**, и **вручную** укажите `RenameField` или `RenameModel`.

---

### 🔁 Переименование поля: пример

1. Самостоятельно создаём файл миграции, правильно указывая имя приложения (`myapp`) и номер (и имя миграции):
```bash
python manage.py makemigrations myapp --empty --name migration_rename_name_to_title
```

2. В полученном файле миграции меняем параметры списка `operations`:

```python
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('your_app', '0005_previous_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='MyappModel',
            old_name='my_code',
            new_name='code',
        ),
    ]
```
3. Применяем свеже-созданную миграцию:
```bash
python manage.py migrate
```
---

### 🔁 Аналогично - переименование модели: пример

```python
operations = [
    migrations.RenameModel(
        old_name='OldModelName',
        new_name='NewModelName',
    ),
]
```

---

## 📌 Итог

| ❌ Неправильно                           | ✅ Правильно                                           |
| --------------------------------------- | ----------------------------------------------------- |
| Просто переименовали поле в `models.py` | Использовали `makemigrations --empty` и `RenameField` |
| Потеря данных при миграции              | Данные сохраняются, меняется только имя               |

---

