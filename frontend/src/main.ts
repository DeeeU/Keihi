import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { setupApollo } from './apollo'

const app = createApp(App)

app.use(createPinia())
app.use(router)
setupApollo(app)

app.mount('#app')
