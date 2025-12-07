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

## 開発ワークフロー自動化（Claude Code Hooks）

このプロジェクトでは、Claude Code の hooks 機能を使用して、開発ワークフローを自動化しています。

### コミット前の自動Linter実行

**目的**: コードの品質を保ち、Linterエラーを早期に検出

**動作**:
- Claudeが `git commit` を実行する前に自動的にLinterを実行
- 変更されたファイルを検出し、該当する側のLinterのみを実行
- Linterエラーがある場合はコミットをブロック

**対象**:
- **Backend**: `ruff check` + `ruff format`
- **Frontend**: `npm run type-check` + `npm run lint` + `npm run format`

**設定ファイル**:
- `.claude/hooks/pre_commit_lint.py` - Pre-commit hook スクリプト
- `.claude/settings.json` の `PreToolUse` hook

### PR作成前の自動テスト実行

**目的**: すべてのテストが通過していることを確認してからPRを作成

**動作**:
- ユーザーが「PR作成」などのキーワードを入力すると自動検出
- 変更されたファイルに応じて適切なテストを実行するよう促す
- CI/CDパイプラインの確認も促す

**対象**:
- **Backend**: pytest によるユニットテスト
- **Frontend**: Vitest によるユニットテスト

**設定ファイル**:
- `.claude/hooks/pr_pre_check.py` - PR作成前チェックスクリプト
- `.claude/settings.json` の `UserPromptSubmit` hook

### カスタムスラッシュコマンド

#### `/create-pr`

PR作成前に必要なすべてのチェックを自動的に実行します。

```
/create-pr
```

**実行内容**:
1. 変更ファイルの確認（`git diff`）
2. backend/frontendの変更検出
3. 該当するテストの実行（backend-tester/frontend-tester agent）
4. CI/CD確認
5. PR作成

### Claude Code Agent の役割分担

#### backend-tester
- **役割**: pytest テスト実行専門
- **Linter**: pre-commit hook で自動実行済みのため、テストのみに集中

#### frontend-tester
- **役割**: Vitest テスト実行専門
- **Linter**: pre-commit hook で自動実行済みのため、テストのみに集中

### ワークフロー図

```
コード変更
   ↓
コミット実行（Claudeが実行）
   ↓
[PreToolUse Hook] ← Linter自動実行
   ├─ Backend: ruff check + format
   └─ Frontend: type-check + lint + format
   ↓
Linter成功 → コミット完了
Linterエラー → コミットブロック（修正が必要）
   ↓
PR作成依頼
   ↓
[UserPromptSubmit Hook] ← テスト実行を促す
   ├─ Backend: backend-tester agent
   └─ Frontend: frontend-tester agent
   ↓
テスト + CI/CD確認
   ↓
PR作成
```

### 設定ファイル一覧

```
.claude/
├── settings.json              # Hooks設定
├── hooks/
│   ├── pre_commit_lint.py    # コミット前Linter
│   └── pr_pre_check.py       # PR作成前チェック
├── commands/
│   └── create-pr.md          # カスタムコマンド
└── agents/
    ├── backend-tester.md     # バックエンドテスト専門
    └── frontend-tester.md    # フロントエンドテスト専門
```

### メリット

1. **早期エラー検出**: コミット時にLinterエラーを検出し、早期に修正
2. **品質保証**: PR作成前にすべてのテストが実行され、品質を保証
3. **自動化**: 手動でのLinter/テスト実行を忘れることがない
4. **効率化**: 役割分担により、各段階で必要なチェックのみを実行

## ライセンス

_ライセンス情報は後日追加予定_

## 貢献

_コントリビューションガイドラインは後日追加予定_
