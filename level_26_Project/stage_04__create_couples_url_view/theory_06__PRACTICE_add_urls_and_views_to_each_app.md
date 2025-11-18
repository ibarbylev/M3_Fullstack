## Добавляем `urls.py` и `views.py` в каждое приложение

### `adminapp`

`adminapp/urls.py`

```python

```


`adminapp/views.py`

```python

```

### `shop`

`shop/urls.py`

```python

```

`shop/views.py`

```python

```

### `user`


`user/urls.py`

```python

```

Здесь чуть сложнее, так как 2 файла views: `views_auth` и `views_account`.
Поэтому:

1. Создаём пакет (а не папку!) `views`
2. В ней создаём 2 файла `views_auth` и `views_account`
3. Чтобы не изменился импорт, добавляем в `views/__init__.py` 2 импорта:

```python
from . import views_auth
from . import views_account
```

`user/views/views_auth.py`

```python

```

`user/views/views_account.py`

```python

```