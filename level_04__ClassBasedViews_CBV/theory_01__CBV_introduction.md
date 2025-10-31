
## 🌲 **Общая иерархия CBV в Django**

```
object
└── View  (django.views.View)
     ├── TemplateView
     ├── RedirectView
     ├── DetailView     ← Display
     ├── ListView       ← Display
     ├── FormView       ← Form-only (не связан с моделью)
     ├── CreateView     ← Editing
     ├── UpdateView     ← Editing
     └── DeleteView     ← Editing
```

---

### 🔹 **Базовый уровень**

| Класс  | Назначение                                                                                     |
| ------ | ---------------------------------------------------------------------------------------------- |
| `View` | Абстрактный базовый класс для всех CBV. Обрабатывает `.dispatch()`, `.get()`, `.post()` и т.п. |

---

### 🔸 **Представления, работающие с шаблонами (Template Views)**

| Класс          | Родитель | Назначение                    |
| -------------- | -------- | ----------------------------- |
| `TemplateView` | `View`   | Просто отображает HTML-шаблон |
| `RedirectView` | `View`   | Перенаправляет на другой URL  |

---

### 📋 **Generic Views для работы с объектами**

| Класс        | Родители                                               | Назначение                 |
| ------------ | ------------------------------------------------------ | -------------------------- |
| `DetailView` | `SingleObjectMixin`, `TemplateResponseMixin`, `View`   | Отображает один объект     |
| `ListView`   | `MultipleObjectMixin`, `TemplateResponseMixin`, `View` | Отображает список объектов |

---

### 📝 **Generic Views для работы с формами (без модели)**

| Класс      | Родители                                     | Назначение                            |
| ---------- | -------------------------------------------- | ------------------------------------- |
| `FormView` | `FormMixin`, `TemplateResponseMixin`, `View` | Обрабатывает обычные формы без модели |

> Используется, когда нужно отобразить и обработать форму, не связанную с моделью. Например: форма обратной связи, подписка на рассылку и т.п.

---

### ✏️ **Generic Editing Views (формы)**

| Класс        | Родители                                           | Назначение             |
| ------------ | -------------------------------------------------- | ---------------------- |
| `CreateView` | `ModelFormMixin`, `ProcessFormView`                | Создание объекта       |
| `UpdateView` | `ModelFormMixin`, `ProcessFormView`                | Редактирование объекта |
| `DeleteView` | `DeleteViewMixin`, `TemplateResponseMixin`, `View` | Удаление объекта       |

---

### 🔧 **Смешанные классы (Mixins)**

Эти классы используются как строительные блоки внутри CBV:

| Mixin                   | Назначение                                                    |
| ----------------------- | ------------------------------------------------------------- |
| `TemplateResponseMixin` | Добавляет `render_to_response()`                              |
| `ContextMixin`          | Добавляет `get_context_data()`                                |
| `SingleObjectMixin`     | Работает с одним объектом (по `pk` или `slug`)                |
| `MultipleObjectMixin`   | Работает с queryset                                           |
| `ModelFormMixin`        | Работает с формой модели (`form_class`, `form_valid`, и т.д.) |
| `ProcessFormView`       | Обработка POST/GET для формы                                  |

---



