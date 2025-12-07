# Keihi

![CI/CD](https://github.com/DeeeU/Keihi/workflows/CI/CD%20Pipeline/badge.svg)

経費管理アプリケーション

## 概要

**Keihi**は、DjangoとVue.jsを使用して構築された経費管理Webアプリケーションです。GraphQLを使用してバックエンドとフロントエンド間の効率的なデータ通信を実現します。

## 技術スタック

### バックエンド
- **Django 5.1+** - Pythonベースのウェブフレームワーク
- **Strawberry GraphQL** - GraphQL APIライブラリ
- **PostgreSQL** - データベース
- **django-cors-headers** - CORS設定

### フロントエンド
- **Vue.js 3** - プログレッシブJavaScriptフレームワーク (Composition API)
- **TypeScript** - 型安全な開発
- **Vite** - 高速ビルドツール
- **Apollo Client** - GraphQLクライアント
- **Pinia** - 状態管理
- **Vue Router** - ルーティング

### テストフレームワーク

#### バックエンド
- **pytest** - メインのテストフレームワーク
- **pytest-django** - Django統合

#### フロントエンド
- **Vitest** - ユニットテスト
- **@vue/test-utils** - Vueコンポーネントテスト
- **happy-dom** - DOM環境

#### コード品質
- **Ruff** - Python linter & formatter
- **mypy** - Python型チェック
- **ESLint** - JavaScript/TypeScript/Vue linter
- **Prettier** - コードフォーマッター

### 開発ツール
- **pip** - Pythonパッケージ管理
- **npm** - Node.jsパッケージ管理

## プロジェクトステータス

🚧 **初期開発段階**

このプロジェクトは現在、初期セットアップ段階にあります。CI/CDパイプラインが構築され、以下の機能は開発予定です。

## セットアップ

### 前提条件
- Python 3.12以上
- Node.js 20以上
- PostgreSQL 16以上（予定）

### バックエンドのセットアップ

```bash
cd backend

# Python仮想環境の作成（任意）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
pip install -r requirements-dev.txt

# データベースマイグレーション
python manage.py migrate

# 開発サーバーの起動
python manage.py runserver
```

GraphQL Playgroundは http://localhost:8000/graphql/ でアクセス可能です。

### フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 環境変数の設定
cp .env.example .env.local

# 開発サーバーの起動
npm run dev
```

開発サーバーは http://localhost:5173 で起動します。

## テストの実行

### バックエンドテスト

```bash
cd backend

# すべてのテストを実行
pytest

# Watchモードでテストを実行
pytest --watch

# 特定のテストファイルを実行
pytest tests/test_example.py
```

### フロントエンドテスト

```bash
cd frontend

# ユニットテストを実行
npm run test

# Watchモードでテストを実行
npm run test:watch

# UIモードでテストを実行
npm run test:ui
```

## コード品質チェック

### バックエンド

```bash
cd backend

# Ruff lint
ruff check .

# Ruff format
ruff format .

# 型チェック（今後追加予定）
# mypy .
```

### フロントエンド

```bash
cd frontend

# 型チェック
npm run type-check

# ESLint
npm run lint

# Prettier
npm run format
```

## CI/CD

このプロジェクトはGitHub Actionsを使用したCI/CDパイプラインを実装しています。

### ワークフローの詳細

すべてのプルリクエストとmain/developブランチへのプッシュで以下のジョブが並列実行されます：

#### Backend
- **Backend Lint** - Ruffによるlinterとformatterチェック
- **Backend Test** - pytestによるユニットテスト実行

#### Frontend
- **Frontend Lint** - TypeScript型チェック、ESLint、Prettierによるコード品質チェック
- **Frontend Test** - Vitestによるユニットテスト実行

### 実行時間
全ジョブの実行時間は約1分以内で完了します（キャッシュ使用時）。

### バッジステータス
![CI/CD](https://github.com/DeeeU/Keihi/workflows/CI/CD%20Pipeline/badge.svg)

## ライセンス

_ライセンス情報は後日追加予定_

## 貢献

_コントリビューションガイドラインは後日追加予定_
