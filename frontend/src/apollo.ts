import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client/core'
import { DefaultApolloClient } from '@vue/apollo-composable'
import type { App } from 'vue'

// GraphQL APIのエンドポイント
const httpLink = new HttpLink({
  uri: import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql',
})

// Apollo Clientインスタンスの作成
export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
})

// Vueアプリケーションにプラグインとして登録する関数
export function setupApollo(app: App) {
  app.provide(DefaultApolloClient, apolloClient)
}
