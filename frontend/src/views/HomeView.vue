<template>
  <div class="home">
    <NavigationBar 
      @openLogin="showLoginModal = true"
      @openRegister="showRegisterModal = true"
      @openAdmin="showAdminPanel = true"
    />
    
    <IntroductionSection @openLogin="showLoginModal = true" />
    
    <NewsSection />
    
    <LoginModal 
      :isOpen="showLoginModal"
      @close="showLoginModal = false"
      @switchToRegister="switchToRegister"
    />
    
    <RegisterModal 
      :isOpen="showRegisterModal"
      @close="showRegisterModal = false"
      @switchToLogin="switchToLogin"
    />
    
    <AdminPanel 
      :isOpen="showAdminPanel"
      @close="showAdminPanel = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'
import IntroductionSection from '../components/IntroductionSection.vue'
import NewsSection from '../components/NewsSection.vue'
import LoginModal from '../components/LoginModal.vue'
import RegisterModal from '../components/RegisterModal.vue'
import AdminPanel from '../components/AdminPanel.vue'

const showLoginModal = ref(false)
const showRegisterModal = ref(false)
const showAdminPanel = ref(false)

const switchToRegister = () => {
  showLoginModal.value = false
  showRegisterModal.value = true
}

const switchToLogin = () => {
  showRegisterModal.value = false
  showLoginModal.value = true
}
</script>

<style scoped>
.home {
  position: relative;
}

/* No additional styles needed - AdminPanel component has its own styles */
</style>