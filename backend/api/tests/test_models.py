import pytest
from decimal import Decimal
from datetime import date
from api.models import Category, Expense


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        """カテゴリーを作成できることをテスト"""
        category = Category.objects.create(
            name="交通費", description="電車やバスなどの交通費", color="#FF5733"
        )

        assert category.id is not None
        assert category.name == "交通費"
        assert category.description == "電車やバスなどの交通費"
        assert category.color == "#FF5733"
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_category_str(self):
        """カテゴリーの__str__メソッドをテスト"""
        category = Category.objects.create(name="会議費")
        assert str(category) == "会議費"

    def test_category_unique_name(self):
        """カテゴリー名がユニークであることをテスト"""
        Category.objects.create(name="交通費")

        with pytest.raises(Exception):
            Category.objects.create(name="交通費")


@pytest.mark.django_db
class TestExpenseModel:
    def test_create_expense(self):
        """経費を作成できることをテスト"""
        category = Category.objects.create(name="交通費")
        expense = Expense.objects.create(
            date=date(2024, 12, 7),
            amount=Decimal("1500.00"),
            category=category,
            description="新宿駅から渋谷駅までの電車代",
            payment_method="electronic_money",
        )

        assert expense.id is not None
        assert expense.date == date(2024, 12, 7)
        assert expense.amount == Decimal("1500.00")
        assert expense.category == category
        assert expense.description == "新宿駅から渋谷駅までの電車代"
        assert expense.payment_method == "electronic_money"
        assert expense.created_at is not None
        assert expense.updated_at is not None

    def test_expense_str(self):
        """経費の__str__メソッドをテスト"""
        category = Category.objects.create(name="交通費")
        expense = Expense.objects.create(
            date=date(2024, 12, 7),
            amount=Decimal("1500.00"),
            category=category,
            description="電車代",
            payment_method="cash",
        )
        assert str(expense) == "2024-12-07 - 交通費 - ¥1500.00"

    def test_expense_ordering(self):
        """経費が日付順（降順）でソートされることをテスト"""
        category = Category.objects.create(name="交通費")
        expense1 = Expense.objects.create(
            date=date(2024, 12, 5),
            amount=Decimal("1000.00"),
            category=category,
            description="テスト1",
            payment_method="cash",
        )
        expense2 = Expense.objects.create(
            date=date(2024, 12, 7),
            amount=Decimal("2000.00"),
            category=category,
            description="テスト2",
            payment_method="cash",
        )

        expenses = list(Expense.objects.all())
        assert expenses[0] == expense2  # 新しい日付が先
        assert expenses[1] == expense1

    def test_expense_category_protect(self):
        """カテゴリーに紐づく経費がある場合、カテゴリーを削除できないことをテスト"""
        category = Category.objects.create(name="交通費")
        Expense.objects.create(
            date=date(2024, 12, 7),
            amount=Decimal("1500.00"),
            category=category,
            description="電車代",
            payment_method="cash",
        )

        with pytest.raises(Exception):  # ProtectedError
            category.delete()
