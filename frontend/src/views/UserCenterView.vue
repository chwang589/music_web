<template>
  <div class="user-center-view">
    <div class="user-center-header">
      <div class="header-container">
        <div class="brand">
          <h1>NeuraFlow</h1>
          <span class="subtitle">User Center</span>
        </div>
        <div class="header-actions">
          <button @click="goHome" class="back-btn">
            <i class="icon-back"></i>
            Back to Home
          </button>
          <button @click="logout" class="logout-btn">
            <i class="icon-logout"></i>
            Logout
          </button>
        </div>
      </div>
    </div>

    <div class="user-center-content">
      <UserCenter :isOpen="true" @close="() => {}" :isFullPage="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import UserCenter from '../components/UserCenter.vue'

const router = useRouter()
const authStore = useAuthStore()

const goHome = () => {
  router.push('/')
}

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.user-center-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.user-center-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand h1 {
  color: white;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.back-btn, .logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.logout-btn {
  background: rgba(220, 53, 69, 0.8);
  color: white;
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 1);
  transform: translateY(-1px);
}

.icon-back::before {
  content: '←';
  font-size: 1.1rem;
}

.icon-logout::before {
  content: '⏻';
  font-size: 1rem;
}

.user-center-content {
  padding: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .brand {
    text-align: center;
  }

  .brand h1 {
    font-size: 1.5rem;
  }

  .header-actions {
    width: 100%;
    justify-content: center;
  }

  .back-btn, .logout-btn {
    flex: 1;
    justify-content: center;
    padding: 0.75rem 1rem;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0.75rem;
  }

  .brand h1 {
    font-size: 1.3rem;
  }

  .subtitle {
    font-size: 0.8rem;
  }

  .header-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .back-btn, .logout-btn {
    width: 100%;
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}
</style>