# Keihi

![CI/CD](https://github.com/DeeeU/Keihi/workflows/CI/CD%20Pipeline/badge.svg)

経費管理アプリケーション

## 概要

**Keihi**は、DjangoとVue.jsを使用して構築された経費管理Webアプリケーションです。GraphQLを使用してバックエンドとフロントエンド間の効率的なデータ通信を実現します。

## 技術スタック

### バックエンド
- **Django** - Pythonベースのウェブフレームワーク
- **GraphQL** (Graphene-Django) - APIレイヤー
- **PostgreSQL** - データベース

### フロントエンド
- **Vue.js 3** - プログレッシブJavaScriptフレームワーク
- **Vite** - ビルドツール
- **Apollo Client** - GraphQLクライアント

### テストフレームワーク

#### バックエンド
- **pytest** - メインのテストフレームワーク
- **pytest-django** - Django統合
- **pytest-cov** - コードカバレッジ測定
- **factory-boy** - テストデータ生成
- **Faker** - ダミーデータ生成

#### フロントエンド
- **Vitest** - ユニットテスト
- **Vue Test Utils** - Vueコンポーネントテスト
- **Playwright** - E2Eテスト

#### コード品質
- **Ruff** - Python linter & formatter
- **mypy** - Python型チェック
- **ESLint** - JavaScript/Vue linter
- **Prettier** - コードフォーマッター

### 開発ツール
- **uv** - Pythonパッケージ管理
- **npm** - Node.jsパッケージ管理
- **pre-commit** - Git pre-commitフック

## プロジェクトステータス

🚧 **初期開発段階**

このプロジェクトは現在、初期セットアップ段階にあります。CI/CDパイプラインが構築され、以下の機能は開発予定です。

## セットアップ

### 前提条件
- Python 3.11以上
- Node.js 18以上
- PostgreSQL 16以上
- uv (Python package manager)

### バックエンドのセットアップ

```bash
# 依存関係のインストール
uv pip install -e ".[dev]"

# pre-commitフックのインストール
pre-commit install

# データベースマイグレーション（実装後）
# python backend/manage.py migrate

# 開発サーバーの起動（実装後）
# python backend/manage.py runserver
```

### フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# ビルド
npm run build
```

## テストの実行

### バックエンドテスト

```bash
# すべてのテストを実行
pytest

# カバレッジ付きでテストを実行
pytest --cov --cov-report=html

# 特定のテストファイルを実行
pytest backend/tests/test_example.py
```

### フロントエンドテスト

```bash
cd frontend

# ユニットテストを実行
npm run test

# カバレッジ付きでテストを実行
npm run test:coverage

# E2Eテストを実行
npm run test:e2e
```

## コード品質チェック

### バックエンド

```bash
# Ruff lint
ruff check backend/

# Ruff format
ruff format backend/

# 型チェック
mypy backend/
```

### フロントエンド

```bash
cd frontend

# ESLint
npm run lint

# Prettier
npx prettier --write src/
```

## CI/CD

このプロジェクトはGitHub Actionsを使用したCI/CDパイプラインを実装しています。

### ワークフロー

- **Backend Lint**: Ruff、mypy による静的解析
- **Backend Tests**: pytest によるテスト実行とカバレッジ測定
- **Frontend Lint**: ESLint、Prettier によるコード品質チェック
- **Frontend Tests**: Vitest によるユニットテストとカバレッジ測定
- **E2E Tests**: Playwright によるE2Eテスト

すべてのプルリクエストとmain/developブランチへのプッシュで自動的に実行されます。

## ライセンス

_ライセンス情報は後日追加予定_

## 貢献

_コントリビューションガイドラインは後日追加予定_
