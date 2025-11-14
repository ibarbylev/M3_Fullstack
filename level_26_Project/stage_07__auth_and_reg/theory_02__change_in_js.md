
```python
# TODO Просто заменить css и js !!!!!!!!


# TODO Не забыть добавить сюда формы логина и регистрации в html и пояснения для формы Python !!!!!!!!

```
## Добавляем место вставки сообщений

Экономим на формах - пользуемся messages

Добавляем в `base.html` сразу же после `header`, что было видно из всех шаблонов.

```html

{% if messages %}
    {% for message in messages %}
        <div class="alert-success">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

```

## Блок авторизированного пользователя на `base.html`

```html
        {% if request.user.is_authenticated %}
            <!-- Block for authorized user -->
            <div class="header__user-actions" id="auth-user">
                <a href="account.html" class="user-icon" aria-label="My Account" title="Аккаунт">
                    <img src="{% static 'img/icons/User_alt.svg' %}" alt="User Account">
                </a>

                <a href="{% url 'shop_order' %}" class="cart-icon" aria-label="Shopping Cart" title="Корзина">
                    <img src="{% static 'img/icons/Shopping_bag.svg' %}" alt="Shopping Cart">
                </a>

                <form method="post" action="{% url 'auth_logout' %}">
                    {% csrf_token %}
                    <button type="submit" class="logout-icon" title="Выйти">
                        <i class="fa-solid fa-right-from-bracket fa-2x"></i>
                    </button>
                </form>
            </div>
        {% else %}
            <!-- Block for unauthorized user -->
            <div class="header__auth-buttons" id="auth-guest2">
                <a href="{% url 'auth_login' %}" class="button button--secondary">Sign in</a>
                <a href="{% url 'auth_registration' %}" class="button button--primary">Register</a>
            </div>

        {% endif %}
```


## Добавляем формы

`auth/login.html`

```html
    <form class="auth-form" id="login-form" method="post" action="{% url 'auth_login' %}">
        {% csrf_token %}

        {% if form.non_field_errors %}
        <div class="error">
            {% for error in form.non_field_errors %}
                {{ error }}
            {% endfor %}
        </div>
        {% endif %}

        {% for field in form %}
            <div class="InputField">
                {{ field.label_tag }}
                {{ field }}

                {% if field.errors %}
                  {% for error in field.errors %}
                    <div class="error">{{ error }}</div>
                  {% endfor %}
                {% endif %}
            </div>
        {% endfor %}
    </form>
    <div class="ButtonGroup">
        <button type="submit" class="button button--primary">Sign In</button>
    </div>
    
    <div class="TextLink">
        <a href="{% url 'auth_password_reset' %}">Forgot password?</a>
    </div>

```


`auth/register.html`

```html
            <form class="auth-form" id="register-form" method="post" action="{% url 'auth_registration' %}">
                {% csrf_token %}

                    {% if form.non_field_errors %}
                        <div class="error">
                            {% for error in form.non_field_errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}

                {% for field in form %}
                    <div class="InputField">
                        {{ field.label_tag }}
                        {{ field }}
                        {% for error in field.errors %}
                            <div class="error">{{ error }}</div>
                        {% endfor %}
                    </div>
                {% endfor %}

                <div class="ButtonGroup">
                    <button type="submit" class="button button--primary">Register</button>
                </div>
            </form>


            <p class="auth-switch">Already have an account? <a href="{% url 'auth_login' %}">Sign in</a></p>

            <p class="auth-switch">
                <a href="{% url 'auth_email_resend_verification' %}">Запрос на повторное подтверждение регистрации</a>
            </p>
```

`auth/password_reset_confirm.html`

```html
      <form class="auth-form" id="forgot-password-form" method="post">
        <h2>Ввод нового пароля по ссылке из письма</h2>

        {% csrf_token %}

        {% if form.non_field_errors %}
        <div class="error">
            {% for error in form.non_field_errors %}
                {{ error }}
            {% endfor %}
        </div>
        {% endif %}

        {% for field in form %}
            <div class="InputField">
                {{ field.label_tag }}
                {{ field }}

                {% if field.errors %}
                  {% for error in field.errors %}
                    <div class="error">{{ error }}</div>
                  {% endfor %}
                {% endif %}
            </div>
        {% endfor %}

        <div class="ButtonGroup ButtonGroup--center">
          <a href="{% url 'auth_login' %}" class="button button--cancel">Cancel</a>
          <button type="submit" class="button button--primary">Reset Password</button>
        </div>
      </form>
```

`auth/password_reset_form.html`

```html
      <form class="auth-form" id="forgot-password-form" method="post" action="{% url 'auth_password_reset' %}">
        <h2>Запрос письма на восстановление пароля</h2>
        {% csrf_token %}

        {% if form.non_field_errors %}
        <div class="error">
            {% for error in form.non_field_errors %}
                {{ error }}
            {% endfor %}
        </div>
        {% endif %}

        {% for field in form %}
            <div class="InputField">
                {{ field.label_tag }}
                {{ field }}

                {% if field.errors %}
                  {% for error in field.errors %}
                    <div class="error">{{ error }}</div>
                  {% endfor %}
                {% endif %}
            </div>
        {% endfor %}

        <div class="ButtonGroup ButtonGroup--center">
          <a href="{% url 'auth_login' %}" class="button button--cancel">Cancel</a>
          <button type="submit" class="button button--primary">Reset Password</button>
        </div>
      </form>
```