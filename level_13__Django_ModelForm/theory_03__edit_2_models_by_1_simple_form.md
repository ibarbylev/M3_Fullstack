## Редактирование 2-х моделей (Book + BookDetail) через обычную форму

### Форма для BookDetail

```python
from django import forms
from .models import BookDetail

class BookDetailForm(forms.ModelForm):
    class Meta:
        model = BookDetail
        fields = ['summary', 'page_count']
        widgets = {
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control'})
        }
```

### View для редактирования Book и его BookDetail

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm, BookDetailForm

def edit_book_with_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Если детали ещё нет, создаём объект (но не сохраняем)
    book_detail = getattr(book, 'detail', None)
    
    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        detail_form = BookDetailForm(request.POST, instance=book_detail)
        if book_form.is_valid() and detail_form.is_valid():
            book_form.save()
            # Для нового BookDetail, если его нет
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
```

### **Шаблон `edit_book_with_detail.html`**

```html
<form method="post">
    {% csrf_token %}
    <h3>Book</h3>
    {{ book_form.as_p }}
    <h3>Details</h3>
    {{ detail_form.as_p }}
    <button type="submit" class="btn btn-primary">Сохранить</button>
</form>
```

Такой подход удобен, если нужно работать с двумя формами на одной странице.

---

## 2 Вариант с GenericView (`UpdateView`)

Django GenericView умеет работать с одной моделью, поэтому для BookDetail потребуется **создать отдельный UpdateView**, либо использовать кастомный `get_context_data` для отображения дополнительной формы.

Простейший вариант — **только Book**:

```python
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Book
from .forms import BookForm

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book.html'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
```

Если хотим **Book + BookDetail вместе**, то делаем так:

```python
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

Этот вариант объединяет `GenericView` с дополнительной формой для `BookDetail`.

* Можно редактировать одновременно `Book` и `BookDetail`.
* Все правила валидации сохраняются.

---

Если хотите, я могу сделать **готовый пример с `urls.py` и полностью рабочими шаблонами для обоих вариантов**, чтобы можно было сразу вставлять в проект.

Хотите, чтобы я это сделал?
