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


class PaymentMethod(models.Model):
    """支払い方法モデル"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name="支払い方法名")
    code = models.CharField(max_length=20, unique=True, verbose_name="コード")
    icon = models.CharField(max_length=50, blank=True, verbose_name="アイコン")
    is_active = models.BooleanField(default=True, verbose_name="有効")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "支払い方法"
        verbose_name_plural = "支払い方法"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Expense(models.Model):
    """経費モデル"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name="日付")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="金額",
    )
    payment = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name="expenses",
        null=True,
        blank=True,
        verbose_name="支払い方法",
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="expenses", verbose_name="カテゴリー"
    )
    description = models.TextField(verbose_name="説明")
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


class Receipt(models.Model):
    """領収書モデル"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.OneToOneField(
        Expense,
        on_delete=models.CASCADE,
        related_name="receipt",
        null=True,
        blank=True,
        verbose_name="経費",
    )
    file_name = models.CharField(max_length=255, verbose_name="ファイル名")
    file_path = models.CharField(max_length=500, verbose_name="ファイルパス")
    file_size = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="ファイルサイズ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "領収書"
        verbose_name_plural = "領収書"
        ordering = ["-created_at"]

    def __str__(self):
        return self.file_name
