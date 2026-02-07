from django.conf import settings
from django.db import models
from django.utils import timezone


class Order(models.Model):
    class PaymentProvider(models.TextChoices):
        REVOLUT = "revolut", "Revolut"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        CANCELED = "CANCELED", "Canceled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    # Shipping/contact
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    country = models.CharField(max_length=80)

    # Payment tracking
    payment_provider = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices,
        default=PaymentProvider.REVOLUT,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    payment_reference = models.CharField(max_length=120, blank=True, null=True)  # Revolut order/payment id
    paid_at = models.DateTimeField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_paid(self, reference: str | None = None):
        """Mark order as paid (use from webhook/confirmation)."""
        self.payment_status = self.PaymentStatus.PAID
        if reference:
            self.payment_reference = reference
        self.paid_at = timezone.now()
        self.save(update_fields=["payment_status", "payment_reference", "paid_at"])

    @property
    def total_amount(self) -> float:
        """Order total (numeric)."""
        return float(sum(item.line_total for item in self.items.all()))

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.full_name} ({self.payment_status})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "checkout.Order",
        related_name="items",
        on_delete=models.CASCADE,
    )
    product_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self) -> float:
        return float(self.price) * int(self.quantity)

    def __str__(self) -> str:
        return f"{self.product_name} x {self.quantity}"
