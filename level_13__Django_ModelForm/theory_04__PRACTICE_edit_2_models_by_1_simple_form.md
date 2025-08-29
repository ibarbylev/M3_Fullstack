## 1 Вариант с обычной функцией**

### `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/edit/', views.edit_book_with_detail, name='edit_book_with_detail'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),  # страница просмотра книги
]
```

---

### `views.py`

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm, BookDetailForm

def edit_book_with_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_detail = getattr(book, 'detail', None)

    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        detail_form = BookDetailForm(request.POST, instance=book_detail)
        if book_form.is_valid() and detail_form.is_valid():
            book_form.save()
            detail = detail_form.save(commit=False)
            detail.book = book
            detail.save()
            return redirect('book_detail', pk=book.pk)
    else:
        book_form = BookForm(instance=book)
        detail_form = BookDetailForm(instance=book_detail)

    context = {
        'book_form': book_form,
        'detail_form': detail_form
    }
    return render(request, 'books/edit_book_with_detail.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})
```

---

### Шаблон `edit_book_with_detail.html`

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Редактировать книгу</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
</head>
<body>
<div class="container mt-5">
    <h2>Редактировать книгу</h2>
    <form method="post">
        {% csrf_token %}
        <h3>Book</h3>
        {{ book_form.as_p }}
        <h3>Details</h3>
        {{ detail_form.as_p }}
        <button type="submit" class="btn btn-primary">Сохранить</button>
    </form>
</div>
</body>
</html>
```

---

### Шаблон `book_detail.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ book.title }}</title>
</head>
<body>
<h1>{{ book.title }}</h1>
<p>Author: {{ book.author }}</p>

{% if book.detail %}
    <p>Summary: {{ book.detail.summary }}</p>
    <p>Pages: {{ book.detail.page_count }}</p>
{% else %}
    <p>Нет деталей</p>
{% endif %}

<a href="{% url 'edit_book_with_detail' book.pk %}">Редактировать</a>
</body>
</html>
```

---

## 2 Вариант с GenericView (`UpdateView`)

### `urls.py`

```python
from django.urls import path
from .views import BookWithDetailUpdateView

urlpatterns = [
    path('book/<int:pk>/edit/', BookWithDetailUpdateView.as_view(), name='edit_book_with_detail'),
    path('book/<int:pk>/', BookWithDetailUpdateView.as_view(template_name='books/book_detail.html'), name='book_detail'),
]
```

---

### `views.py`

```python
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import redirect
from .models import Book
from .forms import BookForm, BookDetailForm

class BookWithDetailUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book_with_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_detail = getattr(self.object, 'detail', None)
        if self.request.POST:
            context['detail_form'] = BookDetailForm(self.request.POST, instance=book_detail)
        else:
            context['detail_form'] = BookDetailForm(instance=book_detail)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book_form = self.get_form()
        book_detail_form = BookDetailForm(request.POST, instance=getattr(self.object, 'detail', None))

        if book_form.is_valid() and book_detail_form.is_valid():
            book_form.save()
            detail = book_detail_form.save(commit=False)
            detail.book = self.object
            detail.save()
            return redirect('book_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = book_form
        context['detail_form'] = book_detail_form
        return self.render_to_response(context)
```

---

### Шаблон для `UpdateView` — `edit_book_with_detail.html`

Можно подходит и для функции**, потому что структура контекста одинаковая.

---

### Шаблон `book_detail.html` для GenericView

```html
<h1>{{ object.title }}</h1>
<p>Author: {{ object.author }}</p>

{% if object.detail %}
    <p>Summary: {{ object.detail.summary }}</p>
    <p>Pages: {{ object.detail.page_count }}</p>
{% else %}
    <p>Нет деталей</p>
{% endif %}

<a href="{% url 'edit_book_with_detail' object.pk %}">Редактировать</a>
```

