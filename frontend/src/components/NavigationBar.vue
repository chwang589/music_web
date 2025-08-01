<template>
  <nav class="navigation-bar" :class="{ scrolled: isScrolled }">
    <div class="nav-container">
      <div class="nav-brand">
        <h2>Music Web</h2>
      </div>
      
      <div class="nav-sections">
        <div class="nav-item" :class="{ active: currentSection === 'introduction' }">
          <button @click="scrollToSection('introduction')" class="nav-button">
            Introduction
          </button>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: introProgress + '%' }"></div>
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
          <button @click="$emit('openAdmin')" class="auth-btn admin-btn">
            Admin
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'

defineEmits(['openLogin', 'openRegister', 'openAdmin'])

const authStore = useAuthStore()
const isScrolled = ref(false)
const currentSection = ref('introduction')
const introProgress = ref(0)
const newsProgress = ref(0)

const scrollToSection = (section: string) => {
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const logout = () => {
  authStore.logout()
}

const handleScroll = () => {
  const scrollTop = window.pageYOffset
  const windowHeight = window.innerHeight
  
  isScrolled.value = scrollTop > 50
  
  // Calculate progress for introduction section
  const introSection = document.getElementById('introduction')
  if (introSection) {
    const introTop = introSection.offsetTop
    const introHeight = introSection.offsetHeight
    
    if (scrollTop >= introTop && scrollTop < introTop + introHeight) {
      currentSection.value = 'introduction'
      introProgress.value = Math.min(100, ((scrollTop - introTop) / introHeight) * 100)
    } else if (scrollTop < introTop) {
      introProgress.value = 0
    } else {
      introProgress.value = 100
    }
  }
  
  // Calculate progress for news section
  const newsSection = document.getElementById('news')
  if (newsSection) {
    const newsTop = newsSection.offsetTop
    const newsHeight = newsSection.offsetHeight
    
    if (scrollTop >= newsTop - windowHeight / 2) {
      currentSection.value = 'news'
      if (scrollTop >= newsTop) {
        newsProgress.value = Math.min(100, ((scrollTop - newsTop) / newsHeight) * 100)
      }
    } else {
      newsProgress.value = 0
    }
  }
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
}

.scrolled .nav-brand h2 {
  color: #2c3e50;
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

.admin-btn {
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

.admin-btn:hover {
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
  .nav-brand h2 {
    font-size: 1.2rem;
  }
  
  .nav-sections {
    gap: 0.5rem;
  }
  
  .auth-buttons {
    flex-direction: column;
    gap: 0.3rem;
  }
  
  .user-menu {
    flex-direction: column;
    gap: 0.3rem;
    font-size: 0.8rem;
  }
}
</style>