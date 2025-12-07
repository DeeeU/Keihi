# Keihi Backend

DjangoとStrawberry GraphQLを使用した経費管理アプリケーションのバックエンドAPI

## 技術スタック

- **Django 5.2+** - Pythonウェブフレームワーク
- **Strawberry GraphQL** - PythonのためのGraphQLライブラリ
- **Django CORS Headers** - CORS対応
- **PostgreSQL / SQLite** - データベース（開発環境ではSQLite）
- **Python 3.11+** - プログラミング言語

## プロジェクト構成

```
backend/
├── config/              # Djangoプロジェクト設定
│   ├── settings.py     # 設定ファイル
│   ├── urls.py         # URLルーティング
│   ├── .env.example    # 環境変数のサンプル
│   └── wsgi.py         # WSGIエントリポイント
├── api/                # GraphQL API アプリケーション
│   ├── schema.py       # GraphQLスキーマ定義
│   ├── models.py       # データモデル
│   └── migrations/     # データベースマイグレーション
├── manage.py           # Django管理コマンド
├── requirements.txt    # 本番環境依存関係
├── requirements-dev.txt # 開発環境依存関係
└── pyproject.toml      # プロジェクトメタデータ
```

## セットアップ

### 1. 仮想環境の作成

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\\Scripts\\activate  # Windows
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

開発環境の場合:

```bash
pip install -r requirements-dev.txt
```

### 3. 環境変数の設定

```bash
cp config/.env.example config/.env
# .envファイルを編集して必要な値を設定
```

### 4. データベースのマイグレーション

```bash
python manage.py migrate
```

### 5. 開発サーバーの起動

```bash
python manage.py runserver
```

サーバーは `http://localhost:8000` で起動します。

## GraphQL Playground

GraphQL APIは以下のURLでアクセスできます:

- GraphQL エンドポイント: `http://localhost:8000/graphql/`
- GraphQL Playground: ブラウザで上記URLにアクセス

### サンプルクエリ

```graphql
query {
  hello
}
```

## 開発

### 新しいアプリの作成

```bash
python manage.py startapp app_name
```

### マイグレーションの作成

```bash
python manage.py makemigrations
python manage.py migrate
```

### スーパーユーザーの作成

```bash
python manage.py createsuperuser
```

### テストの実行

```bash
pytest
```

## コード品質

### フォーマット

```bash
black .
```

### リント

```bash
ruff check .
```

### 型チェック

```bash
mypy .
```

## API設計

このプロジェクトはGraphQLを使用しています。スキーマは [api/schema.py](api/schema.py) で定義されています。

## 環境変数

以下の環境変数を `.env` ファイルで設定できます:

- `DEBUG` - デバッグモード (True/False)
- `SECRET_KEY` - Djangoシークレットキー
- `ALLOWED_HOSTS` - 許可するホスト (カンマ区切り)
- `DB_ENGINE` - データベースエンジン
- `DB_NAME` - データベース名
- `CORS_ALLOWED_ORIGINS` - CORS許可オリジン (カンマ区切り)

## ライセンス

_未定_
