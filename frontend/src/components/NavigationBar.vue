<template>
  <nav class="navigation-bar" :class="{ scrolled: isScrolled, invert: invertColors }">
    <div class="nav-container">
      <div class="nav-brand">
        <!-- Logo removed -->
      </div>
      
      <div class="nav-sections">
        <div class="nav-item" :class="{ active: currentSection === 'introduction' }">
          <button @click="scrollToSection('introduction')" class="nav-button">
            INTRODUCTION
            <div class="progress-border" v-if="showIntroProgress">
              <div class="progress-line" :style="{ width: introProgress + '%' }"></div>
            </div>
          </button>
        </div>
        
        <div class="nav-item" :class="{ active: currentSection === 'news' }">
          <button @click="scrollToSection('news')" class="nav-button">
            NEWS
            <div class="progress-border" v-if="showNewsProgress">
              <div class="progress-line" :style="{ width: '100%' }"></div>
            </div>
          </button>
        </div>
      </div>
      
      <div class="nav-auth">
        <div v-if="!authStore.isAuthenticated" class="auth-buttons">
          <button @click="$emit('openLogin')" class="auth-btn login-btn">
            Login
          </button>
          <button @click="$emit('openRegister')" class="auth-btn register-btn">
            Register
          </button>
        </div>
        
        <div v-else class="user-menu">
          <span class="username">{{ authStore.username }}</span>
          <button @click="goToUserCenter" class="auth-btn user-center-btn">
            User Center
          </button>
          <button @click="logout" class="auth-btn logout-btn">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const props = defineProps<{
  introProgress?: number
  currentSlide?: number
}>()

const emit = defineEmits(['openLogin', 'openRegister', 'navigateToSlide'])

const router = useRouter()
const authStore = useAuthStore()
const isScrolled = ref(false)
const invertColors = ref(false)

// 显示进度条的条件 - 在Introduction页面时始终显示（包括0%）
const showIntroProgress = computed(() => {
  return props.currentSlide === 0
})

// 显示News进度条的条件 - 在News页面时始终显示（包括0%）
const showNewsProgress = computed(() => {
  return props.currentSlide === 1
})

// 确定当前section
const currentSection = computed(() => {
  if (props.currentSlide === 0) return 'introduction'
  if (props.currentSlide === 1) return 'news'
  return 'introduction'
})

// 监听currentSlide变化，实现导航栏样式切换
watch(() => props.currentSlide, (newSlide) => {
  // Introduction页面使用透明导航栏
  if (newSlide === 0) {
    isScrolled.value = false
    invertColors.value = false
  } 
  // News页面使用实心导航栏
  else if (newSlide === 1) {
    isScrolled.value = true
    invertColors.value = false
  }
}, { immediate: true })

const scrollToSection = (section: string) => {
  if (section === 'introduction') {
    emit('navigateToSlide', 0)
  } else if (section === 'news') {
    emit('navigateToSlide', 1)
  }
}

const goToUserCenter = () => {
  router.push('/user-center')
}

const logout = () => {
  authStore.logout()
}

onMounted(() => {
  // 初始化导航栏状态
  if (props.currentSlide === 0) {
    isScrolled.value = false
  } else {
    isScrolled.value = true
  }
})
</script>

<style scoped>
/* 基础导航栏样式 - 模仿FeedMusic原版 */
.navigation-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: transparent;
  backdrop-filter: none;
  border-bottom: none;
  transition: all 0.4s ease;
  height: 70px;
}

.navigation-bar.scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

/* 颜色反转状态 - FeedMusic Tech Spotlight页面效果 */
.navigation-bar.invert {
  background: rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.navigation-bar.invert.scrolled {
  background: rgba(0, 0, 0, 0.95);
  box-shadow: 0 2px 20px rgba(255, 255, 255, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo styles removed */

.nav-sections {
  display: flex;
  gap: 2rem;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.nav-button {
  background: none;
  border: none;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.scrolled .nav-button {
  color: #2c3e50;
}

.invert .nav-button {
  color: #000;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.scrolled .nav-button:hover {
  background: rgba(102, 126, 234, 0.1);
}

.invert .nav-button:hover {
  background: rgba(0, 0, 0, 0.1);
}

.nav-item.active .nav-button {
  background: rgba(255, 255, 255, 0.2);
}

.scrolled .nav-item.active .nav-button {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.invert .nav-item.active .nav-button {
  background: rgba(0, 0, 0, 0.2);
  color: #000;
}

/* FeedMusic原版进度条样式 */
.progress-border {
  width: 60px;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.scrolled .progress-border {
  background: rgba(102, 126, 234, 0.2);
}

.invert .progress-border {
  background: rgba(0, 0, 0, 0.2);
}

.progress-line {
  height: 100%;
  background: white;
  border-radius: 2px;
  transition: width 0.1s ease-out;
  position: absolute;
  top: 0;
  left: 0;
}

.scrolled .progress-line {
  background: #667eea;
}

.invert .progress-line {
  background: #000;
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.auth-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.login-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.register-btn {
  background: #ff6b6b;
  color: white;
}

.scrolled .login-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.invert .login-btn {
  background: rgba(0, 0, 0, 0.2);
  color: #000;
  border: 1px solid rgba(0, 0, 0, 0.3);
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.register-btn:hover {
  background: #ff5252;
  transform: translateY(-1px);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: white;
  font-weight: 600;
  transition: color 0.3s ease;
}

.scrolled .username {
  color: #2c3e50;
}

.invert .username {
  color: #000;
}

.user-center-btn {
  background: #4caf50;
  color: white;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.scrolled .logout-btn {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.invert .logout-btn {
  background: rgba(0, 0, 0, 0.2);
  color: #000;
  border: 1px solid rgba(0, 0, 0, 0.3);
}

.user-center-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.2);
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 15px;
  }
  
  .nav-sections {
    gap: 1rem;
  }
  
  .nav-button {
    font-size: 0.9rem;
    padding: 6px 12px;
  }
  
  .progress-border {
    width: 40px;
  }
  
  .auth-btn {
    padding: 6px 15px;
    font-size: 0.8rem;
  }
  
  .username {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .navigation-bar {
    height: 60px;
  }

  .nav-container {
    padding: 0 10px;
  }

  .nav-brand h2 {
    font-size: 1.1rem;
  }
  
  .nav-sections {
    gap: 0.5rem;
  }

  .nav-button {
    font-size: 0.8rem;
    padding: 4px 8px;
  }

  .progress-border {
    width: 30px;
    height: 2px;
  }
  
  .auth-buttons {
    flex-direction: row;
    gap: 0.3rem;
  }

  .auth-btn {
    padding: 4px 10px;
    font-size: 0.7rem;
  }
  
  .user-menu {
    gap: 0.5rem;
    font-size: 0.7rem;
  }

  .username {
    max-width: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

@media (max-width: 360px) {
  .nav-container {
    flex-wrap: wrap;
    height: auto;
    min-height: 50px;
    padding: 5px;
  }

  .nav-brand {
    order: 1;
    flex: 1;
  }

  .nav-sections {
    order: 3;
    width: 100%;
    justify-content: center;
    margin-top: 5px;
    gap: 1rem;
  }

  .nav-auth {
    order: 2;
  }

  .progress-border {
    display: none;
  }
}
</style>