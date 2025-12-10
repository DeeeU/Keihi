# CLAUDE.md - Backend

このファイルは、Claude Code (claude.ai/code) がこのバックエンドプロジェクトを扱う際のガイダンスを提供します。

## プロジェクト概要

**Keihi Backend** は、Django 6.0とStrawberry GraphQLを使用した経費管理システムのバックエンドAPIです。

### 技術スタック

- **フレームワーク**: Django 6.0
- **Python**: 3.12+
- **API**: GraphQL (Strawberry GraphQL)
- **データベース**: SQLite（開発環境）/ PostgreSQL（本番環境予定）
- **パッケージ管理**: pip (requirements.txt, requirements-dev.txt)
- **テスト**: pytest, pytest-django
- **Linter/Formatter**: Ruff

## プロジェクト構造

```
backend/
├── config/              # Djangoプロジェクト設定
│   ├── settings.py      # Django設定ファイル
│   ├── urls.py          # URLルーティング
│   └── wsgi.py          # WSGI設定
├── api/                 # メインアプリケーション
│   ├── models.py        # データモデル定義
│   ├── schema.py        # GraphQLスキーマ（Strawberry）
│   ├── migrations/      # データベースマイグレーション
│   ├── tests/           # ユニットテスト
│   │   ├── __init__.py
│   │   └── test_models.py
│   ├── admin.py         # Django Admin設定
│   └── apps.py
├── tests/               # 統合テスト
│   ├── conftest.py      # pytest設定・フィクスチャ
│   └── test_example.py
├── manage.py            # Django管理コマンド
├── pytest.ini           # pytest設定
├── requirements.txt     # 本番用依存関係
├── requirements-dev.txt # 開発用依存関係
└── CLAUDE.md            # このファイル
```

## データモデル

### Category（経費カテゴリー）
```python
- id: UUIDField (PK)
- name: CharField (unique)
- description: TextField
- color: CharField (カラーコード)
- created_at, updated_at: DateTimeField
```

### PaymentMethod（支払い方法）
```python
- id: UUIDField (PK)
- name: CharField
- code: CharField (unique)
- icon: CharField (blank=True)
- is_active: BooleanField (default=True)
- created_at, updated_at: DateTimeField
```

### Expense（経費）
```python
- id: UUIDField (PK)
- date: DateField
- amount: DecimalField
- category: ForeignKey → Category (PROTECT)
- payment: ForeignKey → PaymentMethod (PROTECT, null=True)
- description: TextField
- created_at, updated_at: DateTimeField
```

### Receipt（領収書）
```python
- id: UUIDField (PK)
- expense: OneToOneField → Expense (CASCADE, null=True)
- file_name: CharField
- file_path: CharField
- file_size: IntegerField
- created_at, updated_at: DateTimeField
```

## モデル間のリレーション

```
Category ←(PROTECT)─┐
                    │
PaymentMethod ←(PROTECT)─── Expense ─(CASCADE)→ Receipt
                    │
                    └→ related_name="expenses"
```

### リレーションの特徴

1. **Category → Expense (PROTECT)**
   - Categoryに紐づくExpenseがある場合、Categoryは削除できない

2. **PaymentMethod → Expense (PROTECT)**
   - PaymentMethodに紐づくExpenseがある場合、PaymentMethodは削除できない
   - null=True: Expenseは支払い方法なしで作成可能

3. **Expense → Receipt (CASCADE)**
   - Expenseを削除すると、紐づくReceiptも自動削除される
   - OneToOneField: 1つのExpenseに対して1つのReceiptのみ

## 開発ワークフロー

### 1. 開発サーバーの起動

```bash
cd backend
python manage.py runserver
# → http://localhost:8000/
# → http://localhost:8000/graphql/ (GraphQL Playground)
```

### 2. マイグレーション

```bash
# モデル変更後、マイグレーションファイルを生成
python manage.py makemigrations

# マイグレーションを適用
python manage.py migrate

# マイグレーション状態を確認
python manage.py showmigrations
```

### 3. テストの実行

```bash
# 全テスト実行
pytest

# 特定のテストファイルを実行
pytest api/tests/test_models.py

# 特定のテストクラスを実行
pytest api/tests/test_models.py::TestExpenseModel

# 詳細出力（-v）
pytest -v

# カバレッジ付き（要pytest-cov）
pytest --cov=api
```

### 4. コード品質チェック

```bash
# Ruffでlintチェック
ruff check .

# Ruffで自動修正
ruff check --fix .

# Ruffでフォーマット
ruff format .
```

### 5. Django管理コマンド

```bash
# スーパーユーザー作成
python manage.py createsuperuser

# Django shell起動（対話的にモデル操作）
python manage.py shell

# データベースリセット（開発時のみ）
python manage.py flush
```

## GraphQL API

### エンドポイント
- **開発**: `http://localhost:8000/graphql/`
- **GraphQL Playground**: ブラウザでエンドポイントにアクセス

### 現在の実装

```graphql
type Query {
  hello: String
}
```

### 設定

- **CSRF保護**: GraphQLエンドポイントはCSRF exemptに設定（`csrf_exempt`）
- **CORS**: フロントエンド（localhost:5173）からのアクセスを許可
- **認証**: 未実装（今後追加予定）

### 今後の実装予定

```graphql
# 経費のCRUD操作
type Query {
  expenses: [Expense!]!
  expense(id: UUID!): Expense
  categories: [Category!]!
  paymentMethods: [PaymentMethod!]!
}

type Mutation {
  createExpense(input: ExpenseInput!): Expense!
  updateExpense(id: UUID!, input: ExpenseInput!): Expense!
  deleteExpense(id: UUID!): Boolean!
}
```

## テスト戦略

### ユニットテスト（api/tests/）

各モデルごとにテストクラスを作成：

- **TestCategoryModel** (3テスト)
  - 作成、__str__、unique制約

- **TestExpenseModel** (4テスト)
  - 作成、__str__、並び順、PROTECT制約

- **TestReceiptModel** (4テスト)
  - 作成、__str__、OneToOne関係、CASCADE削除

- **TestPaymentMethodModel** (5テスト)
  - 作成、__str__、unique制約、ForeignKey関係、PROTECT制約

### テストのベストプラクティス

1. **@pytest.mark.django_db デコレータ必須**
   - データベースアクセスを伴うテストに必要

2. **テストの独立性**
   - 各テストは独立して実行可能であること
   - テスト間でデータを共有しない

3. **Docstring必須**
   - 各テストメソッドにdocstringで目的を記載

4. **明確なassert**
   - 何をテストしているか明確にする
   - 必要に応じてコメントを追加

## Django Admin

Django Adminで全モデルを管理可能：

```bash
# スーパーユーザーでログイン
http://localhost:8000/admin/
```

### 登録済みモデル
- Category
- Expense
- PaymentMethod
- Receipt

## 環境設定

### 必須環境変数

現在は不要（SQLiteを使用）。今後、本番環境では以下が必要：

```bash
# .env ファイル（今後）
DATABASE_URL=postgresql://user:pass@localhost:5432/keihi
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

### 依存関係のインストール

```bash
# 本番用依存関係
pip install -r requirements.txt

# 開発用依存関係（pytestなど）
pip install -r requirements-dev.txt
```

## コーディング規約

### モデル定義

1. **必ずUUIDFieldをPKに使用**
   ```python
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   ```

2. **verbose_nameを必ず設定**
   ```python
   name = models.CharField(max_length=100, verbose_name="カテゴリー名")
   ```

3. **created_at, updated_atを含める**
   ```python
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
   updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
   ```

4. **Metaクラスで日本語名を設定**
   ```python
   class Meta:
       verbose_name = "カテゴリー"
       verbose_name_plural = "カテゴリー"
       ordering = ["name"]
   ```

5. **__str__メソッドを実装**
   ```python
   def __str__(self):
       return self.name
   ```

### GraphQLスキーマ（Strawberry）

1. **型定義にはstrawberry.Typeを使用**
   ```python
   @strawberry.type
   class ExpenseType:
       id: strawberry.ID
       date: datetime.date
       amount: Decimal
   ```

2. **Queryクラスでエンドポイント定義**
   ```python
   @strawberry.type
   class Query:
       @strawberry.field
       def expenses(self) -> List[ExpenseType]:
           return Expense.objects.all()
   ```

## トラブルシューティング

### マイグレーションエラー

```bash
# マイグレーションをリセット（開発時のみ）
python manage.py migrate api zero
python manage.py migrate

# または、データベースを削除して再作成
rm db.sqlite3
python manage.py migrate
```

### テストが失敗する

```bash
# データベースを再作成してテスト
pytest --create-db

# 詳細ログ付きで実行
pytest -vv --tb=short
```

### Ruffエラー

```bash
# 自動修正できるものは修正
ruff check --fix .

# フォーマットを適用
ruff format .
```

## 今後の実装予定

### Phase 2: GraphQL API実装
- [ ] CRUD操作のMutation実装
- [ ] フィルタリング・ソート機能
- [ ] ページネーション
- [ ] エラーハンドリング

### Phase 3: 認証・認可
- [ ] ユーザーモデル
- [ ] JWT認証
- [ ] パーミッション管理

### Phase 4: ファイルアップロード
- [ ] 領収書画像のアップロード機能
- [ ] S3連携（本番環境）
- [ ] 画像のサムネイル生成

### Phase 5: 高度な機能
- [ ] 経費の承認ワークフロー
- [ ] 月次・年次レポート
- [ ] エクスポート機能（CSV, Excel）
- [ ] カテゴリーの階層構造

## 参考リンク

- [Django Documentation](https://docs.djangoproject.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
