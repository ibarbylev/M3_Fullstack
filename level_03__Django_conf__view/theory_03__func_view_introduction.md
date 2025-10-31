## 🔹 Что такое view в Django?

**View** (представление) — это функция или класс, который получает **запрос (HttpRequest)** и возвращает **ответ (HttpResponse)**.  
Это ядро логики обработки запросов.

Здесь мы рассмотрим только view на основе функций.

---

## 🔹 1. `HttpRequest` — объект запроса

Передаётся первым аргументом (`request`) в каждую view-функцию:

```
def my_view(request):
    print(request.method)        # 'GET', 'POST', и т.д.
    print(request.GET.get('q'))  # параметры из URL
    print(request.POST)          # данные из формы
```

`request` невероятно ёмкий объект, который (в частности) содержит:

| Свойство         | Назначение                         |
|------------------|------------------------------------|
| `request.method` | Метод запроса (`GET`, `POST`, ...) |
| `request.GET`    | Параметры строки запроса (`?q=...`) |
| `request.POST`   | Данные POST                        |
| `request.FILES`  | Загруженные файлы                  |
| `request.user`   | Авторизованный пользователь        |
| `request.path`   | Путь (`/blog/5/`)                  |
| и т.д.           | и т.п.                             |

---

## 🔹 2. `HttpResponse` — базовый ответ

Простой текстовый ответ:

```
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Привет, мир!")
```

Можно задать код и заголовки:

```
HttpResponse("Not found", status=404, content_type="text/plain")
```

---

## 🔹 3. `JsonResponse` — JSON-ответ

Удобно использовать для API:

```
from django.http import JsonResponse

def api_data(request):
    data = {"name": "Django", "version": 4}
    return JsonResponse(data)
```

По умолчанию сериализует словарь в JSON и устанавливает `Content-Type: application/json`.

---

## 🔹 4. `render()` — HTML-ответ с шаблоном

Наиболее часто используемый способ возвращать HTML:

```
from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html', {'title': 'Главная'})
```

* Подгружает шаблон `home.html`
* Передаёт в него данные (`{'title': ...}`)
* Возвращает `HttpResponse` с готовым HTML

---

## 🔹 5. `redirect()` — перенаправление

Перенаправляет пользователя на другой URL (обычно после POST):

```
from django.shortcuts import redirect

def submit_form(request):
    # логика обработки формы
    return redirect('home')  # по имени маршрута
```

Можно передать:

* имя маршрута (`redirect('home')`)
* URL (`redirect('/thanks/')`)
* объект модели (перейдёт на `get_absolute_url()`)

---

## 🔹 Краткая шпаргалка

| Функция / Класс | Назначение                      |
| --------------- | ------------------------------- |
| `HttpRequest`   | Информация о входящем запросе   |
| `HttpResponse`  | Ответ с произвольным содержимым |
| `JsonResponse`  | Ответ в формате JSON            |
| `render()`      | Ответ с HTML-шаблоном           |
| `redirect()`    | Перенаправление на другой адрес |


