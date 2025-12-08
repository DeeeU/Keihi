import strawberry
import strawberry_django
from typing import List, Optional
from decimal import Decimal
import datetime
from .models import Category as CategoryModel, Expense as ExpenseModel


@strawberry_django.type(CategoryModel)
class Category:
    id: strawberry.ID
    name: str
    description: str
    color: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry_django.type(ExpenseModel)
class Expense:
    id: strawberry.ID
    date: datetime.date
    amount: Decimal
    category: Category
    description: str
    payment_method: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.input
class CategoryInput:
    name: str
    description: Optional[str] = ""
    color: Optional[str] = "#3B82F6"


@strawberry.input
class ExpenseInput:
    date: datetime.date
    amount: Decimal
    category_id: strawberry.ID
    description: str
    payment_method: str


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from Keihi GraphQL API"

    @strawberry.field
    def categories(self) -> List[Category]:
        return CategoryModel.objects.all()

    @strawberry.field
    def category(self, id: strawberry.ID) -> Optional[Category]:
        try:
            return CategoryModel.objects.get(pk=id)
        except CategoryModel.DoesNotExist:
            return None

    @strawberry.field
    def expenses(self) -> List[Expense]:
        return ExpenseModel.objects.select_related("category").all()

    @strawberry.field
    def expense(self, id: strawberry.ID) -> Optional[Expense]:
        try:
            return ExpenseModel.objects.select_related("category").get(pk=id)
        except ExpenseModel.DoesNotExist:
            return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_category(self, input: CategoryInput) -> Category:
        category = CategoryModel.objects.create(
            name=input.name, description=input.description, color=input.color
        )
        return category

    @strawberry.mutation
    def create_expense(self, input: ExpenseInput) -> Expense:
        category = CategoryModel.objects.get(pk=input.category_id)
        expense = ExpenseModel.objects.create(
            date=input.date,
            amount=input.amount,
            category=category,
            description=input.description,
            payment_method=input.payment_method,
        )
        return expense

    @strawberry.mutation
    def update_expense(self, id: strawberry.ID, input: ExpenseInput) -> Expense:
        expense = ExpenseModel.objects.get(pk=id)
        expense.date = input.date
        expense.amount = input.amount
        expense.category = CategoryModel.objects.get(pk=input.category_id)
        expense.description = input.description
        expense.payment_method = input.payment_method
        expense.save()
        return expense

    @strawberry.mutation
    def delete_expense(self, id: strawberry.ID) -> bool:
        try:
            expense = ExpenseModel.objects.get(pk=id)
            expense.delete()
            return True
        except ExpenseModel.DoesNotExist:
            return False


schema = strawberry.Schema(query=Query, mutation=Mutation)
