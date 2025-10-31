В Django, помимо уже готовых фильтров, можно создавать свои собственные.

Порядок действий:
- 1 В выбранном предложении создаём папку для фильтров `templatetags`
- 2 В этой папке создаём py-файл (например, `custom_filters.py`)
- 3 Далее созданные фильтры необходимо импортировать в шаблон: `{% load custom_filters %}`

# Фильтр без параметров

Для примера создадим фильтр `currency_format`, который форматирует числа, добавляя
 - разделители тысяч (пробел)
 - для десятичных знака в конце
---

## 🔧 1. Создаём файл для пользовательских фильтров

**Структура:**

```
shop/
├── templatetags/
│   └── custom_filters.py
```


---

## 🧪 2. Создаём и регистрируем фильтр `currency_format`

**`custom_filters.py`:**

```python
from django import template

register = template.Library()


@register.filter(name='currency_format')
def currency_format(value):
    """
    Преобразует число в формат "# ###,00".
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        # Если value не число - возвращаем пустую строку
        return ''

    # Форматируем: разделитель тысяч — пробел, разделитель дроби — запятая
    # f-string с параметром ,.2f форматирует 123456.789 как 123,456.79
    # далее меняем
    # ',' -> 'X'
    # '.' -> ','
    # 'X' -> ' '
    # 123,456.79 -> 123 456,79
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
    return formatted
```

---

## 📌 3. Использование фильтра в шаблоне

В шаблоне сначала загрузите фильтры:

```django
{% load custom_filters %}

{% with price=987564123.9867 %}
  {{ price|currency_format }}  
{% endwith %}
```

# Фильтр с параметрами

Мы можем передать из шаблона параметры через двоеточие.  

Например, указать тип валюты: (`usd`, `euro` или `rub`):

```django
{% load custom_filters %}

{% with price=987564123.9867 %}
  {{ price|currency_format:usd }}  
{% endwith %}
```

Изменяем функцию.

Теперь, если валюта на указана, выводим знак рублей в конце.
А если указана - знак валюты в начале.

Изменённый вариант фильтра:
```python
from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'usd': '$',
    'euro': '€',
    'rub': '₽',
}

@register.filter(name='currency_format')
def currency_format(value, currency=None):
    """
    Форматирует число в денежный формат с указанием валюты.
    Пример:
        {{ 123456.78|currency_format:"usd" }} → $123 456,78
        {{ 123456.78|currency_format }} → 123 456,78 ₽
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return ''

    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")

    currency = (currency or '').lower()
    symbol = CURRENCY_SYMBOLS.get(currency)

    if symbol:
        return f"{symbol}{formatted}"  # Валюта указана — символ в начале
    else:
        return f"{formatted} ₽"  # По умолчанию — рубль в конце
```

