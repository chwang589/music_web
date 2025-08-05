<template>
  <nav class="navigation-bar" :class="{ scrolled: isScrolled, invert: invertColors }">
    <div class="nav-container">
      <div class="nav-brand">
        <!-- Logo removed -->
      </div>
      
      <!-- 移除汉包菜单按钮 -->
      
      <div class="nav-sections mobile-open"> <!-- 移动端始终显示 -->
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
      
      <div class="nav-auth mobile-open"> <!-- 移动端始终显示 -->
        <div v-if="!authStore.isAuthenticated" class="auth-buttons">
          <button @click="$emit('openLogin')" class="auth-btn login-btn">
            LOGIN
          </button>
          <button @click="$emit('openRegister')" class="auth-btn register-btn">
            REGISTER
          </button>
        </div>
        
        <div v-else class="user-menu">
          <span class="username">{{ authStore.username.toUpperCase() }}</span>
          <button @click="goToUserCenter" class="auth-btn user-center-btn">
            USER CENTER
          </button>
          <button @click="logout" class="auth-btn logout-btn">
            LOGOUT
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
// 移除汉包菜单相关变量

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
  // 移除汉包菜单关闭逻辑
}

// 移除汉包菜单切换函数

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
  color: #3a4d7a;
}

.invert .nav-button {
  color: #000;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.scrolled .nav-button:hover {
  background: rgba(120, 150, 220, 0.15);
}

.invert .nav-button:hover {
  background: rgba(0, 0, 0, 0.1);
}

.nav-item.active .nav-button {
  background: rgba(255, 255, 255, 0.2);
}

.scrolled .nav-item.active .nav-button {
  background: rgba(120, 150, 220, 0.2);
  color: #7896dc;
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

/* Mobile menu toggle button */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 30px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
}

.mobile-menu-toggle span {
  display: block;
  width: 20px;
  height: 2px;
  background: white;
  margin: 3px 0;
  transition: all 0.3s ease;
  transform-origin: center;
}

.scrolled .mobile-menu-toggle span {
  background: #ffffff; /* 滚动时汉包图标也使用白色 */
}

.invert .mobile-menu-toggle span {
  background: #000;
}

.mobile-menu-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.mobile-menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }
  
  .nav-sections {
    position: fixed;
    top: 20px;
    right: 20px;
    left: auto;
    background: transparent !important;
    backdrop-filter: none !important;
    flex-direction: row;
    justify-content: flex-end;
    gap: 20px;
    padding: 0;
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
    transition: all 0.3s ease;
    z-index: 1000;
    border: none !important;
    box-shadow: none !important;
  }
  
  .scrolled .nav-sections {
    display: none !important;
  }
  
  .nav-auth {
    position: fixed;
    bottom: 5px;
    left: 5px;
    right: 5px;
    background: transparent !important;
    backdrop-filter: none !important;
    flex-direction: row;
    justify-content: space-between;
    padding: 0;
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
    transition: all 0.3s ease;
    z-index: 1000;
    border: none !important;
    box-shadow: none !important;
  }
  
  .scrolled .nav-auth {
    position: fixed !important;
    top: 20px !important;
    bottom: auto !important;
    left: auto !important;
    right: 20px !important;
    transform: none !important;
    width: auto !important;
    justify-content: flex-end !important;
    gap: 10px !important;
    flex-direction: row !important;
  }
  
  /* 移动端始终显示 */
  
  /* 移除不需要的样式 */
  
  .scrolled .nav-sections,
  .scrolled .nav-auth {
    background: transparent !important; /* 滚动时也保持透明 */
  }
  
  .scrolled .nav-auth {
    position: fixed !important;
    bottom: 5px !important;
    left: 15px !important;
    right: 15px !important;
  }
  
  .nav-item {
    margin: 0;
    position: relative;
    flex: 0 0 auto;
  }
  
  .nav-button {
    padding: 12px 20px;
    text-align: center;
    font-size: 1.2rem;
    color: #ffffff;
    background: transparent !important;
    backdrop-filter: none !important;
    border: none !important;
    border-radius: 8px;
    transition: all 0.3s ease;
    white-space: nowrap;
    font-weight: 600;
  }
  
  .scrolled .nav-button {
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .nav-button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px);
  }
  
  .nav-button.active {
    background: rgba(255, 255, 255, 0.15) !important;
  }
  
  .scrolled .nav-button {
    color: #2c3e50 !important;
    background: transparent !important;
  }
  
  .auth-buttons {
    flex-direction: row;
    gap: 15px;
    align-items: center;
  }
  
  .auth-btn {
    padding: 8px 12px;
    text-align: center;
    color: #ffffff !important;
    background: transparent !important;
    backdrop-filter: none !important;
    border: none !important;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.3s ease;
    white-space: nowrap;
    flex: 0 0 auto;
  }
  
  
  .scrolled .auth-btn {
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .auth-btn:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px);
    color: #ffffff !important;
  }
  
  .scrolled .auth-btn {
    color: #2c3e50 !important;
  }
  
  .scrolled .auth-btn:hover {
    background: rgba(44, 62, 80, 0.1) !important;
    color: #2c3e50 !important;
  }
  
  .user-menu {
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
  
  .scrolled .user-menu {
    flex-direction: row !important;
    align-items: center !important;
    gap: 10px !important;
  }
  
  .scrolled .user-menu .username {
    display: block !important;
    flex-direction: row !important;
    gap: 0 !important;
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .scrolled .user-menu .auth-btn {
    display: flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .username {
    text-align: center;
    padding: 8px 12px;
    color: #ffffff !important;
    font-weight: 600;
    background: transparent !important;
    backdrop-filter: none !important;
    border: none !important;
    border-radius: 8px;
    font-size: 0.95rem;
    white-space: nowrap;
    flex: 0 0 auto;
    transition: all 0.3s ease;
  }
  
  .username:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px);
  }
  
  .scrolled .username {
    color: #2c3e50 !important;
  }
  
  /* 移动端用户信息统一样式 - 不带进度条 */
  .user-menu .username {
    text-align: center;
    padding: 6px 10px;
    color: #ffffff !important;
    font-weight: 600;
    background: transparent !important;
    backdrop-filter: none !important;
    border: none !important;
    border-radius: 8px;
    font-size: 0.85rem;
    white-space: nowrap;
    flex: 0 0 auto;
    transition: all 0.3s ease;
  }
  
  .user-menu .username:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px);
  }
  
  .scrolled .user-menu .username {
    color: #2c3e50 !important;
  }
  
  .scrolled .user-menu .username:hover {
    background: rgba(44, 62, 80, 0.1) !important;
  }
  
  .scrolled .user-menu .auth-btn {
    text-transform: uppercase;
    padding: 6px 10px !important;
    font-size: 0.8rem;
    font-weight: 600;
  }
  
  .scrolled .user-menu .username {
    padding: 6px 10px !important;
    font-size: 0.8rem;
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
  
  /* 移动端进度条样式 */
  .progress-border {
    position: absolute;
    bottom: 5px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 2px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 1px;
    overflow: hidden;
  }
  
  .progress-line {
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 1px;
    transition: width 0.3s ease;
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