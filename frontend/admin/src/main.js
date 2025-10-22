import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

// Import EdgeRelay API service
import EdgeRelayApiService from './services/edgeRelayApi.js'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Provide EdgeRelay API service globally
const apiService = EdgeRelayApiService
app.provide('$api', apiService)
app.config.globalProperties.$api = apiService

// Initialize authentication store
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.initializeAuth()

app.mount('#app')
