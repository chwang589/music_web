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
    <div class="cineslider-container" ref="cinesliderContainer">
      <!-- 背景过渡层 - FeedMusic原版色彩 -->
      <div class="cineslider-shifter" ref="shifter1" :style="{ backgroundColor: '#e6e6e6' }"></div>
      <div class="cineslider-shifter" ref="shifter2" :style="{ backgroundColor: '#35017f' }"></div>
      
      <div class="cineslider-wrapper">
        <!-- Slide 1: Introduction -->
        <div 
          id="introduction" 
          class="cineslider-slide"
          :class="{ 'cineslider-slide-active': currentSlide === 0 }"
        >
          <IntroductionSection 
            @openLogin="showLoginModal = true" 
            @updateProgress="updateIntroProgress"
            @nextSlide="nextSlide"
            :initialProgress="introProgress"
          />
        </div>
        
        <!-- Slide 2: News -->
        <div 
          id="news" 
          class="cineslider-slide"
          :class="{ 'cineslider-slide-active': currentSlide === 1 }"
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
import { gsap } from 'gsap'
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

const cinesliderContainer = ref<HTMLElement>()
const shifter1 = ref<HTMLElement>()
const shifter2 = ref<HTMLElement>()

const updateIntroProgress = (progress: number) => {
  // 只有在Introduction页面时才更新进度
  if (currentSlide.value === 0) {
    introProgress.value = progress
  } else {
    // 在news页面时，introduction进度条清零
    introProgress.value = 0
  }
}

const switchToRegister = () => {
  showLoginModal.value = false
  showRegisterModal.value = true
}

const switchToLogin = () => {
  showRegisterModal.value = false
  showLoginModal.value = true
}

// FeedMusic风格的CineSlider切换效果
const slideTo = (targetIndex: number, immediate = false) => {
  if (isTransitioning.value || targetIndex === currentSlide.value) return
  if (targetIndex < 0 || targetIndex >= totalSlides) return
  
  const direction = targetIndex > currentSlide.value ? 'down' : 'up'
  const duration = immediate ? 0.1 : 1.8  // 延长换页时间
  
  isTransitioning.value = true
  
  // 立即更新进度条，不要等动画完成
  if (targetIndex === 1) {
    // 切换到news页面时，introduction进度条立即清零
    introProgress.value = 0
  } else if (targetIndex === 0) {
    // 从news回到introduction时，立即设置为95%
    introProgress.value = 95
  }
  
  const currentSlideEl = cinesliderContainer.value?.querySelector('.cineslider-slide-active') as HTMLElement
  const targetSlideEl = cinesliderContainer.value?.querySelectorAll('.cineslider-slide')[targetIndex] as HTMLElement
  
  if (!currentSlideEl || !targetSlideEl || !shifter1.value || !shifter2.value) return
  
  // 设置初始状态
  gsap.set(currentSlideEl, { zIndex: 0 })
  gsap.set([shifter1.value, shifter2.value, targetSlideEl], {
    display: 'block',
    zIndex: 1,
    y: direction === 'down' ? '100%' : '-100%'
  })
  
  // 创建动画时间轴
  const timeline = gsap.timeline()
  
  const shifterFirst = direction === 'down' ? shifter1.value : shifter2.value
  const shifterSecond = direction === 'down' ? shifter2.value : shifter1.value
  
  timeline.add([
    gsap.to(shifterFirst, {
      duration: duration * 0.8,
      y: direction === 'down' ? '-100%' : '100%',
      ease: 'power2.out'
    }),
    gsap.to(shifterSecond, {
      duration: duration * 0.8,
      y: direction === 'down' ? '-100%' : '100%',
      ease: 'power2.out',
      delay: duration * 0.3
    }),
    gsap.to(targetSlideEl, {
      duration: duration * 0.8,
      y: '0%',
      ease: 'power2.out',
      delay: duration * 0.3
    })
  ])
  
  timeline.eventCallback('onComplete', () => {
    // 清理状态
    gsap.set([shifter1.value, shifter2.value, currentSlideEl], { display: 'none' })
    currentSlide.value = targetIndex
    
    setTimeout(() => {
      isTransitioning.value = false
    }, 100)
  })
}

const navigateToSlide = (slideIndex: number) => {
  slideTo(slideIndex)
}

const nextSlide = () => {
  if (currentSlide.value < totalSlides - 1) {
    slideTo(currentSlide.value + 1)
  }
}

const prevSlide = () => {
  if (currentSlide.value > 0) {
    slideTo(currentSlide.value - 1)
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
  
  // If we're in news slide (currentSlide === 1)
  if (currentSlide.value === 1) {
    // Allow scrolling back to introduction when scrolling up and at top of news page
    if (event.deltaY < -50) {
      const newsContainer = document.querySelector('.news-section .container') as HTMLElement
      if (newsContainer && newsContainer.scrollTop <= 0) {
        event.preventDefault()
        prevSlide()
        return
      }
    }
    // Allow normal scrolling within news page - don't prevent default
    return
  }
  
  // For any other future slides, allow wheel navigation
  event.preventDefault()
  
  if (event.deltaY > 50) {
    nextSlide()
  } else if (event.deltaY < -50) {
    prevSlide()
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (isTransitioning.value) return
  
  // If we're in news slide, only allow going back to introduction
  if (currentSlide.value === 1) {
    switch (event.key) {
      case 'ArrowUp':
      case 'PageUp':
        event.preventDefault()
        prevSlide()
        break
    }
    return
  }
  
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

/* FeedMusic CineSlider System */
.cineslider-container {
  position: relative;
  width: 100vw;
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
  height: 100%;
  display: none;
  z-index: 0;
}

.cineslider-slide-active {
  display: block;
  z-index: 1;
}

.cineslider-shifter {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  display: none;
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