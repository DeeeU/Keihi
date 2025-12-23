<template>
  <div class="container mx-auto p-8">
    <UCard>
      <template #header>
        <h1 class="text-3xl font-bold">Keihi - 経費管理アプリ</h1>
      </template>

      <div class="space-y-4">
        <p class="text-lg">Nuxt 3 + GraphQL + Pinia + Nuxt UIで構築されています</p>

        <div v-if="pending" class="flex items-center gap-2">
          <UIcon name="i-heroicons-arrow-path" class="animate-spin" />
          <span>読み込み中...</span>
        </div>

        <div v-else-if="error" class="text-red-500">
          <p>エラーが発生しました:</p>
          <pre>{{ error }}</pre>
        </div>

        <div v-else-if="data" class="bg-green-50 p-4 rounded">
          <p class="font-semibold">GraphQL接続成功</p>
          <p class="mt-2">サーバーからのメッセージ: {{ data.hello }}</p>
        </div>

        <UButton @click="refresh">再読み込み</UButton>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { gql } from '@apollo/client/core'
import { useQuery } from '@vue/apollo-composable'

const HELLO_QUERY = gql`
  query {
    hello
  }
`

const { result, loading: pending, error, refetch: refresh } = useQuery(HELLO_QUERY)

const data = computed(() => result.value)
</script>
