# Для чего нужна аннотация?

---

## 1. **Агрегация данных внутри QuerySet**

Аннотация часто используется, чтобы вычислять значения прямо в запросе, а не в Python.

### Пример 1.1: Подсчёт связанных объектов

```python
from django.db.models import Count
from books.models import Author

authors = Author.objects.annotate(book_count=Count('book'))
for author in authors:
    print(author.name, author.book_count)
```

**Что делает:**

* `Count('book')` считает, сколько книг связано с автором.
* Результат добавляется в объект `Author` как новое поле `book_count`.

**Цель:**
Избежать дополнительного запроса и сразу получить вычисленные данные.

---

### Пример 1.2: Добавление полей: среднее, сумма, макс/мин

```python
from django.db.models import Avg, Sum, Max

customers = Customer.objects.annotate(
    avg_price=Avg('order__total'),
    total_spent=Sum('order__total'),
    last_order_date=Max('order__created_at')
)
```

**Цель:**
Сразу получить агрегированные данные по каждому объекту.

---

## 2. **Создание вычисляемых полей**

Можно делать математические и логические вычисления прямо в SQL.

### Пример 2.1: Разница цен

```python
from django.db.models import F, ExpressionWrapper, DecimalField

products = Product.objects.annotate(
    discount_amount=ExpressionWrapper(
        F('price') - F('discount_price'),
        output_field=DecimalField()
    )
)
```

**Цель:**
Добавить в результат новое поле, которое не хранится в БД с типом данных DecimalField()

---

### Пример 2.2: Логическое условие через `Case` и `When`

```python
from django.db.models import Case, When, Value, CharField

products = Product.objects.annotate(
    price_category=Case(
        When(price__lt=100, then=Value('cheap')),
        When(price__lt=500, then=Value('medium')),
        default=Value('expensive'),
        output_field=CharField()
    )
)
```

**Цель:**
Классифицировать объекты прямо в запросе.

---

## 3. **Фильтрация агрегатов**

Иногда нужно агрегировать только по части данных.

### Пример 3.1: Подсчёт только опубликованных книг

```python
authors = Author.objects.annotate(
    published_books=Count('book', filter=Q(book__is_published=True))
)
```

**Цель:**
Считать или суммировать только те строки, что удовлетворяют условию.

---

### Пример 3.2: Сумма заказов за последний месяц

```python
from django.utils import timezone
from datetime import timedelta

one_month_ago = timezone.now() - timedelta(days=30)

customers = Customer.objects.annotate(
    recent_spent=Sum('order__total', filter=Q(order__created_at__gte=one_month_ago))
)
```

**Цель:**
Частичная агрегация с условием.  
(Для каждого клиента в QuerySet customers создаётся дополнительное поле recent_spent,   
с суммой всех его заказов за последние 30 дней.   
Если заказов не было, то значение будет None.)

---

## 4. **Работа с датами и временем**

Django ORM умеет извлекать части даты прямо в SQL.

### Пример 4.1: Группировка по месяцу

```python
from django.db.models.functions import TruncMonth
from sales.models import Order

orders_by_month = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(
    total=Sum('total')
)
```

**Цель:**
Сгруппировать и агрегировать по временным периодам.
Будет получен QuerySet словарей
```python
{
    'month': datetime.date(2025, 8, 1),  # первый день месяца
    'total': 12345.67                   # сумма всех заказов за этот месяц
}
```
где 
* month — начало месяца, 
* total — сумма всех заказов за этот месяц.

---

### Пример 4.2: День недели

```python
from django.db.models.functions import ExtractWeekDay

sales = Order.objects.annotate(weekday=ExtractWeekDay('created_at'))
```

**Цель:**
Добавить вычисляемое поле с номером дня недели.
(Каждый заказ получит новое поле дня недели)
---

## 5. **Оптимизация запросов**

Аннотация может заменить дополнительные запросы или Python-цикл.

### Пример 5.1: Минимизировать N+1 запрос

Вместо:

```python
for author in Author.objects.all():
    author.book_count = author.book_set.count()
```

Мы делаем:

```python
Author.objects.annotate(book_count=Count('book'))
```

**Результат:**
Один SQL-запрос вместо множества.

---

## 🗂 Итоговая таблица по целям аннотации

| Цель применения      | Инструменты                        | Пример                 |
| -------------------- | ---------------------------------- | ---------------------- |
| Агрегация            | `Count`, `Sum`, `Avg`, `Max`       | Подсчёт книг автора    |
| Вычисляемые поля     | `F`, `ExpressionWrapper`           | Разница цен            |
| Условная логика      | `Case`, `When`, `Value`            | Категория цены         |
| Частичная агрегация  | `filter=` внутри агрегатов         | Подсчёт опубликованных |
| Работа с датами      | `TruncMonth`, `ExtractWeekDay`     | Продажи по месяцам     |
| Оптимизация запросов | Любые аннотации + `select_related` | Убираем N+1 запросы    |


