## Зачем нужны агрегации и аннотации?

В Django агрегации и аннотации нужны для эффективной обработки данных ИМЕННО на уровне БД, а не в Python.  
Это особенно важно при работе с большим объёмом данных.


| Тип           | Описание                                                                                                      |
| ------------- |---------------------------------------------------------------------------------------------------------------|
| **Агрегация** | `.aggregate()` - позволяет получить обобщённую информацию по QuerySet (`SUM`, `AVG`, `COUNT`, `MAX`, `MIN`)   |
| **Аннотация** | `.annotate()` - позволяет добавить вычисляемые (в том числа агрегированные) поля к каждому объекту в QuerySet |

**Примеры задач:**

* Посчитать общее количество заказов — `.aggregate(Count("id"))`
* Подсчитать сумму всех покупок пользователя — `.annotate(total=Sum("orders__amount"))`

---

## 🔹 Почему это лучше делать через SQL (а не в Python)?

### 📌 Пример: Сравнение производительности

Допустим, у нас есть модель заказов и модель пользователей, делающих эти заказы:

```python
class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
```

Попробуем просуммировать стоимость всех заказов двумя способам:
- извлечь сумму каждого заказа и просуммировать в Python;
- найти общую сумму на уровне SQL и передать готовый результат в Python

### ❌ Вариант на Python:

```python
total = sum(order.amount for order in Order.objects.filter(user=user))
```

Этот код:

* Загружает **все заказы пользователя** в память (могут быть тысячи).
* Делает много SQL-запросов или один тяжёлый с передачей всех данных в Python.
* Плохо масштабируется.

### ✅ Вариант на уровне SQL (агрегация):

```python
from django.db.models import Sum

total = Order.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"]
```

Этот код:

* Генерирует один SQL-запрос с `SUM(amount)`.
* Быстро обрабатывается СУБД (использует индексы, если есть).
* Возвращает только одно число, без лишней передачи данных.

---

## SQL против Python

Предположим:

* 1 пользователь имеет 100 000 заказов.
* Каждая строка `amount` занимает 100 байт в передаче.
* Вариант на Python передаёт 100 000 × 100 байт = **\~10 MB** данных в память интерпретатора.
* SQL-агрегация возвращает **одно число** (несколько байт).

**Вывод**:

* Агрегации в SQL снижают нагрузку на память и сеть.
* Они **значительно быстрее**.
* Они масштабируемы и позволяют базе данных выполнять оптимизацию.

---

## 🔹 Пример с аннотацией

Посчитаем сумму заказов по каждому пользователю:

```python
from django.db.models import Sum

User.objects.annotate(total_spent=Sum("order__amount"))
```

Аналог в Python:

```python
for user in User.objects.all():
    user.total_amount_by_user = sum(order.amount for order in user.order_set.all())
```

⚠ Это приведёт к **N+1 проблеме**:  
1 запрос на пользователей и **N** отдельных запросов на заказы для каждого пользователя. 

✅ С аннотацией будет ТОЛЬКО один SQL-запрос с `GROUP BY`.

```python
from django.db.models import Sum

# добавить каждому пользователю поле total_amount_by_user, равное сумме всех заказов пользователя
User.objects.annotate(total_amount_by_user=Sum("order__amount"))
```

```sql
SELECT 
    auth_user.id, 
    auth_user.username, 
    auth_user.email,
    SUM(app_order.amount) AS total_amount_by_user
FROM auth_user
LEFT OUTER JOIN app_order ON app_order.user_id = auth_user.id
GROUP BY auth_user.id, auth_user.username, auth_user.email;
```
### Почему группировка идёт по трём полям, а не по одному полю `user.id`?

Причина: совместимость с SQL стандартом (и MySQL `ONLY_FULL_GROUP_BY`)

Этот режим требует, чтобы все поля в SELECT, которые не являются агрегатными функциями,  
обязательно были включены в GROUP BY.

### Как оставить группировку только по `user.id`?

Можно использовать .values("id"):

```python
User.objects.values("id").annotate(total=Sum("order__amount"))
```
В этом случае Django не будет добавлять поля:

```sql
SELECT 
    auth_user.id, SUM(app_order.amount) AS total_amount_by_user
FROM auth_user
LEFT OUTER JOIN app_order ON app_order.user_id = auth_user.id
GROUP BY auth_user.id;
```
---

## 💡 Вывод

> **Агрегации и аннотации в Django нужны, чтобы использовать силу SQL:**
>
> * меньше данных передаётся в Python
> * меньше запросов к базе
> * выше скорость обработки
> * меньше нагрузка на память и сеть
> * лучше масштабируемость проекта

