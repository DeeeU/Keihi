# Keihi フロントエンド

KeiHiプロジェクトのフロントエンドアプリケーションです。Vue.js 3 + TypeScript + Vite で構築されています。

## 技術スタック

- **フレームワーク**: Vue.js 3 (Composition API)
- **言語**: TypeScript
- **ビルドツール**: Vite
- **ルーティング**: Vue Router
- **状態管理**: Pinia
- **GraphQL Client**: Apollo Client (@vue/apollo-composable)
- **コード品質**: ESLint + Prettier

## プロジェクト構成

```
frontend/
├── src/
│   ├── assets/          # 静的アセット（CSS、画像など）
│   ├── components/      # Vueコンポーネント
│   ├── router/          # Vue Routerの設定
│   ├── stores/          # Piniaストア（状態管理）
│   ├── views/           # ページコンポーネント
│   ├── apollo.ts        # Apollo Client設定
│   ├── App.vue          # ルートコンポーネント
│   └── main.ts          # アプリケーションエントリーポイント
├── public/              # パブリックアセット
├── .env.example         # 環境変数のサンプル
└── vite.config.ts       # Vite設定
```

## セットアップ手順

### 1. 依存関係のインストール

```bash
cd frontend
npm install
```

### 2. 環境変数の設定

`.env.example`ファイルをコピーして`.env.local`を作成します：

```bash
cp .env.example .env.local
```

`.env.local`の内容を確認・編集します：

```env
# GraphQL API Endpoint
VITE_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
```

### 3. 開発サーバーの起動

```bash
npm run dev
```

開発サーバーは http://localhost:5173 で起動します。

### 4. バックエンドとの連携確認

1. バックエンドサーバーが http://localhost:8000 で起動していることを確認
2. フロントエンドアプリケーション（ http://localhost:5173 ）にアクセス
3. GraphQL接続テストコンポーネントで「Hello from GraphQL!」が表示されることを確認

## 利用可能なコマンド

```bash
# 開発サーバーの起動
npm run dev

# 型チェック
npm run type-check

# プロダクションビルド
npm run build

# プロダクションビルドのプレビュー
npm run preview

# コードフォーマット
npm run format

# Lint実行
npm run lint
```

## GraphQL Clientの使い方

このプロジェクトでは、Apollo Clientを使用してバックエンドのGraphQL APIと通信します。

### クエリの実行例

```vue
<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'

const EXAMPLE_QUERY = gql`
  query {
    hello
  }
`

const { result, loading, error } = useQuery(EXAMPLE_QUERY)
</script>

<template>
  <div v-if="loading">読み込み中...</div>
  <div v-else-if="error">エラー: {{ error.message }}</div>
  <div v-else>{{ result.hello }}</div>
</template>
```

### ミューテーションの実行例

```vue
<script setup lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'

const CREATE_ITEM = gql`
  mutation CreateItem($name: String!) {
    createItem(name: $name) {
      id
      name
    }
  }
`

const { mutate, loading, error } = useMutation(CREATE_ITEM)

const handleCreate = async () => {
  await mutate({ name: 'New Item' })
}
</script>
```

## プロキシ設定

開発環境では、Viteのプロキシ機能を使用してCORSの問題を回避しています。

[vite.config.ts](vite.config.ts) で以下のように設定：

```typescript
server: {
  proxy: {
    '/graphql': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

これにより、フロントエンドから `/graphql` へのリクエストが自動的にバックエンドの `http://localhost:8000/graphql` にプロキシされます。

## トラブルシューティング

### GraphQL接続エラー

1. バックエンドサーバーが起動しているか確認
2. `.env.local`のエンドポイントURLが正しいか確認
3. ブラウザの開発者ツールでネットワークタブを確認

### ポート競合

デフォルトポート（5173）が使用中の場合、Viteは自動的に別のポートを使用します。ターミナルに表示されるURLを確認してください。

## 推奨IDE設定

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (Veturは無効化してください)

## 推奨ブラウザ設定

- Chromium系ブラウザ（Chrome、Edge、Braveなど）:
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Chrome DevToolsでCustom Object Formatterを有効化](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Firefox DevToolsでCustom Object Formatterを有効化](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## 今後の開発予定

- [ ] 認証・認可機能の実装
- [ ] 経費管理機能のUIコンポーネント開発
- [ ] ユニットテスト・E2Eテストの追加
- [ ] レスポンシブデザインの最適化
- [ ] PWA対応

## 参考リンク

- [Vue.js 公式ドキュメント](https://ja.vuejs.org/)
- [Vite ドキュメント](https://ja.vitejs.dev/)
- [Apollo Client Vue ドキュメント](https://v4.apollo.vuejs.org/)
- [Vue Router ドキュメント](https://router.vuejs.org/)
- [Pinia ドキュメント](https://pinia.vuejs.org/)
