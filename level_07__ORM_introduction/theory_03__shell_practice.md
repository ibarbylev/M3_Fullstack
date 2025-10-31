# Работа в БД

## Добавление записи в модель Django (способ 1)


```python
product = MyappModel(code="example_1", value="example volume 1")
product.save()
```

### Объяснение:

* `MyappModel(...)` — создаёт **экземпляр модели**, но **ещё не сохраняет его в базу данных**.
* `product.save()` — сохраняет объект в базу данных, выполнив SQL-запрос `INSERT`.

Этот подход — **стандартный способ** добавления записей в Django.

---

## Альтернатива: сокращённая форма (способ 2)

Если вы хотите сразу создать и сохранить объект, можно использовать:

```python
MyappModel.objects.create(code="example_2", value="example volume 2")
```

Это то же самое, только за один шаг:   
создаёт объект и вызывает `save()` автоматически.

---

Обе формы корректны. Используйте ту, которая подходит под ваш случай:

* Если нужно что-то сделать **до сохранения** (например, изменить поля, вызвать методы) —   
  используйте `product = MyappModel(...)`, затем `product.save()`.
* Если просто нужно **создать и сохранить** — можно `MyappModel.objects.create(...)`.

## Что такое `objects`?

В Django `objects` — это **менеджер модели** (специальный объект),  
через который выполняются запросы к БД:  
 - создание, 
 - поиск, 
 - фильтрация, 
 - удаление 

---


В нашем случае, `MyappModel.objects` — это **менеджер**, через который можно:

#### 🔸 Получить все записи:

```python
MyappModel.objects.all()
```

#### 🔸 Найти запись по условию:

```python
MyappModel.objects.filter(code="default")
MyappModel.objects.get(id=1)
```

#### 🔸 Создать и сохранить запись:

```python
MyappModel.objects.create(code="example_3", value="example volume 3")
```

#### 🔸 Найти нужную запись и изменить:

```python
product = MyappModel.objects.get(id=3)
product.value += "ONLY FOR ME"
product.save()
```


#### 🔸 Удалить:

```python
product = MyappModel.objects.get(id=3)
product.delete()
```

---

### Что такое менеджер (objects) "под капотом:?

Django по умолчанию добавляет менеджер `objects` в каждую модель:

```python
objects = models.Manager()
```

Таким образом, Django позволяет создать свой менеджер с кастомными методами (если нужно).

---

### Итого:

* `MyappModel.objects` — это способ **взаимодействовать с таблицей `MyappModel`** в базе данных.
* Через него вы делаете **запросы**, **создаёте**, **обновляете** и **удаляете** записи.

