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
          />
        </div>
        
        <!-- Slide 2: News -->
        <div 
          id="news" 
          class="cineslider-slide"
          :class="{ 'cineslider-slide-active': currentSlide === 1 }"
        >
          <NewsSection ref="newsSectionRef" />
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
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
const newsSectionRef = ref<any>()

const updateIntroProgress = (progress: number) => {
  // 只有在Introduction页面时才更新进度
  if (currentSlide.value === 0) {
    introProgress.value = progress
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
  
  // 跟踪访问状态
  if (targetIndex === 1) {
    console.log('Setting hasVisitedNews to true in localStorage')
    localStorage.setItem('hasVisitedNews', 'true')
  }
  
  // 从其他页面返回时，让进度条和文字界面自然保持一致
  // 不再强制设置进度为100%
  
  const direction = targetIndex > currentSlide.value ? 'down' : 'up'
  const duration = immediate ? 0.1 : 1.8  // 延长换页时间
  
  isTransitioning.value = true
  
  const currentSlideEl = cinesliderContainer.value?.querySelector('.cineslider-slide-active') as HTMLElement
  const targetSlideEl = cinesliderContainer.value?.querySelectorAll('.cineslider-slide')[targetIndex] as HTMLElement
  
  // 立即更新currentSlide以让导航栏响应
  const previousSlide = currentSlide.value
  currentSlide.value = targetIndex
  
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
    
    // 动画完成后重置fromNewsPage标志
    setTimeout(() => {
      isTransitioning.value = false
      
      // 如果切换到News页面，刷新新闻列表
      if (targetIndex === 1 && newsSectionRef.value) {
        console.log('Refreshing news list after slide transition')
        newsSectionRef.value.fetchNews()
      }
      
      // 清理完成
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

  // If we're in introduction slide, don't handle wheel events here
  // Let IntroductionSection handle all wheel events including page transitions
  if (currentSlide.value === 0) {
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

// Touch/Swipe navigation for mobile - 避免与IntroductionSection冲突
const initTouchNavigation = () => {
  if (!window.Hammer || !cinesliderContainer.value) return
  
  const hammer = new window.Hammer(cinesliderContainer.value)
  hammer.get('swipe').set({ direction: window.Hammer.DIRECTION_VERTICAL })
  
  hammer.on('swipeup', (e) => {
    // 如果在Introduction页面，不处理快速滑动，让IntroductionSection处理
    if (currentSlide.value === 0) {
      return
    }
    
    if (!isTransitioning.value && currentSlide.value < totalSlides - 1) {
      console.log('Touch swipe up detected, navigating to next slide')
      nextSlide()
    }
  })
  
  hammer.on('swipedown', (e) => {
    // 如果在Introduction页面，不处理快速滑动，让IntroductionSection处理
    if (currentSlide.value === 0) {
      return
    }
    
    if (!isTransitioning.value && currentSlide.value > 0) {
      console.log('Touch swipe down detected, navigating to previous slide')
      prevSlide()
    }
  })
  
  console.log('Touch navigation initialized')
}

onMounted(() => {
  window.addEventListener('wheel', handleWheel, { passive: false })
  window.addEventListener('keydown', handleKeyDown)
  
  // Initialize touch navigation for mobile devices
  nextTick(() => {
    initTouchNavigation()
  })
  
  // 开发用：按F12清除localStorage重置状态
  window.addEventListener('keydown', (e) => {
    if (e.key === 'F12') {
      localStorage.removeItem('hasVisitedNews')
      location.reload()
    }
  })
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

/* Mobile optimizations */
@media (max-width: 768px) {
  .cineslider-container {
    /* Fix for mobile viewport height issues */
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for modern browsers */
  }
  
  .cineslider-slide {
    height: 100vh;
    height: 100dvh;
    /* Prevent scroll bounce on iOS */
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: none;
  }
  
  .cineslider-wrapper {
    /* Improve touch performance */
    transform: translateZ(0);
    backface-visibility: hidden;
  }
}

/* Touch-friendly navigation hints */
@media (max-width: 768px) and (pointer: coarse) {
  .cineslider-slide {
    /* Add visual hint for swipe navigation */
    position: relative;
  }
  
  .cineslider-slide::after {
    content: '';
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 30px;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    animation: swipeHint 2s infinite;
  }
  
  @keyframes swipeHint {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.8; }
  }
}
</style>