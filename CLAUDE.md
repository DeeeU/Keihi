# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリのコードを扱う際のガイダンスを提供します。

## プロジェクト概要

**Keihi** は、DjangoとVue.jsを使用したWebアプリケーションプロジェクトです。現在、初期セットアップ段階にあります。

### 技術スタック

- **バックエンド**: Django 5.1+ (Python 3.12+)
- **フロントエンド**: Vue.js 3 (Composition API, TypeScript)
- **API**: GraphQL (Strawberry GraphQL)
- **パッケージ管理**:
  - Backend: pip (requirements.txt)
  - Frontend: npm (package.json)

GraphQLを使用してバックエンドとフロントエンド間の効率的なデータ通信を実現します。

## プロジェクトステータス

初期セットアップが完了しています。以下の機能が実装済みです：

✅ **完了**
- Django + Strawberry GraphQLバックエンド
- Vue.js 3 + TypeScriptフロントエンド
- GraphQL APIの接続（バックエンド↔フロントエンド）
- CI/CDパイプライン（GitHub Actions）
- 自動テスト（Backend: pytest, Frontend: Vitest）
- Linter/Formatter設定（Backend: Ruff, Frontend: ESLint + Prettier）

🚧 **開発予定**
- 経費管理機能
- 認証・認可
- データベースモデル設計
- E2Eテスト（Playwright）

## 開発環境のセットアップ

### 依存関係のインストール

```bash
# バックエンド
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# フロントエンド
cd frontend
npm install
cp .env.example .env.local
```

### 開発サーバーの起動

```bash
# バックエンド（別ターミナル）
cd backend
python manage.py migrate
python manage.py runserver
# → http://localhost:8000/graphql/

# フロントエンド（別ターミナル）
cd frontend
npm run dev
# → http://localhost:5173
```

## アーキテクチャ

### プロジェクト構造

```
Keihi/
├── backend/           # Djangoアプリケーション
│   ├── config/        # Djangoプロジェクト設定
│   │   ├── settings.py
│   │   └── urls.py
│   ├── api/           # GraphQL API
│   │   ├── schema.py  # Strawberry GraphQLスキーマ
│   │   ├── models.py
│   │   └── tests.py
│   ├── tests/         # 統合テスト
│   │   ├── conftest.py
│   │   └── test_example.py
│   ├── pytest.ini     # pytest設定
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/          # Vue.jsアプリケーション
│   ├── src/
│   │   ├── components/
│   │   │   └── __tests__/  # コンポーネントテスト
│   │   ├── __tests__/      # ユニットテスト
│   │   ├── apollo.ts       # Apollo Client設定
│   │   └── main.ts
│   ├── tests/         # 統合テスト
│   ├── vitest.config.ts
│   └── package.json
├── .github/
│   └── workflows/
│       └── ci.yml     # CI/CDパイプライン
└── README.md
```

### GraphQL API設計

GraphQLは`Strawberry GraphQL`を使用して実装されています。

**現在の実装:**
- `hello` クエリ - 接続テスト用の基本クエリ
- エンドポイント: `http://localhost:8000/graphql/`
- CSRF保護: GraphQLエンドポイントはCSRF exemptに設定
- CORS: フロントエンド（localhost:5173）からのアクセスを許可

**今後の実装予定:**
- 経費データのCRUD操作
- ユーザー認証
- カテゴリー管理

## テスト

### テストフレームワーク

#### バックエンド
- **pytest**: メインのテストフレームワーク
- **pytest-django**: Django統合

サンプルテスト: `backend/tests/test_example.py`

#### フロントエンド
- **Vitest**: ユニットテスト
- **@vue/test-utils**: Vueコンポーネントテスト
- **happy-dom**: DOM環境

サンプルテスト:
- `frontend/src/__tests__/example.spec.ts`
- `frontend/src/components/__tests__/HelloWorld.spec.ts`

### テストの実行

```bash
# バックエンド
cd backend
pytest

# フロントエンド
cd frontend
npm run test        # 一度だけ実行
npm run test:watch  # Watchモード
npm run test:ui     # UIモード
```

### コード品質ツール

#### Backend
- **Ruff**: Linter & Formatter
```bash
ruff check .
ruff format .
```

#### Frontend
- **TypeScript**: 型チェック
- **ESLint**: Linter
- **Prettier**: Formatter
```bash
npm run type-check
npm run lint
npm run format
```

## ビルドとデプロイ

### CI/CDパイプライン

GitHub Actionsを使用したCI/CDパイプライン(`.github/workflows/ci.yml`)が構築されています。

#### ワークフロージョブ

すべてのジョブは並列実行されます：

1. **Backend Lint** (~17秒)
   - Ruffによるlinterチェック
   - Ruffによるformatterチェック

2. **Backend Test** (~17秒)
   - pytestによるユニットテスト実行

3. **Frontend Lint** (~20秒)
   - TypeScript型チェック
   - ESLint
   - Prettier

4. **Frontend Test** (~23秒)
   - Vitestによるユニットテスト実行

#### トリガー
- `main`/`develop`ブランチへのプッシュ
- プルリクエストの作成・更新

#### 実行時間
全ジョブの合計実行時間: 約1分以内（キャッシュ使用時）

_デプロイ設定は実装後に追加予定_
