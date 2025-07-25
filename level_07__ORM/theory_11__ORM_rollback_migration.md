
### Как откатить миграцию

1. Прежде всего надо найти номер нужной миграции:

```bash
python manage.py showmigrations myapp
```

2. Предположим, мы нашли - это вторая миграция в приложении `myapp`:

```bash
python manage.py migrate myapp 0002
```

В данном случае миграция с номером `0003` будет отменена.

---

### Если необходимо откатить ВСЕ миграции приложения:

```bash
python manage.py migrate myapp zero
```

---

### Резюме

* `python manage.py migrate app_name migration_name` — откатить миграции до указанной.
* `python manage.py migrate app_name zero` — откатить все миграции приложения.

---

