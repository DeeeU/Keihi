<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'

// GraphQLクエリの定義
const HELLO_QUERY = gql`
  query {
    hello
  }
`

// クエリの実行
const { result, loading, error } = useQuery(HELLO_QUERY)
</script>

<template>
  <div class="graphql-test">
    <h2>GraphQL接続テスト</h2>

    <div v-if="loading" class="loading">
      読み込み中...
    </div>

    <div v-else-if="error" class="error">
      <p>エラーが発生しました:</p>
      <pre>{{ error.message }}</pre>
    </div>

    <div v-else-if="result" class="success">
      <p>バックエンドからのレスポンス:</p>
      <pre>{{ result.hello }}</pre>
    </div>
  </div>
</template>

<style scoped>
.graphql-test {
  padding: 2rem;
  border: 2px solid #42b983;
  border-radius: 8px;
  margin: 1rem 0;
}

h2 {
  color: #42b983;
  margin-bottom: 1rem;
}

.loading {
  color: #ffa500;
  font-weight: bold;
}

.error {
  color: #ff0000;
}

.error pre {
  background-color: #ffe0e0;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}

.success {
  color: #42b983;
}

.success pre {
  background-color: #e8f5e9;
  padding: 1rem;
  border-radius: 4px;
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
