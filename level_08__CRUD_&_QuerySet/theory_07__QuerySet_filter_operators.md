
### 🔍 **Основные операторы фильтрации Django ORM**

| Оператор                                   | Назначение                       | Пример использования              | SQL-аналог                |
| ------------------------------------------ | -------------------------------- | --------------------------------- | ------------------------- |
| `exact`                                    | Точное совпадение                | `filter(age__exact=30)`           | `= 30`                    |
| `iexact`                                   | Нечувствительно к регистру       | `filter(name__iexact="john")`     | `ILIKE 'john'`            |
| `contains`                                 | Подстрока                        | `filter(name__contains="oh")`     | `LIKE '%oh%'`             |
| `icontains`                                | Подстрока без учёта регистра     | `filter(name__icontains="oh")`    | `ILIKE '%oh%'`            |
| `in`                                       | Вхождение в список значений      | `filter(id__in=[1,2,3])`          | `IN (1,2,3)`              |
| `gt`                                       | Больше                           | `filter(age__gt=18)`              | `> 18`                    |
| `gte`                                      | Больше или равно                 | `filter(age__gte=18)`             | `>= 18`                   |
| `lt`                                       | Меньше                           | `filter(age__lt=65)`              | `< 65`                    |
| `lte`                                      | Меньше или равно                 | `filter(age__lte=65)`             | `<= 65`                   |
| `startswith`                               | Начинается с                     | `filter(name__startswith="Jo")`   | `LIKE 'Jo%'`              |
| `istartswith`                              | Начинается с, без учёта регистра | `filter(name__istartswith="jo")`  | `ILIKE 'jo%'`             |
| `endswith`                                 | Заканчивается на                 | `filter(name__endswith="n")`      | `LIKE '%n'`               |
| `iendswith`                                | Заканчивается на, без регистра   | `filter(name__iendswith="n")`     | `ILIKE '%n'`              |
| `range`                                    | Диапазон                         | `filter(age__range=(18,30))`      | `BETWEEN 18 AND 30`       |
| `isnull`                                   | Проверка на NULL                 | `filter(last_login__isnull=True)` | `IS NULL`                 |
| `regex`                                    | Регулярное выражение             | `filter(name__regex=r'^[A-Z]')`   | `REGEXP '^[A-Z]'`         |
| `iregex`                                   | Регулярка без учёта регистра     | `filter(name__iregex=r'^[a-z]')`  | `REGEXP '^[a-z]'`         |
| `date`, `year`, `month`, `day`, `week_day` | Фильтрация по частям даты        | `filter(birth_date__year=1990)`   | `YEAR(birth_date) = 1990` |

---

### ✅ Примеры

```python
# Все пользователи старше 18
User.objects.filter(age__gt=18)

# Пользователи с именем, содержащим 'admin' (без учёта регистра)
User.objects.filter(username__icontains='admin')

# Пользователи, зарегистрированные в 2024 году
User.objects.filter(date_joined__year=2024)

# Пользователи без аватара
User.objects.filter(avatar__isnull=True)
```

Оператор `_exact` выглядит как избыточный, поскольку оба нижеследующих варианта

```sql
Book.objects.filter(author="Джейн Остин")
Book.objects.filter(author_exact="Джейн Остин")
```

дают один и тот же вариант SQL-запроса:

```sql
SELECT * FROM book WHERE author = 'Джейн Остин';
```

Но `_exact` может оказаться крайне нужным для унификации запросов в цикле.   
Например: 
```python
field_name = "author"
lookup = "exact"
value = "Джейн Остин"

filter_key = f"{field_name}__{lookup}"  # => 'author__exact'

queryset = Book.objects.filter(**{filter_key: value})
```