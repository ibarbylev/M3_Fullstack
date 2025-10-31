Главное, что может делать QuerySet, - это извлекать,
(а затем структуировать извлечённые данные)   
всеми мыслимыми и немыслимыми способами.

Таки образом, "извлечение" в QuerySet понимается **в широком смысле**:   
 - не только получить строки из таблицы,
 - но и настроить **формат, условия, агрегаты и оптимизации**.

---

### 🔍 Такое структурирование помогает понимать:

1. **Что именно ты извлекаешь** — объекты модели, значения полей, агрегаты.
2. **Как** ты их извлекаешь — с условиями, сортировкой, аннотациями.
3. **Какие есть надстройки** — оптимизация JOIN'ов, агрегации, подсчёты.

---

## 📂 Категории методов извлечения данных:

| Категория                 | Что делает                           | Примеры                                   |
| ------------------------- | ------------------------------------ | ----------------------------------------- |
| **Фильтрация и выборка**  | Выбирает строки из таблицы           | `filter()`, `get()`, `exclude()`, `all()` |
| **Формат результата**     | Меняет формат данных                 | `values()`, `values_list()`, `raw()`      |
| **Агрегация и аннотация** | Считает и добавляет вычисляемые поля | `aggregate()`, `annotate()`, `count()`    |
| **Оптимизация запросов**  | Уменьшает число SQL-запросов         | `select_related()`, `prefetch_related()`  |

---
| **Категория**                | **Метод**            | **Описание**                                | **Возвращает**      | **Пример**                                         |
| ---------------------------- | -------------------- | ------------------------------------------- | ------------------- | -------------------------------------------------- |
| **1. Фильтрация и выборка**  | `all()`              | Все записи                                  | `QuerySet`          | `User.objects.all()`                               |
|                              | `filter()`           | Фильтрация по условию                       | `QuerySet`          | `User.objects.filter(age__gte=18)`                 |
|                              | `exclude()`          | Противоположное `filter()`                  | `QuerySet`          | `User.objects.exclude(is_active=True)`             |
|                              | `get()`              | Один объект (или ошибка)                    | `Model instance`    | `User.objects.get(pk=1)`                           |
|                              | `first()`            | Первый объект (или `None`)                  | `Model` или `None`  | `User.objects.first()`                             |
|                              | `last()`             | Последний объект (или `None`)               | `Model` или `None`  | `User.objects.last()`                              |
|                              | `exists()`           | Есть ли хотя бы один объект                 | `bool`              | `User.objects.filter(...).exists()`                |
|                              | `order_by()`         | Сортировка по полю                          | `QuerySet`          | `User.objects.order_by('-date_joined')`            |
|                              | `distinct()`         | Только уникальные строки                    | `QuerySet`          | `User.objects.values('email').distinct()`          |
| **2. Формат результата**     | `values()`           | Получить словари с нужными полями           | `QuerySet of dict`  | `User.objects.values('id', 'username')`            |
|                              | `values_list()`      | Получить кортежи с нужными полями           | `QuerySet of tuple` | `User.objects.values_list('username', flat=True)`  |
|                              | `only()`             | Загрузка только указанных полей             | `QuerySet`          | `User.objects.only('username')`                    |
|                              | `defer()`            | Отложенная загрузка указанных полей         | `QuerySet`          | `User.objects.defer('password')`                   |
|                              | `raw()`              | Сырой SQL-запрос                            | `RawQuerySet`       | `User.objects.raw('SELECT * FROM auth_user')`      |
| **3. Агрегация и аннотация** | `aggregate()`        | Вычисление общего значения (сумма, среднее) | `dict`              | `User.objects.aggregate(Avg('age'))`               |
|                              | `annotate()`         | Добавление вычисленного поля к каждому      | `QuerySet`          | `User.objects.annotate(post_count=Count('posts'))` |
|                              | `count()`            | Количество объектов                         | `int`               | `User.objects.count()`                             |
| **4. Оптимизация запросов**  | `select_related()`   | JOIN по ForeignKey                          | `QuerySet`          | `Post.objects.select_related('author')`            |
|                              | `prefetch_related()` | JOIN по M2M или обратным FK                 | `QuerySet`          | `Author.objects.prefetch_related('books')`         |
