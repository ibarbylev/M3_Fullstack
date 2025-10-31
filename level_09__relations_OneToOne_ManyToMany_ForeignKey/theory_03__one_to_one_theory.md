Связь **один к одному (One-to-One)** означает:    
каждой записи одной таблицы соответствует НЕ БОЛЕЕ одной записи другой таблицы.
И наоборот.

---

## 📘 Класс `OneToOneField`

Для реализации связи один к одному в Django используется поле:

```python
models.OneToOneField()
```

### Сигнатура:

```python
OneToOneField(
    to,                          # модель, с которой устанавливается связь
    on_delete,                   # поведение при удалении связанной записи
    parent_link=False,           # используется в наследовании
    related_name=None,           # имя обратной связи
    related_query_name=None,     # имя для обратных запросов
    limit_choices_to=None,
    ...)
```

---

## 🧱 Пример: Профиль пользователя
Классический пример:  
- использование встроенной модели пользователя (`User`) 
- и собственной модели `Profile`, куда добавлены поля, которых нет в `User`

```python
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)  # отчество
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

```

🔍 Здесь:

* `Profile.user` — это связь один к одному с `User`.
* Один `User` имеет один `Profile`.
* Если пользователь удаляется — его `Profile` тоже удаляется (`on_delete=models.CASCADE`).

---

## 🔁 Обратный доступ

Вы можете обращаться к профилю из `User`:

```python
user = User.objects.get(username="john")
profile = user.profile
```

Чтобы изменить имя обратного доступа:

```python
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_profile')
```

Теперь:

```python
user.custom_profile
```

---

## ✅ Когда использовать OneToOneField

* Вы хотите **расширить** существующую модель (например, `User` → `Profile`).
* Каждая запись **должна иметь только одну связанную запись** в другой таблице.
* Не нужно хранить всё в одной таблице (из соображений логики или оптимизации).

---

## Создание и связывание объектов

```python
# Создаём пользователя и профиль
user = User.objects.create(username="Иван")
profile = Profile.objects.create(user=user, patronymic="Иваныч")

# Или привязываем вручную
profile = Profile()
profile.user = user
profile.save()
```

