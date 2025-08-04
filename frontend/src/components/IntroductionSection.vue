<template>
  <section id="introduction" class="introduction-section">
    <!-- Video Background Layer -->
    <div class="videobg-container">
      <video 
        ref="videoBackground"
        class="video-background" 
        autoplay 
        loop 
        muted 
        playsinline
        preload="auto"
      >
        <source src="/videos/intro.mp4" type="video/mp4">
      </video>
      <div class="videobg-shadow"></div>
    </div>
    
    <!-- 装饰边框 -->
    <div class="border" data-position="top"></div>
    <div class="border" data-position="right"></div>
    <div class="border" data-position="left"></div>
    <div class="border" data-position="bottom"></div>

    <!-- 左上角Logo -->
    <div class="brand-logo" ref="brandLogo">
      <div class="logo-icon">N</div>
    </div>

    <!-- 初始加载Logo动画 -->
    <div class="intro-loader" ref="introLoader">
      <div class="loader-logo">
        <div class="loader-icon">N</div>
        <div class="loader-text">NeuraFlow</div>
        <div class="loader-subtitle">AI Music News Platform</div>
      </div>
    </div>

    <!-- 介绍段落 - 左下角小字体 -->
    <div class="intro-paragraph" ref="introParagraph">
      <p>NeuraFlow is an intelligent AI music news platform, using advanced neural networks and content algorithms to deliver personalized music insights and trending news.</p>
      <p>NeuraFlow facilitates seamless discovery of music content, connecting artists, fans, and industry professionals in a <b>trusted</b>, dynamic, and innovative digital ecosystem.</p>
    </div>

    <!-- 星球大战滚动文字 - 保留滚动效果但不响应用户交互 -->
    <div class="starwars-container" ref="starwarsContainer">
      <div class="starwars-wrapper" ref="starwarsWrapper">
        <p>When you want something,</p>
        <p>all the universe conspires</p>
        <p>in helping you to achieve it.</p>
        <p class="author-signature">Paulo Coelho</p>
        <p><br><br></p>
        <p><br><br></p>
        <p>NeuraFlow is that conspiracy:</p>
        <p>the conspiracy of music.</p>
        <p><br><br></p>
        <p><br><br></p>
        <p>Music is the single</p>
        <p>most important ingredient</p>
        <p>that connects human souls.</p>
        <p><br><br></p>
        <p><br><br></p>
        <p>Industry analysts</p>
        <p>and music streaming platforms</p>
        <p>forecast the global music market</p>
        <p>to be worth over</p>
        <p><strong>25 billion dollars</strong></p>
        <p><strong>by 2025.</strong></p>
        <p><br><br></p>
        <p><br><br></p>
        <p>The key to growth</p>
        <p>in this industry</p>
        <p>is <strong>innovation</strong>.</p>
        <p><br><br></p>
        <p><br><br></p>
        <p style="white-space: normal;"><strong>NeuraFlow</strong> is a digital platform of <strong>musical discovery</strong></p>
      </div>
    </div>
    
    <!-- Scroll Down 按钮 -->
    <a href="#" class="scroll-down" @click.prevent="nextSlide">
      <i class="icon"></i>
      <span>SCROLL DOWN</span>
    </a>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { gsap } from 'gsap'
import Hammer from 'hammerjs'

// 不需要props了，直接从localStorage读取

const emit = defineEmits(['openLogin', 'updateProgress', 'nextSlide'])

const videoBackground = ref<HTMLVideoElement>()
const starwarsContainer = ref<HTMLDivElement>()
const starwarsWrapper = ref<HTMLDivElement>()
const introParagraph = ref<HTMLDivElement>()
const brandLogo = ref<HTMLDivElement>()
const introLoader = ref<HTMLDivElement>()
let starwarsScroll: any = null
let isScrolling = false
let hammerManager: any = null
let introAnimationComplete = false

const updateProgress = (progress: number) => {
  emit('updateProgress', progress)
}

const scrollToNext = () => {
  emit('nextSlide')
}

// FeedMusic原版StarWars滚动插件 - 完全重写
class StarWarsScroll {
  container: HTMLElement
  options: any
  wrapper: HTMLElement
  sentences: NodeListOf<HTMLElement>
  isLocked: boolean
  scrollProgress: number
  maxScrollHeight: number
  timeline: any
  kinetic: any
  
  constructor(container: HTMLElement, options: any = {}) {
    this.container = container
    this.options = Object.assign({
      debug: false,
      offsetSentenceDistance: 100,
      offsetScale: 0.25,
      offsetAlpha: 0.25,
      stagger: 0.5,
      duration: 1,
      mousewheelThrottle: 10,
      lock: false,
      onInit: () => {},
      onProgress: () => {},
      onComplete: () => {},
      onStart: () => {},
      onReverse: () => {}
    }, options)
    
    this.wrapper = container.querySelector('.starwars-wrapper') as HTMLElement
    this.sentences = this.wrapper.querySelectorAll('p')
    this.isLocked = this.options.lock
    this.scrollProgress = 0
    this.maxScrollHeight = 0
    this.timeline = gsap.timeline({ 
      paused: true, 
      ease: 'none',
      onStart: () => this.options.onStart(),
      onComplete: () => this.options.onComplete(),
      onReverseComplete: () => this.options.onReverse(),
      onUpdate: () => this.options.onProgress(this.timeline.progress())
    })
    
    this.init()
  }
  
  init() {
    this.calculateScrollHeight()
    this.setupSentences()
    this.createSequence()
    this.bindEvents()
    this.options.onInit()
    this.log('StarWars scroll initialized')
  }
  
  calculateScrollHeight() {
    let totalHeight = 0
    this.sentences.forEach((sentence) => {
      totalHeight += sentence.offsetHeight + parseInt(getComputedStyle(sentence).marginBottom.replace('px', ''), 10)
    })
    this.maxScrollHeight = totalHeight + window.innerHeight
    
    // 为wrapper设置动态高度以确保有足够的滚动空间
    if (this.wrapper) {
      this.wrapper.style.height = this.maxScrollHeight + 'px'
    }
    
    this.log(`Calculated scroll height: ${this.maxScrollHeight}`)
  }
  
  setupSentences() {
    this.sentences.forEach((sentence, index) => {
      // 调整初始位置，确保四行文字都在屏幕可见区域
      const baseOffset = 10 // 从10%位置开始，给四行文字适当间距
      
      // Paulo Coelho使用更小的间距，让它更接近第三行
      let distanceMultiplier
      if (index === 3) {
        distanceMultiplier = index * (this.options.offsetSentenceDistance * 0.6) // Paulo Coelho间距缩小40%
      } else {
        distanceMultiplier = index * this.options.offsetSentenceDistance
      }
      
      const y = baseOffset + distanceMultiplier
      const scale = 1 - this.options.offsetScale * index
      const alpha = Math.max(0, 1 - this.options.offsetAlpha * index)
      
      gsap.set(sentence, {
        y: y + '%',
        scale: scale,
        opacity: alpha,
        transformOrigin: 'center center',
        force3D: true,
        backfaceVisibility: 'hidden'
      })
    })
  }
  
  createSequence() {
    const maxSteps = Math.round(1 / this.options.offsetAlpha)
    const baseOffset = 10 // 与setupSentences中的baseOffset保持一致
    
    this.sentences.forEach((sentence, index) => {
      let step = 0
      let currentIndex = index
      let staggerDelay = this.options.stagger * index
      
      // 向上滚动阶段
      for (step = 0; step < currentIndex; step++) {
        const targetY = baseOffset + this.options.offsetSentenceDistance * (currentIndex - step - 1)
        this.timeline.to(sentence, {
          duration: this.options.duration,
          y: targetY + '%',
          opacity: 1 - this.options.offsetAlpha * (currentIndex - step - 1),
          scale: 1 - this.options.offsetScale * (currentIndex - step - 1),
          ease: 'none',
          force3D: true
        }, staggerDelay)
        staggerDelay += this.options.duration
      }
      
      // 继续向上消失阶段 - 最后一句不完全消失，保持在100%可见
      if (index < this.sentences.length - 1) {
        for (step = 0; step < maxSteps; step++) {
          const targetY = baseOffset - this.options.offsetSentenceDistance * (step + 1)
          this.timeline.to(sentence, {
            duration: this.options.duration,
            y: targetY + '%',
            opacity: 1 - this.options.offsetAlpha * (step + 1),
            scale: 1 + this.options.offsetScale * (step + 1),
            ease: 'none',
            force3D: true
          }, staggerDelay)
          staggerDelay += this.options.duration
        }
      } else {
        // 最后一句话在100%时保持可见状态
        this.timeline.to(sentence, {
          duration: this.options.duration,
          y: baseOffset + '%',
          opacity: 1,
          scale: 1,
          ease: 'none',
          force3D: true
        }, staggerDelay)
      }
    })
  }
  
  bindEvents() {
    let wheelTimeout: any = null
    
    // 鼠标滚轮控制 - 模拟FeedMusic原版的节流处理
    const handleWheel = (e: WheelEvent) => {
      e.preventDefault()
      
      if (this.isLocked) return
      
      // 清除上一个定时器
      if (wheelTimeout) {
        clearTimeout(wheelTimeout)
      }
      
      // 节流处理
      wheelTimeout = setTimeout(() => {
        const delta = e.deltaY > 0 ? 0.01 : -0.01
        this.scrollProgress = Math.max(0, Math.min(1, this.scrollProgress + delta))
        this.timeline.progress(this.scrollProgress)
        
        // 触发进度事件
        this.trigger('progress', this.scrollProgress)
        
        // 检查是否完成 - 移除页面切换逻辑
        if (this.scrollProgress >= 1) {
          this.trigger('complete')
        } else if (this.scrollProgress <= 0) {
          this.trigger('reverse')
        }
      }, this.options.mousewheelThrottle)
    }
    
    this.container.addEventListener('wheel', handleWheel, { passive: false })
    
    // 存储事件处理器以便清理
    this.container._wheelHandler = handleWheel
  }
  
  // 触摸手势支持
  initTouch() {
    if (!window.Hammer) return
    
    const hammer = new Hammer(this.container)
    hammer.get('pan').set({ direction: Hammer.DIRECTION_VERTICAL })
    
    let startProgress = 0
    
    hammer.on('panstart', () => {
      startProgress = this.scrollProgress
    })
    
    hammer.on('panmove', (e) => {
      if (this.isLocked) return
      
      const delta = e.deltaY / window.innerHeight
      this.scrollProgress = Math.max(0, Math.min(1, startProgress + delta))
      this.timeline.progress(this.scrollProgress)
      this.trigger('progress', this.scrollProgress)
    })
    
    hammer.on('panend', (e) => {
      // 根据滑动速度决定是否自动完成滚动
      if (Math.abs(e.velocityY) > 0.3) {
        const targetProgress = e.velocityY > 0 ? 1 : 0
        gsap.to(this, {
          duration: 0.5,
          scrollProgress: targetProgress,
          ease: 'power2.out',
          onUpdate: () => {
            this.timeline.progress(this.scrollProgress)
            this.trigger('progress', this.scrollProgress)
          },
          onComplete: () => {
            if (this.scrollProgress >= 1) {
              this.trigger('complete')
            } else if (this.scrollProgress <= 0) {
              this.trigger('reverse')
            }
          }
        })
      }
    })
    
    this.hammerManager = hammer
  }
  
  lock() {
    this.isLocked = true
  }
  
  unlock() {
    this.isLocked = false
  }
  
  reset() {
    this.scrollProgress = 0
    this.timeline.progress(0)
  }
  
  destroy() {
    if (this.container._wheelHandler) {
      this.container.removeEventListener('wheel', this.container._wheelHandler)
    }
    if (this.hammerManager) {
      this.hammerManager.destroy()
    }
    this.timeline.kill()
  }
  
  trigger(eventName: string, ...args: any[]) {
    const event = new CustomEvent(eventName, { detail: args })
    this.container.dispatchEvent(event)
    this.log(`Event triggered: ${eventName}`)
  }
  
  on(eventName: string, callback: (e: any) => void) {
    this.container.addEventListener(eventName, callback)
  }
  
  log(message: string) {
    if (this.options.debug && window.console && window.console.log) {
      console.log(`StarWarsScroll: ${message}`)
    }
  }
}

const nextSlide = () => {
  if (isScrolling) return
  isScrolling = true
  
  setTimeout(() => {
    scrollToNext()
    isScrolling = false
  }, 300)
}

const handleWheel = (event: WheelEvent) => {
  // 如果滚动向下且StarWars动画接近完成(90%以上)，则准备切换到下一页
  if (event.deltaY > 0 && starwarsScroll && starwarsScroll.scrollProgress > 0.9) {
    event.preventDefault()
    // 立即触发页面切换，让导航栏先响应
    scrollToNext()
  }
}

const initVideoBackground = () => {
  if (!videoBackground.value) return
  
  // 确保视频静音自动播放
  videoBackground.value.muted = true
  videoBackground.value.playsInline = true
  
  // 处理视频加载和播放
  videoBackground.value.addEventListener('loadeddata', () => {
    videoBackground.value?.play().catch((error) => {
      console.warn('Video autoplay failed:', error)
    })
  })
  
  // 处理视频错误
  videoBackground.value.addEventListener('error', (error) => {
    console.warn('Video failed to load:', error)
  })
}

const initStarWarsScroll = () => {
  if (!starwarsContainer.value) return
  
  // 初始化StarWars滚动 - 保留原版交互但不切换页面
  starwarsScroll = new StarWarsScroll(starwarsContainer.value, {
    debug: false,
    offsetSentenceDistance: 60, // 缩小整体行间距
    offsetScale: 0.25, // 恢复原版缩放
    offsetAlpha: 0.2, // 适当调整透明度，让Paulo Coelho可见
    stagger: 0.5,
    duration: 1,
    mousewheelThrottle: 10,
    onInit: function() {
      // 初始化完成后显示StarWars容器
      if (starwarsContainer.value) {
        starwarsContainer.value.style.opacity = '1'
      }
      
      // 检查是否是第一次访问
      const hasVisitedNews = localStorage.getItem('hasVisitedNews') === 'true'
      console.log('=== StarWars Init Debug ===')
      console.log('hasVisitedNews from localStorage:', hasVisitedNews)
      
      // 设置初始化标志，防止onProgress覆盖
      this.isInitializing = true
      
      // 简化初始化逻辑，只设置进度，文字状态由HomeView处理
      if (!hasVisitedNews) {
        // 第一次访问，从0%开始
        console.log('First visit - setting to 0%')
        this.scrollProgress = 0
        updateProgress(0)
      } else {
        // 从其他页面返回，设置为100%（文字状态由HomeView处理）
        console.log('Return visit - setting progress to 100%')
        this.scrollProgress = 1.0
        updateProgress(100)
        
        // 隐藏介绍文字
        if (introParagraph.value) {
          gsap.set(introParagraph.value, { opacity: 0 })
        }
      }
      
      // 短暂延迟后允许onProgress正常工作
      const self = this
      setTimeout(() => {
        self.isInitializing = false
        console.log('StarWars initialization completed')
      }, 100)
    },
    onProgress: function(progress: number) {
      // 避免在初始化时覆盖手动设置的进度
      if (!this.isInitializing) {
        updateProgress(progress * 100)
      }
      
      // 控制介绍文字的显示/隐藏 - 与进度条保持一致
      if (introParagraph.value) {
        const hasVisitedNews = localStorage.getItem('hasVisitedNews') === 'true'
        let shouldShow
        
        if (hasVisitedNews) {
          // 从其他页面返回时，100%时文字已经滚动完成所以隐藏，向下滚动时再次显示
          shouldShow = progress < 0.99
        } else {
          // 第一次访问时，初始0%时显示，开始滚动后逐渐隐藏
          shouldShow = progress <= 0.01
        }
        
        const currentOpacity = parseFloat(window.getComputedStyle(introParagraph.value).opacity)
        
        if (shouldShow && currentOpacity < 1) {
          gsap.to(introParagraph.value, {
            duration: 0.5,
            opacity: 1,
            ease: 'power2.out'
          })
        } else if (!shouldShow && currentOpacity > 0) {
          gsap.to(introParagraph.value, {
            duration: 0.5,
            opacity: 0,
            ease: 'power2.out'
          })
        }
      }
    },
    onComplete: function() {
      // 动画完成后立即切换到下一页
      scrollToNext()
    },
    onStart: function() {
      // 开始滚动时的处理
      console.log('StarWars scroll started')
    },
    onReverse: function() {
      // 倒序滚动时的处理
      console.log('StarWars scroll reversed')
    }
  })
  
  // 初始化触摸支持
  starwarsScroll.initTouch()
}

const initIntroAnimation = () => {
  // 3秒后开始淡出加载动画
  setTimeout(() => {
    if (introLoader.value) {
      introLoader.value.classList.add('fade-out')
      
      // 1秒后完全隐藏加载器并初始化其他组件
      setTimeout(() => {
        if (introLoader.value) {
          introLoader.value.style.display = 'none'
        }
        introAnimationComplete = true
        
        // 初始化视频背景和StarWars滚动
        initVideoBackground()
        initStarWarsScroll()
      }, 1000)
    }
  }, 3000)
}

onMounted(() => {
  nextTick(() => {
    // 检查是否是第一次访问
    const hasVisitedNews = localStorage.getItem('hasVisitedNews') === 'true'
    
    console.log('=== IntroductionSection onMounted ===')
    console.log('hasVisitedNews in onMounted:', hasVisitedNews)
    
    if (!hasVisitedNews) {
      // 第一次访问，播放完整的loading动画
      console.log('First visit - starting intro animation')
      initIntroAnimation()
    } else {
      // 从其他页面返回，跳过loading动画
      console.log('Return visit - skipping intro animation, initializing directly')
      if (introLoader.value) {
        introLoader.value.style.display = 'none'
      }
      introAnimationComplete = true
      // 立即初始化组件
      initVideoBackground()
      initStarWarsScroll()
    }
  })

  // Add wheel event listener for page navigation
  window.addEventListener('wheel', handleWheel, { passive: false })
})

onUnmounted(() => {
  window.removeEventListener('wheel', handleWheel)
  document.removeEventListener('wheel', handleWheel)
  if (starwarsScroll) {
    starwarsScroll.destroy()
  }
})
</script>

<style scoped>
/* 基础样式 */
.introduction-section {
  position: relative;
  height: 100vh;
  overflow: hidden;
  font-family: 'Ubuntu', sans-serif;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

/* 视频背景容器 */
.videobg-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.video-background {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  opacity: 0.3;
}

.videobg-shadow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
}

/* 装饰边框 */
.border {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  z-index: 10;
}

.border[data-position="top"] {
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
}

.border[data-position="right"] {
  top: 0;
  right: 0;
  bottom: 0;
  width: 1px;
}

.border[data-position="bottom"] {
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
}

.border[data-position="left"] {
  top: 0;
  left: 0;
  bottom: 0;
  width: 1px;
}

/* 左上角品牌Logo */
.brand-logo {
  position: absolute;
  top: 30px;
  left: 30px;
  z-index: 50;
  opacity: 0.9;
  transition: all 0.3s ease;
}

.brand-logo:hover {
  opacity: 1;
  transform: translateY(-2px);
}

.brand-logo .logo-icon {
  font-size: 48px;
  font-weight: 900;
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
  font-family: 'Helvetica Neue', 'Helvetica', sans-serif;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
  transform: skew(-15deg);
}

/* 初始加载Logo动画 */
.intro-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 1;
  transition: all 1s ease-out;
}

.intro-loader.fade-out {
  opacity: 0;
  pointer-events: none;
}

.loader-logo {
  text-align: center;
  animation: logoEntry 2s ease-out forwards;
}

.loader-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: 700;
  color: white;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
  margin: 0 auto 20px;
  animation: iconPulse 2s ease-in-out infinite alternate;
}

.loader-text {
  font-size: 36px;
  font-weight: 600;
  color: white;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  background: linear-gradient(135deg, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
  animation: textSlideUp 1s ease-out 0.5s both;
}

.loader-subtitle {
  font-size: 16px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 2px;
  text-transform: uppercase;
  animation: textSlideUp 1s ease-out 0.8s both;
}

@keyframes logoEntry {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes iconPulse {
  0% {
    transform: scale(1);
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
  }
  100% {
    transform: scale(1.05);
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
  }
}

@keyframes textSlideUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 介绍段落 - 左下角小字体 */
.intro-paragraph {
  position: absolute;
  bottom: 20px;
  left: 20px;
  max-width: 350px;
  z-index: 20;
  opacity: 1;
  will-change: opacity, transform;
  backface-visibility: hidden;
}

.intro-paragraph p {
  font-size: 12px;
  line-height: 1.4;
  margin-bottom: 6px;
  color: #fff;
  font-weight: 300;
  opacity: 0.8;
}

/* 星球大战滚动文字容器 - 大幅扩大显示区域 */
.starwars-container {
  position: absolute;
  top: 30%; /* 向上移动容器 */
  left: 0;
  width: 100%;
  height: 200%;
  overflow: hidden;
  z-index: 15;
  perspective: 1000px;
  transform-style: preserve-3d;
  opacity: 0; /* 初始隐藏，等待初始化完成 */
  transition: opacity 0.5s ease;
}

.starwars-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400%; /* 增加wrapper高度以容纳所有四行文字 */
  transform-style: preserve-3d;
  will-change: transform;
  backface-visibility: hidden;
}

.starwars-wrapper p {
  position: absolute;
  left: 50%;
  font-size: 62px; /* 进一步增大字体 */
  text-align: center;
  white-space: nowrap;
  font-weight: 400;
  font-style: italic;
  letter-spacing: 2px;
  width: 1400px; /* 增大宽度适应更大的字体 */
  margin-left: -700px;
  transform-origin: center center;
  color: #fff;
  opacity: 1;
  will-change: transform, opacity, scale;
  backface-visibility: hidden;
  transform: translateZ(0);
  /* 简化文字效果 */
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
  font-family: 'Helvetica Neue', 'Helvetica', sans-serif;
}

.starwars-wrapper p strong {
  color: #fff;
  font-weight: 700;
  text-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
}

.starwars-wrapper p.author-signature {
  color: #fff;
  font-weight: 900; /* 最大粗细 */
  font-style: italic;
  font-size: 78px; /* 进一步增大Paulo Coelho字体 */
  font-family: 'Helvetica Neue Black', 'Arial Black', 'Helvetica Neue', sans-serif; /* 更粗的字体 */
  background: linear-gradient(135deg, #ffffff, #f0f0f0, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 
    0 0 25px rgba(255, 255, 255, 0.6),
    0 0 50px rgba(255, 255, 255, 0.4);
  letter-spacing: 5px; /* 适当调整字母间距 */
  white-space: nowrap;
  width: 1400px; /* 增大宽度适应更大的字体 */
  margin-left: -700px;
  text-align: center;
  position: absolute;
  left: 50%;
  transform-origin: center center;
  will-change: transform, opacity, scale;
  backface-visibility: hidden;
  transform: translateZ(0);
  filter: drop-shadow(0 4px 8px rgba(255, 255, 255, 0.5));
  font-stretch: expanded; /* 拉伸字体让它看起来更胖 */
}

/* Scroll Down 按钮 - 与鼠标重合在中心位置 */
.scroll-down {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  opacity: 0.8;
  text-align: center;
  cursor: pointer;
  z-index: 100;
  transition: all 0.3s ease;
  font-family: 'Helvetica Neue', 'Helvetica', sans-serif;
  font-style: italic;
  font-weight: 500;
}

.scroll-down:hover {
  opacity: 0; /* 点击时文字消失 */
  transform: translateX(-50%) translateY(-2px);
}

.scroll-down:active {
  opacity: 0; /* 点击时完全透明 */
}

.scroll-down .icon {
  display: block;
  width: 24px;
  height: 40px;
  margin: 0 auto 8px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  position: relative;
  background: transparent;
}

/* FeedMusic精确复制的鼠标滚轮指示器 */
.scroll-down .icon::before {
  content: '';
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
  animation: scroll-indicator 2s ease-in-out infinite;
}

.scroll-down span {
  display: block;
  text-transform: lowercase;
  letter-spacing: 1px;
  font-weight: 300;
}

/* 滚轮指示器动画 */
@keyframes scroll-indicator {
  0% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  50% {
    opacity: 0.3;
    transform: translateX(-50%) translateY(8px);
  }
  100% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Paulo Coelho 艺术字闪烁动画 */
@keyframes shimmer {
  0% {
    background-position: -200% center;
  }
  100% {
    background-position: 200% center;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .intro-paragraph {
    left: 20px;
    right: 20px;
    max-width: none;
    top: 100px;
  }
  
  .starwars-wrapper p {
    font-size: 18px;
    width: 90%;
    margin-left: -45%;
    white-space: normal;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .starwars-wrapper p {
    font-size: 16px;
    max-width: 250px;
  }
  
  .intro-paragraph p {
    font-size: 11px;
  }
}
</style>