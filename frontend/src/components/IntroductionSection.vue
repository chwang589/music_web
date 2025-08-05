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
      // 参考桌面端，初始只显示前2-3行文字，后面的文字透明度为0
      const baseOffset = 15 // 稍微向下一点开始
      
      // Paulo Coelho使用更小的间距，让它更接近第三行
      let distanceMultiplier
      if (index === 3) {
        distanceMultiplier = index * (this.options.offsetSentenceDistance * 0.6) // Paulo Coelho间距缩小40%
      } else {
        distanceMultiplier = index * this.options.offsetSentenceDistance
      }
      
      const y = baseOffset + distanceMultiplier
      const scale = 1 - this.options.offsetScale * index
      // 恢复初始透明度：所有文字都有适当的可见度
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
        const delta = e.deltaY > 0 ? 0.01 : -0.01 // 恢复网页端正常速度
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
      }, this.options.mousewheelThrottle) // 恢复网页端正常节流时间
    }
    
    this.container.addEventListener('wheel', handleWheel, { passive: false })
    
    // 存储事件处理器以便清理
    this.container._wheelHandler = handleWheel
  }
  
  // 触摸手势支持 - 修复移动端导航问题
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
      
      // 修正滑动方向：向上滑动（deltaY为负值）文字向下滚动（减少progress）
      // 向下滑动（deltaY为正值）文字向上滚动（增加progress）
      const delta = -e.deltaY / (window.innerHeight * 4) // 调整灵敏度，优化手感
      this.scrollProgress = Math.max(0, Math.min(1, startProgress + delta))
      this.timeline.progress(this.scrollProgress)
      this.trigger('progress', this.scrollProgress)
    })
    
    hammer.on('panend', (e) => {
      // 简化触摸结束逻辑，只处理页面切换，不做额外的惯性动画
      if (this.scrollProgress >= 0.95 && e.velocityY > 0.5) {
        // 滚动已经接近完成，且向下滑动速度足够快，触发页面切换
        this.trigger('complete')
      } else if (this.scrollProgress <= 0.05 && e.velocityY < -0.5) {
        // 滚动在开始位置，且向上滑动速度足够快
        this.trigger('reverse')
      }
      // 其他情况不做任何额外动画，避免粘连感
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
  // 对于其他滚动，让StarWars类处理（不阻止默认行为）
}

const initVideoBackground = () => {
  if (!videoBackground.value) return
  
  // 移动端检测和优化
  const isMobile = window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  
  if (isMobile) {
    // 移动端使用静态背景图片替代视频
    console.log('Mobile device detected, using static background instead of video')
    const videoContainer = videoBackground.value.parentElement
    if (videoContainer) {
      // 使用1.png作为移动端背景图片
      videoContainer.style.background = `url('/1.png')`
      videoContainer.style.backgroundSize = 'cover' // 覆盖整个容器
      videoContainer.style.backgroundPosition = 'center center' // 居中显示
      videoContainer.style.backgroundRepeat = 'no-repeat' // 不重复
      videoContainer.style.backgroundAttachment = 'fixed' // 固定背景，增强视觉效果
      
      // 添加轻微的叠加效果以确保文字可读性
      const overlay = document.createElement('div')
      overlay.style.position = 'absolute'
      overlay.style.top = '0'
      overlay.style.left = '0'
      overlay.style.width = '100%'
      overlay.style.height = '100%'
      overlay.style.background = 'rgba(26, 40, 68, 0.2)' // 轻微的蓝色叠加
      overlay.style.pointerEvents = 'none' // 不阻挡交互
      videoContainer.appendChild(overlay)
      
      // 隐藏视频元素
      videoBackground.value.style.display = 'none'
    }
    return
  }
  
  // 桌面端正常播放视频
  videoBackground.value.muted = true
  videoBackground.value.playsInline = true
  
  // 处理视频加载和播放
  videoBackground.value.addEventListener('loadeddata', () => {
    videoBackground.value?.play().catch((error) => {
      console.warn('Video autoplay failed, fallback to static background:', error)
      // 视频播放失败时降级为静态背景
      const videoContainer = videoBackground.value?.parentElement
      if (videoContainer) {
        videoContainer.style.background = `url('/1.png')`
        videoContainer.style.backgroundSize = 'cover'
        videoContainer.style.backgroundPosition = 'center center'
        videoContainer.style.backgroundRepeat = 'no-repeat'
        videoBackground.value!.style.display = 'none'
      }
    })
  })
  
  // 处理视频错误
  videoBackground.value.addEventListener('error', (error) => {
    console.warn('Video failed to load, using fallback background:', error)
    // 视频加载失败时降级为静态背景
    const videoContainer = videoBackground.value?.parentElement
    if (videoContainer) {
      videoContainer.style.background = `url('/1.png')`
      videoContainer.style.backgroundSize = 'cover'
      videoContainer.style.backgroundPosition = 'center center'
      videoContainer.style.backgroundRepeat = 'no-repeat'
      videoBackground.value!.style.display = 'none'
    }
  })
}

const initStarWarsScroll = () => {
  if (!starwarsContainer.value) return
  
  // 初始化StarWars滚动 - 保留原版交互但不切换页面
  starwarsScroll = new StarWarsScroll(starwarsContainer.value, {
    debug: false,
    offsetSentenceDistance: 60, // 恢复原来的行间距
    offsetScale: 0.25, // 恢复原来的缩放效果
    offsetAlpha: 0.2, // 恢复原来的透明度设置
    stagger: 0.5,
    duration: 1,
    mousewheelThrottle: 10,
    onInit: function() {
      // 初始化完成后显示StarWars容器
      if (starwarsContainer.value) {
        starwarsContainer.value.style.opacity = '1'
      }
      
      // 简化逻辑：始终从0%开始，让进度条和文字界面自然保持一致
      console.log('StarWars initialized - starting from 0%')
      this.scrollProgress = 0
      updateProgress(0)
      if (this.timeline) {
        this.timeline.progress(0)
      }
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
      console.log('StarWars animation completed, switching to next slide')
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

  // 添加页面切换的wheel事件监听器
  // 这个监听器专门处理从StarWars滚动到News页面的切换
  window.addEventListener('wheel', handleWheel, { passive: false })
})

onUnmounted(() => {
  // 清理StarWars滚动实例
  if (starwarsScroll) {
    starwarsScroll.destroy()
  }
  
  // 清理wheel事件监听器
  window.removeEventListener('wheel', handleWheel)
})
</script>

<style scoped>
/* 基础样式 */
.introduction-section {
  position: relative;
  height: 100vh;
  overflow: hidden;
  font-family: 'Ubuntu', sans-serif;
  background: linear-gradient(135deg, #1a2844 0%, #2d3b5f 100%);
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
  top: 20px;
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
  background: linear-gradient(135deg, #1a2844 0%, #2d3b5f 100%);
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
  background: linear-gradient(135deg, #7896dc, #8aa6ee);
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
  left: 2%;
  width: 96%;
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
  font-size: 62px; /* 恢复桌面端原始字体大小 */
  text-align: center;
  white-space: normal; /* 允许换行 */
  font-weight: 400;
  font-style: italic;
  letter-spacing: 2px; /* 桌面端字母间距 */
  line-height: 1.4; /* 桌面端行间距 */
  width: 80%; /* 限制宽度让长文字换行 */
  margin-left: -40%; /* 居中偏移 */
  transform-origin: center center;
  color: #fff;
  opacity: 1;
  will-change: transform, opacity, scale;
  backface-visibility: hidden;
  transform: translateZ(0);
  /* 简化文字效果 */
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
  font-family: 'Helvetica Neue', 'Helvetica', sans-serif;
  line-height: 1.2; /* 调整行高适应换行 */
  word-wrap: break-word; /* 强制长单词换行 */
  hyphens: auto; /* 启用连字符换行 */
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
  white-space: nowrap; /* Paulo Coelho保持不换行 */
  width: 90%; /* 稍微限制宽度 */
  left: 50%;
  margin-left: -45%; /* 居中偏移 */
  text-align: center;
  position: absolute;
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
  bottom: 120px;
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
  opacity: 1;
  transform: translateX(-50%) translateY(-2px);
}

.scroll-down:hover span {
  opacity: 0; /* hover时文字消失 */
}

.scroll-down:hover .icon {
  border-color: rgba(255, 255, 255, 1); /* hover时鼠标图标变白 */
}

.scroll-down:hover .icon::before {
  background: rgba(255, 255, 255, 1); /* hover时滚动点变白 */
}

.scroll-down:active {
  opacity: 1;
}

.scroll-down:active span {
  opacity: 0; /* 点击时文字消失 */
}

.scroll-down:active .icon {
  border-color: rgba(255, 255, 255, 1); /* 点击时鼠标图标变白 */
}

.scroll-down:active .icon::before {
  background: rgba(255, 255, 255, 1); /* 点击时滚动点变白 */
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
  transition: border-color 0.3s ease; /* 添加边框颜色动画 */
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
  transition: background 0.3s ease; /* 添加滚动点颜色动画 */
}

.scroll-down span {
  display: block;
  text-transform: uppercase; /* 保持大写 */
  letter-spacing: 1px;
  font-weight: 300;
  transition: opacity 0.3s ease; /* 添加文字淡入淡出动画 */
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
  /* 移动端隐藏介绍文字 */
  .intro-paragraph {
    display: none;
  }
  
  .starwars-wrapper p {
    font-size: 20px; /* 移动端更小字体 */
    width: 90%; /* 限制宽度让文字换行 */
    left: 50%; /* 居中定位 */
    margin-left: -45%; /* 居中偏移 */
    white-space: normal; /* 允许换行 */
    text-align: center; /* 确保文本居中 */
    padding: 0 15px; /* 内边距 */
    box-sizing: border-box;
    line-height: 1.7; /* 增加行高 */
    letter-spacing: 3px; /* 增加字母间距 */
    transform-origin: center center;
    word-wrap: break-word;
    hyphens: auto;
  }
  
  .starwars-wrapper p.author-signature {
    font-size: 38px; /* Paulo Coelho移动端字体 */
    width: 95%; /* 稍微宽一点 */
    left: 50%;
    margin-left: -47.5%;
    text-align: center;
    padding: 0 10px;
    box-sizing: border-box;
    transform-origin: center center;
    white-space: nowrap; /* 保持不换行 */
  }
}

@media (max-width: 480px) {
  .starwars-wrapper p {
    font-size: 26px; /* 小屏幕字体 */
    width: 95%; /* 限制宽度 */
    left: 50%;
    margin-left: -47.5%;
    text-align: center;
    padding: 0 10px;
    box-sizing: border-box;
    line-height: 1.4; /* 增加行高 */
  }
  
  .starwars-wrapper p.author-signature {
    font-size: 30px; /* Paulo Coelho小屏幕 */
    width: 98%;
    left: 50%;
    margin-left: -49%;
    white-space: nowrap;
  }
  
  .intro-paragraph p {
    font-size: 11px;
  }
}
</style>