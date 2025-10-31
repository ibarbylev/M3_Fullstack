Метаклассы позволяют добавлять/изменить свойства атрибутов и методов класса  
самым невероятным и фантастическим способом.  

Однако поля, описанные в моделях, становятся атрибутами экземпляров класса   
благодаря **дескрипторам**, а не метаклассам.

Точнее, добавляет поля метод `__init__` базового класса.  
А дескрипторы управляют свойствами этих полей.

## Что такое Дескриптор?

**Дескриптор (descriptor)** - это объект, определяющий и контролирующий  
значение (свойства, поведение) атрибутов экземпляра класса.   
Дескриптор определяет методы, которые вызываются в момент доступа к атрибуту  
класса. Эти методы могут быть вызваны:  
 - при попытке узнать значение атрибута (метод `__get__`);
 - при попытке присвоить атрибуту новое значение (метод `__set__`);
 - или при попытке удаления атрибута (метод `__delete__`).

Иными словами, дескрипторы - это некие объекты, определяющие поведение  
атрибутов класса при вызове методов `__get__`, `__set__` или `__delete__`.

Дескриптор, где используются ТОЛЬКО методы `__get__`, называется **non-data descriptor**.   
А тот, где наоборот, используются только методы `__set__` и/или `__delete__`,  
называется **data descriptor**.

### Пример
*Реализовать конструкцию, которая превращает атрибуты класса в атрибуты экземпляра*
*(Как в моделях Django)*

```python

class MyField:
    def __init__(self, *, default=None):
        self.default = default
        self.name = None  # имя будет назначено позже

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class BaseModel:
    def __init__(self, **kwargs):
        # добавляем все переданные поля, как атрибуты экземпляра класса
        for key, value in kwargs.items():
            setattr(self, key, value)


class Person(BaseModel):
    name = MyField(default="Unknown")
    age = MyField(default=0)


p = Person(name="Peter", age=25)
print(p.name)  # Peter
print(p.age)   # 25
```

---


### 1. **`MyField` — дескриптор-поле**

```python
class MyField:
    def __init__(self, *, default=None):
        self.default = default
        self.name = None  # имя будет установлено в __set_name__
```

* Имитирует поведение `CharField`, `IntegerField` и др. в Django.
* Сохраняет значение по умолчанию (`default`), если ничего не передано.

### 2. **`__set_name__`** — автоматическое имя поля

```python
def __set_name__(self, owner, name):
    self.name = '_' + name
```

* Устанавливает имя, под которым поле будет храниться в `instance.__dict__`.
* Добавляет подчёркивание, чтобы избежать конфликта с самим дескриптором.
  (иначе возможна рекурсивная ссылка:  
  `instance.__dict__.get` в методе `__get__` снова вызывает метод `__get__`)


### 3. **`__get__` и `__set__` — доступ к значению**

```python
def __get__(self, instance, owner):
    if instance is None:
        return self
    return instance.__dict__.get(self.name, self.default)

def __set__(self, instance, value):
    instance.__dict__[self.name] = value
```

* `__get__`: возвращает значение поля или `default`, если оно ещё не установлено.
* `__set__`: сохраняет значение в экземпляре.

---

### 4. **`BaseModel` — универсальный конструктор**

```python
class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
```

* Получает любые именованные аргументы (`**kwargs`).
* Передаёт их через `setattr()` → это вызывает `__set__` у соответствующего поля-дескриптора.

---

### 5. **`Person` — класс модели**

```python
class Person(BaseModel):
    name = MyField(default="Unknown")
    age = MyField(default=0)
```

* Пользовательский класс, **без `__init__`**.
* Поля — это экземпляры дескрипторов `MyField`.
* Наследуется от `BaseModel`, чтобы поддерживать передачу значений при создании экземпляра.

---

Это упрощённая версия, которая не сравнивает имена дескрипторов с именами,  
использованными при создании класса `Person(name="Peter", age=25)`

Ниже - улучшенный вариант базового класса, лишённый указанного недостатка:
```python
class BaseModel:
    def __init__(self, **kwargs):
        # Определяем только те поля, которые существуют как дескрипторы
        allowed_fields = {
            key for key, value in self.__class__.__dict__.items()
            if isinstance(value, MyField)
        }

        for key, value in kwargs.items():
            if key not in allowed_fields:
                raise TypeError(f"Unexpected field: {key}")
            setattr(self, key, value)
```

Таким образом, будут приняты только те поля, которые описаны в дескрипторе `MyField`.


## 📌 Вывод

| Компонент             | Назначение                                                                 |
| --------------------- | -------------------------------------------------------------------------- |
| `MyField`             | Поле-дескриптор с поддержкой `default`                                     |
| `__set_name__`        | Автоматически узнаёт имя атрибута                                          |
| `__get__` / `__set__` | Управляют доступом к значению экземпляра                                   |
| `BaseModel.__init__`  | Универсально инициализирует поля через `**kwargs`                          |
| `Person`              | Класс модели, как в Django: без явного `__init__`, с дескрипторными полями |


В этом упрощённом примере дескрипторы не проверяют значения атрибутов. 
Хотя могут это делать значительно эффективнее традиционных способов (см. следующие 4 файла)
---

