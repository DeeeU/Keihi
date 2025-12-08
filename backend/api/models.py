import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """経費カテゴリーモデル"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="カテゴリー名")
    description = models.TextField(blank=True, verbose_name="説明")
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="カラーコード")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Expense(models.Model):
    """経費モデル"""

    PAYMENT_METHOD_CHOICES = [
        ("cash", "現金"),
        ("credit_card", "クレジットカード"),
        ("debit_card", "デビットカード"),
        ("electronic_money", "電子マネー"),
        ("bank_transfer", "銀行振込"),
        ("other", "その他"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name="日付")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="金額",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="expenses", verbose_name="カテゴリー"
    )
    description = models.TextField(verbose_name="説明")
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cash", verbose_name="支払い方法"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "経費"
        verbose_name_plural = "経費"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["-date"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.date} - {self.category.name} - ¥{self.amount}"
