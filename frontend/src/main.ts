import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.css'
import './types/global.d.ts'
import Hammer from 'hammerjs'

// 全局注册Hammer.js
window.Hammer = Hammer

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')