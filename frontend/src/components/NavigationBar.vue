<template>
  <nav class="navigation-bar" :class="{ scrolled: isScrolled }">
    <div class="nav-container">
      <div class="nav-brand">
        <h2>NeuraFlow</h2>
      </div>
      
      <div class="nav-sections">
        <div class="nav-item" :class="{ active: currentSection === 'introduction' }">
          <button @click="scrollToSection('introduction')" class="nav-button">
            Introduction
          </button>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: (introProgress || 0) + '%' }"></div>
          </div>
        </div>
        
        <div class="nav-item" :class="{ active: currentSection === 'news' }">
          <button @click="scrollToSection('news')" class="nav-button">
            News
          </button>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: newsProgress + '%' }"></div>
          </div>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
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
const newsProgress = ref(0)

// Determine current section based on slide index
const currentSection = computed(() => {
  if (props.currentSlide === 0) return 'introduction'
  if (props.currentSlide === 1) return 'news'
  return 'introduction'
})

const scrollToSection = (section: string) => {
  // Use slide navigation instead of scrollIntoView
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

const handleScroll = () => {
  // For slide system, we don't use scroll position to determine section
  // Instead, we use the currentSlide prop
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navigation-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.navigation-bar.scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand h2 {
  color: white;
  margin: 0;
  font-weight: 700;
  transition: color 0.3s ease;
  background: linear-gradient(135deg, #00d4ff, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.scrolled .nav-brand h2 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
}

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
}

.scrolled .nav-button {
  color: #2c3e50;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.scrolled .nav-button:hover {
  background: rgba(102, 126, 234, 0.1);
}

.nav-item.active .nav-button {
  background: rgba(255, 255, 255, 0.2);
}

.scrolled .nav-item.active .nav-button {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.progress-bar {
  width: 60px;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-top: 5px;
  overflow: hidden;
}

.scrolled .progress-bar {
  background: rgba(102, 126, 234, 0.2);
}

.progress-fill {
  height: 100%;
  background: white;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.scrolled .progress-fill {
  background: #667eea;
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

.login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
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
}

.scrolled .username {
  color: #2c3e50;
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

.user-center-btn:hover {
  background: #45a049;
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.2);
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 15px;
    height: 60px;
  }
  
  .nav-sections {
    gap: 1rem;
  }
  
  .nav-button {
    font-size: 0.9rem;
    padding: 6px 12px;
  }
  
  .progress-bar {
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
  .nav-container {
    padding: 0 10px;
    height: 55px;
  }

  .nav-brand h2 {
    font-size: 1.1rem;
  }
  
  .nav-sections {
    gap: 0.3rem;
  }

  .nav-button {
    font-size: 0.8rem;
    padding: 4px 8px;
  }

  .progress-bar {
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
    gap: 0.3rem;
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

  .progress-bar {
    display: none;
  }
}
</style>