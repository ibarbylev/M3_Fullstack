## Декоратор `@pytest.mark.parametrize`

### 1 Основная идея

Декоратор `@pytest.mark.parametrize` позволяет запускать один и тот же тест  
несколько раз с разными входными данными**.  
Это удобно, когда нужно протестировать одну функцию или поведение с множеством вариантов, не дублируя код теста.

---

### 2 Синтаксис

```python
@pytest.mark.parametrize("аргументы", [список_значений])
def test_example(аргументы):
    ...
```

* `"аргументы"` — строка с названием одного или нескольких параметров, через запятую.
* `[список_значений]` — список кортежей или значений, которые будут подставлены в тест.

  * Если параметров несколько, каждый элемент списка — **кортеж** из значений.

---

### 3 Примеры

#### Один параметр

```python
import pytest

@pytest.mark.parametrize("x", [1, 2, 3])
def test_square(x):
    assert x * x >= 0
```

* Тест выполнится 3 раза:

  * `x = 1`
  * `x = 2`
  * `x = 3`

---

#### Несколько параметров

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (4, 5, 9),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

* Тест выполнится 3 раза, каждый раз подставляются свои `a, b, expected`.

---

### 4 Важные особенности

1. **Каждая комбинация — отдельный тест**

   * В отчёте pytest будут отдельные строки для каждой комбинации.

2. **Можно использовать fixtures**

   ```python
   @pytest.mark.parametrize("x", [1,2])
   def test_with_fixture(x, db):
       ...
   ```

   Здесь `db` — обычный fixture, а `x` — параметр.

3. **Списки и тюплы**

   * Если один параметр → можно просто `[1,2,3]`
   * Если несколько параметров → каждый элемент `[ (1,2), (3,4) ]`

---

### 5 Как это применимо к нашим URL

В примере:

```python
@pytest.mark.parametrize("url_name, view_func", [
    ("auth_registration", users_views.RegistrationView),
    ("auth_login", users_views.LoginView),
])
def test_users_urls(url_name, view_func):
    url = reverse(url_name)
    assert resolve(url).func.view_class == view_func
```

* Тест `test_users_urls` будет выполнен **дважды**:

  1. `url_name = "auth_registration"`, `view_func = RegistrationView`
  2. `url_name = "auth_login"`, `view_func = LoginView`
* 
* Таким образом мы проверяем **несколько URL** одним тестом, без копирования кода.



---

#### 5.1. `resolve(url)`

* Функция `django.urls.resolve` принимает URL в виде строки и возвращает объект,  
  который содержит информацию о том, какой view будет вызван для этого URL.
* Пример:

```python
from django.urls import resolve
match = resolve("/auth/login/")
print(match)
```

`match` — объект `ResolverMatch`, у которого есть несколько атрибутов:

| Атрибут    | Описание                                                   |
| ---------- | ---------------------------------------------------------- |
| `func`     | view function, которая будет вызвана                       |
| `args`     | позиционные аргументы, извлечённые из URL                  |
| `kwargs`   | именованные аргументы, извлечённые из URL (например, slug) |
| `url_name` | имя URL (name)                                             |
| `app_name` | имя приложения (если задано)                               |

---

#### 5.2. `resolve(url).func`

* Для **Function-Based View (FBV)** это просто функция, которая обрабатывает запрос.
* Для **Class-Based View (CBV)** это **обёртка**, потому что CBV — это класс,  
  а Django вызывает метод `as_view()`, который возвращает функцию.

---

#### 5.3. `resolve(url).func.view_class`

* Когда используется CBV (`class MyView(View): ...`), в URL мы обычно пишем:

```python
path("auth/login/", LoginView.as_view(), name="auth_login")
```

* `as_view()` возвращает **callable function**, но она хранит ссылку на сам класс через атрибут `.view_class`.
* Поэтому:

```python
resolved_view = resolve("/auth/login/").func
print(resolved_view.view_class)  # LoginView
```

* Это позволяет проверить, что **по URL действительно вызывается нужный CBV**.

---

#### 5.4. Проверка через `assert`

```python
assert resolve(url).func.view_class == view_func
```

* `resolve(url).func.view_class` → класс view, который зарегистрирован для данного URL.
* `view_func` → класс view, который мы ожидаем.
* Если они равны → тест проходит. Если нет → pytest выдаёт ошибку.

---

#### 5.5 FBV vs CBV

* FBV:

```python
assert resolve("/some-url/").func == my_view_function
```

* CBV:

```python
assert resolve("/some-url/").func.view_class == MyClassBasedView
```

То есть для CBV **обязательно использовать `.view_class`**, иначе сравнение будет с обёрнутой функцией, и оно не пройдет.

