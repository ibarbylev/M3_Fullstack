from django.db import models
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta
import uuid

# ------------------------------
# Product
# ------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default="шт")
    category_id = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    specs = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            # Проверка на уникальность
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def is_in_stock(self):
        return self.stock > 0

# ------------------------------
# Order / OrderItem
# ------------------------------
class Order(models.Model):
    STATUS_CHOICES = (
        ("cart", "Cart"),
        ("pending", "Pending"),
        ("paid", "Paid"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=255, blank=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="cart")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} {self.status} {self.user}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            now = timezone.now()
            candidate_id = f"{now.strftime('%Y%m%d__%H%M%S')}__{self.user.id}"

            # проверяем уникальность
            while Order.objects.filter(order_id=candidate_id).exists():
                # добавляем 1 секунду
                now += timezone.timedelta(seconds=1)
                candidate_id = f"{now.strftime('%Y%m%d__%H%M%S')}__{self.user.id}"

            self.order_id = candidate_id

        super().save(*args, **kwargs)

    def add_product(self, product, quantity=1):
        """
        Добавляет продукт в заказ или корзину.
        Если товар уже есть в корзине, увеличивает количество.
        """
        item, created = self.items.get_or_create(
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        if not created:
            item.quantity += quantity
            item.save()

    def recalculate_total(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = total
        self.save(update_fields=["total_price", "updated_at"])

    def to_pending(self):
        """
        Перевод корзины в заказ и генерация order_id.
        """
        if self.status != "cart":
            raise ValueError("Order is not in cart status")
        self.status = "pending"
        # self.order_id = f"{self.created_at.strftime('%Y%m%d_%H%M%S')}__{self.user.id}"
        self.save(update_fields=["status", "order_id"])
        # после перевода в pending — проверяем автооплату
        Payment.process_auto(self.user)

    @classmethod
    def cleanup_expired_carts(cls):
        """
        Удаляет все корзины (status='cart'), которые не изменялись более 7 дней.
        """
        expiration_time = timezone.now() - timedelta(days=7)
        expired_carts = cls.objects.filter(status="cart", created_at__lt=expiration_time)
        expired_carts.delete()

    @classmethod
    def cleanup_old_pending(cls, days=100):
        """
        Удаляет заказа, не оплаченные в течение 100 дней.
        """
        cutoff = timezone.now() - timedelta(days=days)
        cls.objects.filter(status="pending", created_at__lt=cutoff).delete()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

# ------------------------------
# Payment
# ------------------------------
class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    @transaction.atomic
    def process(cls, order):
        """Оплата заказа (только для pending)."""
        if order.status != "pending":
            return  # Просто выходим, если не pending (избегаем raise для nested вызовов)

        profile = order.user.userprofile
        if profile.balance < order.total_price:
            raise ValueError("Insufficient balance")

        # Списание в памяти
        profile.balance -= order.total_price

        # Сначала меняем статус заказа и сохраняем (чтобы исключить из pending в nested)
        order.status = "paid"
        order.save(update_fields=["status"])

        # Затем сохраняем профиль (триггерит сигнал, но заказ уже paid)
        profile.save(update_fields=["balance"])

        # Создаём payment
        payment = cls.objects.create(
            order=order,
            status="completed",
        )
        return payment

    @classmethod
    @transaction.atomic
    def process_auto(cls, user):
        """Автоматическая оплата всех pending-заказов при наличии средств."""
        profile = user.userprofile
        while True:
            # Динамически берём следующий pending-заказ
            order = user.orders.filter(status="pending").order_by("created_at").first()
            if not order:
                break
            if profile.balance < order.total_price:
                break
            cls.process(order)

# ------------------------------
# Review
# ------------------------------
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# ------------------------------
# Сигналы
# ------------------------------

# Автоматический пересчёт total_price при изменении OrderItem
@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.recalculate_total()

# Автоматическая проверка автооплаты при создании Payment
@receiver(post_save, sender=Payment)
def check_auto_payment(sender, instance, created, **kwargs):
    if created and instance.status == "pending":
        Payment.process_auto(instance.order.user)
