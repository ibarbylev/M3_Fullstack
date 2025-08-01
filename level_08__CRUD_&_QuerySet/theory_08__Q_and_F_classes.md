## ✅ `Q` — логические выражения (AND, OR, NOT)

### 📌 Что делает `Q`

Класс `Q` позволяет:

* комбинировать фильтры с **`&` (AND)**, **`|` (OR)**, **`~` (NOT)**;
* строить условия **динамически**, особенно в сложных случаях;
* использовать **одновременно `AND` и `OR`**, чего нельзя достичь обычным `.filter()` без `Q`.

### 🧠 Синтаксис

```python
from django.db.models import Q

Q(условие1) & Q(условие2)   # AND
Q(условие1) | Q(условие2)   # OR
~Q(условие)                 # NOT
```

### 🧪 Примеры

#### 🔹 Простое `OR`:

```python
# Все пользователи с именем 'admin' ИЛИ email 'test@example.com'
User.objects.filter(Q(username='admin') | Q(email='test@example.com'))
```

#### 🔹 Сложное `AND + OR`:

```python
# Все активные пользователи, у которых возраст < 18 ИЛИ > 65
User.objects.filter(is_active=True).filter(Q(age__lt=18) | Q(age__gt=65))
```

#### 🔹 Отрицание:

```python
# Все пользователи, НЕ активные
User.objects.filter(~Q(is_active=True))
```

#### 🔹 Комбинирование с `.exclude()`:

```python
# Исключить пользователей с именем admin или moderator
User.objects.exclude(Q(username='admin') | Q(username='moderator'))
```

#### 🔹 Динамическое добавление условий:

```python
filters = Q()
if some_condition:
    filters &= Q(is_staff=True)
if other_condition:
    filters |= Q(is_superuser=True)

User.objects.filter(filters)
```

---

## ✅ `F` — сравнение **поля с полем**

### 📌 Что делает `F`

`F` используется для создания запросов, в которых **одно поле сравнивается с другим** в рамках одной записи.

Также `F` полезен для **инкрементов**, **декрементов** и **вычислений**.

### 🧠 Синтаксис

```python
from django.db.models import F

F('другое_поле')
```

---

### 🧪 Примеры

#### 🔹 Сравнение полей:

```python
# Товары, где количество на складе меньше количества заказов
Product.objects.filter(stock__lt=F('ordered'))
```

#### 🔹 Обновление поля на основе другого:

```python
# Увеличить рейтинг на 1
User.objects.update(rating=F('rating') + 1)
```

#### 🔹 Вычитание:

```python
# Уменьшить остаток на складе на 5
Product.objects.update(stock=F('stock') - 5)
```

#### 🔹 F в аннотациях:

```python
# Пользователи с разницей между входами и ошибками
User.objects.annotate(
    diff=F('login_count') - F('error_count')
)
```

---

## 🆚 `Q` vs `F` — в чём разница?

|                | `Q`                                   | `F`                                  |
| -------------- |---------------------------------------|--------------------------------------|
| Назначение     | Логические выражения                  | Сравнение полей в одной строке       |
| Пример         | `Q(age__lt=18) \| Q(is_active=False)` | `F('stock') < F('ordered')`          |
| Аналог в SQL   | WHERE + логика                        | `WHERE field1 < field2`              |


