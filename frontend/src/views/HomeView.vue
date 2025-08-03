<template>
  <div class="home">
    <NavigationBar 
      @openLogin="showLoginModal = true"
      @openRegister="showRegisterModal = true"
      :introProgress="introProgress"
      :currentSlide="currentSlide"
      @navigateToSlide="navigateToSlide"
    />
    
    <!-- Cineslider Container like feedmusic.com -->
    <div class="cineslider-container">
      <div class="cineslider-wrapper">
        <!-- Slide 1: Introduction -->
        <div 
          id="introduction" 
          class="cineslider-slide"
          :class="{ active: currentSlide === 0 }"
        >
          <IntroductionSection 
            @openLogin="showLoginModal = true" 
            @updateProgress="updateIntroProgress"
            @nextSlide="nextSlide"
          />
        </div>
        
        <!-- Slide 2: News -->
        <div 
          id="news" 
          class="cineslider-slide"
          :class="{ active: currentSlide === 1 }"
        >
          <NewsSection />
        </div>
      </div>
    </div>
    
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
    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import NavigationBar from '../components/NavigationBar.vue'
import IntroductionSection from '../components/IntroductionSection.vue'
import NewsSection from '../components/NewsSection.vue'
import LoginModal from '../components/LoginModal.vue'
import RegisterModal from '../components/RegisterModal.vue'

const showLoginModal = ref(false)
const showRegisterModal = ref(false)
const introProgress = ref(0)
const currentSlide = ref(0)
const totalSlides = 2
let isTransitioning = ref(false)

const updateIntroProgress = (progress: number) => {
  introProgress.value = progress
}

const switchToRegister = () => {
  showLoginModal.value = false
  showRegisterModal.value = true
}

const switchToLogin = () => {
  showRegisterModal.value = false
  showLoginModal.value = true
}

const navigateToSlide = (slideIndex: number) => {
  if (slideIndex >= 0 && slideIndex < totalSlides && !isTransitioning.value) {
    currentSlide.value = slideIndex
  }
}

const nextSlide = () => {
  if (currentSlide.value < totalSlides - 1 && !isTransitioning.value) {
    isTransitioning.value = true
    currentSlide.value++
    setTimeout(() => {
      isTransitioning.value = false
    }, 800)
  }
}

const prevSlide = () => {
  if (currentSlide.value > 0 && !isTransitioning.value) {
    isTransitioning.value = true
    currentSlide.value--
    setTimeout(() => {
      isTransitioning.value = false
    }, 800)
  }
}

const handleWheel = (event: WheelEvent) => {
  if (isTransitioning.value) {
    event.preventDefault()
    return
  }

  // If we're in introduction slide, let IntroductionSection handle internal navigation
  if (currentSlide.value === 0) {
    // Don't prevent default here - let IntroductionSection handle it
    return
  }
  
  // For all other slides, always use wheel for slide navigation
  event.preventDefault()
  
  if (event.deltaY > 50) {
    nextSlide()
  } else if (event.deltaY < -50) {
    prevSlide()
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (isTransitioning.value) return
  
  switch (event.key) {
    case 'ArrowDown':
    case 'PageDown':
      event.preventDefault()
      nextSlide()
      break
    case 'ArrowUp':
    case 'PageUp':
      event.preventDefault()
      prevSlide()
      break
  }
}

onMounted(() => {
  window.addEventListener('wheel', handleWheel, { passive: false })
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('wheel', handleWheel)
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.home {
  position: relative;
  overflow: hidden;
}

/* Cineslider System - inspired by feedmusic.com */
.cineslider-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.cineslider-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.cineslider-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateY(100%);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

/* First slide starts visible */
.cineslider-slide:first-child {
  opacity: 1;
  transform: translateY(0);
  z-index: 2;
}

.cineslider-slide.active {
  opacity: 1;
  transform: translateY(0);
  z-index: 2;
}

/* Ensure child components fill the slide */
.cineslider-slide > * {
  width: 100%;
  height: 100%;
}

/* Responsive */
@media (max-width: 768px) {
  .cineslider-slide {
    height: 100vh;
  }
}
</style>