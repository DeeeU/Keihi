# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリのコードを扱う際のガイダンスを提供します。

## プロジェクト概要

**Keihi** は、DjangoとVue.jsを使用したWebアプリケーションプロジェクトです。現在、初期セットアップ段階にあります。

### 技術スタック

- **バックエンド**: Django (Python)
- **フロントエンド**: Vue.js
- **API**: GraphQL (DjangoとVue間のデータ通信)
- **パッケージ管理**: UV, poetry, pdm, pixi, pipenv などに対応

GraphQLを使用してバックエンドとフロントエンド間の効率的なデータ通信を実現します。

## プロジェクトステータス

これは新規リポジトリであり、まだソースコードは実装されていません。CI/CDパイプラインが構築されており、以下のセクションは、プロジェクトの開発が進むにつれて追記されます。

## 開発環境のセットアップ

### パッケージ管理

- **バックエンド**: `uv` を使用 (`pyproject.toml`)
- **フロントエンド**: `npm` を使用 (`package.json`)

### 依存関係のインストール

```bash
# バックエンド
uv pip install -e ".[dev]"
pre-commit install

# フロントエンド
cd frontend && npm install
```

## アーキテクチャ

### プロジェクト構造

```
Keihi/
├── backend/           # Djangoアプリケーション
│   ├── keihi/         # Djangoプロジェクト設定
│   ├── api/           # GraphQL API
│   └── tests/         # バックエンドテスト
├── frontend/          # Vue.jsアプリケーション
│   ├── src/           # ソースコード
│   └── tests/         # フロントエンドテスト
├── .github/
│   └── workflows/     # CI/CD設定
├── docs/              # ドキュメント
└── scripts/           # ビルド/デプロイスクリプト
```

### GraphQL API設計

GraphQLは`graphene-django`を使用して実装します。バックエンドとフロントエンド間のデータ通信に使用され、効率的なクエリとミューテーションを提供します。

_具体的なスキーマ設計は実装後に追加予定_

## テスト

### テストフレームワーク

#### バックエンド
- **pytest**: メインのテストフレームワーク
- **pytest-django**: Django統合
- **pytest-cov**: コードカバレッジ
- **factory-boy**: テストデータ生成
- **Faker**: ダミーデータ生成

#### フロントエンド
- **Vitest**: ユニットテスト
- **Vue Test Utils**: Vueコンポーネントテスト
- **Playwright**: E2Eテスト

### テストの実行

```bash
# バックエンド
pytest --cov

# フロントエンド
cd frontend
npm run test
npm run test:e2e
```

## ビルドとデプロイ

### CI/CDパイプライン

GitHub Actionsを使用したCI/CDパイプラインが構築されています。

#### 自動化されたチェック
1. **コード品質**: Ruff、ESLint、Prettier
2. **型チェック**: mypy、TypeScript
3. **テスト**: pytest、Vitest、Playwright
4. **カバレッジ**: Codecov統合

#### トリガー
- `main`/`develop`ブランチへのプッシュ
- プルリクエストの作成・更新

_デプロイ設定は実装後に追加予定_
