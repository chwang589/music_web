<template>
  <section id="introduction" class="introduction-section">
    <!-- Dynamic Background -->
    <canvas ref="starCanvas" class="star-canvas"></canvas>
    
    
    <!-- Slide Content Container -->
    <div class="slides-container">
      <!-- Slide 1: Quote -->
      <div class="cineslider-slide scroll-section" data-section="1">
        <div class="slide-content">
          <blockquote class="main-quote">
            <p class="quote-text">
              When you want something,<br>
              all the universe conspires<br>
              in helping you to achieve it.
            </p>
            <cite class="quote-author">Paulo Coelho</cite>
          </blockquote>
        </div>
      </div>
      
      <!-- Slide 2: Brand Statement -->
      <div class="cineslider-slide scroll-section" data-section="2">
        <div class="slide-content">
          <h1 class="brand-title">NeuraFlow: Where AI meets music:</h1>
          <h2 class="brand-subtitle">neural networks, infinite melodies.</h2>
        </div>
      </div>
      
      <!-- Slide 3: Philosophy -->
      <div class="cineslider-slide scroll-section" data-section="3">
        <div class="slide-content">
          <p class="philosophy-line">Intelligence is the single</p>
          <p class="philosophy-line">most powerful force</p>
          <p class="philosophy-line">shaping music's digital future.</p>
        </div>
      </div>
      
      <!-- Slide 4: Vision -->
      <div class="cineslider-slide scroll-section" data-section="4">
        <div class="slide-content">
          <p class="vision-text">
            We believe AI-powered music journalism<br>
            will revolutionize how we<br>
            <strong class="highlight-text">discover, understand, and connect</strong><br>
            with music.
          </p>
          <p class="difference-text">
            The future of music news<br>
            is intelligent, personalized,<br>
            and <strong class="trust-text">limitless</strong>.
          </p>
        </div>
      </div>
      
      <!-- Slide 5: Final Statement -->
      <div class="cineslider-slide scroll-section" data-section="5">
        <div class="slide-content">
          <h3 class="final-title">NeuraFlow is the <strong>intelligent bridge</strong> between AI and music</h3>
        </div>
      </div>
    </div>
    
    <!-- Scroll Indicator -->
    <div class="scroll-indicator" @click="nextSlide" v-show="currentSlide < totalSlides - 1">
      <span class="scroll-text">scroll down</span>
      <div class="scroll-arrow"></div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'

const emit = defineEmits(['openLogin', 'updateProgress', 'nextSlide'])

const starCanvas = ref<HTMLCanvasElement>()
const currentSlide = ref(0)
const totalSlides = 5
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera  
let renderer: THREE.WebGLRenderer
let stars: THREE.Points
let nebulaClouds: THREE.Mesh[] = []
let animationId: number
let time = 0
let isScrolling = false

const updateProgress = () => {
  // Calculate progress: 0-100% based on current slide
  const progress = (currentSlide.value / (totalSlides - 1)) * 100
  emit('updateProgress', progress)
}

const scrollToNext = () => {
  // Instead of scrolling to news section, emit event to go to next slide
  emit('nextSlide')
}

const initStarField = () => {
  if (!starCanvas.value) return

  scene = new THREE.Scene()
  
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  renderer = new THREE.WebGLRenderer({ 
    canvas: starCanvas.value,
    alpha: true,
    antialias: true
  })
  
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x000000, 1)

  // Create colorful nebula clouds (fewer on mobile for performance)
  const isMobile = window.innerWidth < 768
  const nebulaCount = isMobile ? 3 : 5
  
  if (nebulaCount >= 3) {
    createNebulaCloud(-300, -200, 0xff6b6b, 0.3) // Red nebula
    createNebulaCloud(200, 100, 0x4ecdc4, 0.25)  // Cyan nebula  
    createNebulaCloud(-100, 300, 0x9b59b6, 0.35) // Purple nebula
  }
  if (nebulaCount >= 5) {
    createNebulaCloud(400, -150, 0xf39c12, 0.2)  // Orange nebula
    createNebulaCloud(-400, 200, 0x3498db, 0.28) // Blue nebula
  }

  // Create multiple star layers for depth (reduce on mobile)
  const starMultiplier = isMobile ? 0.6 : 1
  createStarLayer(Math.floor(1200 * starMultiplier), 1.2, 0x6496c8)  // Far blue stars
  createStarLayer(Math.floor(600 * starMultiplier), 2.0, 0x9bb5d1)   // Medium white-blue stars
  createStarLayer(Math.floor(300 * starMultiplier), 3.0, 0xffffff)   // Close white stars
  createStarLayer(Math.floor(150 * starMultiplier), 4.0, 0xffff88)   // Bright yellow stars

  camera.position.z = 5
  animate()
}

const createNebulaCloud = (x: number, y: number, color: number, opacity: number) => {
  const nebulaGeometry = new THREE.PlaneGeometry(600, 400)
  
  // Create custom shader material for more realistic nebula effect
  const nebulaMaterial = new THREE.ShaderMaterial({
    uniforms: {
      time: { value: 0 },
      color: { value: new THREE.Color(color) },
      opacity: { value: opacity }
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform float time;
      uniform vec3 color;
      uniform float opacity;
      varying vec2 vUv;
      
      // Noise function for organic shapes
      float noise(vec2 p) {
        return sin(p.x * 10.0 + time * 0.5) * sin(p.y * 8.0 + time * 0.3) * 0.5 + 0.5;
      }
      
      void main() {
        vec2 uv = vUv - 0.5;
        float dist = length(uv);
        
        // Create flowing nebula pattern
        float n1 = noise(vUv * 2.0 + time * 0.1);
        float n2 = noise(vUv * 4.0 - time * 0.05);
        float n3 = noise(vUv * 8.0 + time * 0.08);
        
        float nebula = (n1 * 0.5 + n2 * 0.3 + n3 * 0.2);
        nebula *= smoothstep(0.8, 0.0, dist);
        
        vec3 finalColor = color * (0.8 + nebula * 0.4);
        float alpha = nebula * opacity * smoothstep(0.7, 0.0, dist);
        
        gl_FragColor = vec4(finalColor, alpha);
      }
    `,
    transparent: true,
    blending: THREE.AdditiveBlending
  })

  const nebula = new THREE.Mesh(nebulaGeometry, nebulaMaterial)
  nebula.position.set(x, y, -600 - Math.random() * 200)
  nebula.rotation.z = Math.random() * Math.PI * 2
  scene.add(nebula)
  
  // Store reference for animation
  if (!nebulaClouds) nebulaClouds = []
  nebulaClouds.push(nebula)
}

const createStarLayer = (count: number, size: number, color: number) => {
  const starGeometry = new THREE.BufferGeometry()
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  const baseColor = new THREE.Color(color)

  for (let i = 0; i < count * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 2000
    positions[i + 1] = (Math.random() - 0.5) * 2000  
    positions[i + 2] = (Math.random() - 0.5) * 1000

    // Vary the color slightly
    const starColor = baseColor.clone()
    starColor.multiplyScalar(0.8 + Math.random() * 0.4)
    colors[i] = starColor.r
    colors[i + 1] = starColor.g
    colors[i + 2] = starColor.b
  }

  starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  starGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const starMaterial = new THREE.PointsMaterial({
    size: size,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
  })

  const starLayer = new THREE.Points(starGeometry, starMaterial)
  scene.add(starLayer)
  
  if (!stars) stars = starLayer // Set the first layer as main stars for animation
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  time += 0.01
  
  // Animate nebula clouds
  nebulaClouds.forEach((nebula, index) => {
    if (nebula.material && 'uniforms' in nebula.material) {
      const material = nebula.material as THREE.ShaderMaterial
      material.uniforms.time.value = time
    }
    
    // Slow rotation for organic movement
    nebula.rotation.z += 0.0002 * (index % 2 === 0 ? 1 : -1)
    
    // Subtle position drift
    nebula.position.x += Math.sin(time * 0.1 + index) * 0.1
    nebula.position.y += Math.cos(time * 0.15 + index) * 0.1
  })
  
  // Animate stars
  if (stars) {
    stars.rotation.x += 0.0003
    stars.rotation.y += 0.0001
    
    const positions = stars.geometry.attributes.position.array as Float32Array
    for (let i = 0; i < positions.length; i += 3) {
      positions[i + 2] += 0.3
      if (positions[i + 2] > 1000) {
        positions[i + 2] = -1000
      }
    }
    stars.geometry.attributes.position.needsUpdate = true
  }

  renderer.render(scene, camera)
}


const handleResize = () => {
  if (!camera || !renderer) return
  
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

const initSlideSystem = () => {
  // Set initial state immediately - only show first slide
  gsap.set('.scroll-section', {
    opacity: 0,
    y: 50,
    pointerEvents: 'none'
  })

  gsap.set('[data-section="1"]', {
    opacity: 1,
    y: 0,
    pointerEvents: 'auto'
  })
}

const nextSlide = () => {
  if (isScrolling) return
  
  // If at last slide, scroll to next section
  if (currentSlide.value >= totalSlides - 1) {
    scrollToNext()
    return
  }
  
  isScrolling = true
  const current = currentSlide.value
  const next = current + 1
  
  // Hide current slide and show next slide simultaneously
  gsap.to(`[data-section="${current + 1}"]`, {
    opacity: 0,
    y: -30,
    duration: 0.3,
    pointerEvents: 'none'
  })
  
  // Show next slide
  gsap.to(`[data-section="${next + 1}"]`, {
    opacity: 1,
    y: 0,
    duration: 0.5,
    delay: 0.1,
    ease: 'power2.out',
    pointerEvents: 'auto',
    onComplete: () => {
      currentSlide.value = next
      updateProgress()
      isScrolling = false
    }
  })
}

const prevSlide = () => {
  if (isScrolling || currentSlide.value <= 0) return
  
  isScrolling = true
  const current = currentSlide.value
  const prev = current - 1
  
  // Hide current slide
  gsap.to(`[data-section="${current + 1}"]`, {
    opacity: 0,
    y: 30,
    duration: 0.3,
    pointerEvents: 'none'
  })
  
  // Show previous slide
  gsap.to(`[data-section="${prev + 1}"]`, {
    opacity: 1,
    y: 0,
    duration: 0.5,
    delay: 0.1,
    ease: 'power2.out',
    pointerEvents: 'auto',
    onComplete: () => {
      currentSlide.value = prev
      updateProgress()
      isScrolling = false
    }
  })
}

const handleWheel = (event: WheelEvent) => {
  // Handle internal slide navigation within introduction section
  event.preventDefault()
  
  if (event.deltaY > 0) {
    // If at last slide, go to next main slide (news)
    if (currentSlide.value >= totalSlides - 1) {
      scrollToNext()
    } else {
      nextSlide()
    }
  } else {
    prevSlide()
  }
}

onMounted(() => {
  nextTick(() => {
    // Initialize slide system immediately to prevent text stacking
    initSlideSystem()
    updateProgress() // Initial progress
    
    // Initialize star field
    initStarField()
  })

  // Add wheel event listener for slide navigation
  window.addEventListener('wheel', handleWheel, { passive: false })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
  }
  
  window.removeEventListener('wheel', handleWheel)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;900&display=swap');

/* 基础样式 */
.introduction-section {
  position: relative;
  height: 100vh; /* Fixed height like feedmusic.com */
  overflow: hidden; /* Prevent scrolling */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(180deg, #000 0%, #111 100%);
}

.introduction-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, #000 0%, #111 100%);
  z-index: 0;
}

/* 星云背景样式 */
.star-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}



/* Slides container */
.slides-container {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 10;
}

/* Cineslider slide styles */
.cineslider-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  will-change: transform, opacity;
}

/* Scroll sections - initial hidden state to prevent text stacking */
.scroll-section {
  opacity: 0;
  transform: translateY(50px);
  pointer-events: none;
}

/* First section visible by default */
.scroll-section[data-section="1"] {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.slide-content {
  text-align: center;
  color: white;
  max-width: 800px;
  padding: 0 2rem;
}

.main-quote {
  margin: 0;
  padding: 0;
  border: none;
}

.quote-text {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 400;
  line-height: 1.3;
  color: white;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.quote-author {
  font-family: 'Inter', sans-serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  font-style: italic;
  display: block;
}

.brand-title {
  font-family: 'Inter', sans-serif;
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 300;
  color: white;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.brand-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 400;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  line-height: 1.2;
}

.philosophy-line {
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.3rem, 3vw, 2rem);
  font-weight: 300;
  color: rgba(255, 255, 255, 0.85);
  margin: 0.2rem 0;
  line-height: 1.4;
}

.vision-text {
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  font-weight: 300;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
  line-height: 1.5;
}

.highlight-text {
  color: #4CAF50;
  font-weight: 700;
}

.difference-text {
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  font-weight: 300;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  line-height: 1.5;
}

.trust-text {
  color: #2196F3;
  font-weight: 600;
}

.final-title {
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  font-weight: 400;
  color: white;
  margin: 0;
  line-height: 1.3;
}

.final-title strong {
  color: #FF9800;
  font-weight: 700;
}

/* 滚动指示器样式 */
.scroll-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  will-change: transform;
  animation: scrollBounce 2.5s ease-in-out infinite;
  transition: opacity 0.3s ease;
}

.scroll-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: underline;
  font-weight: 300;
  letter-spacing: 0.02em;
}

.scroll-indicator.hidden {
  opacity: 0;
  pointer-events: none;
}

.scroll-arrow {
  width: 20px;
  height: 20px;
  border-right: 2px solid rgba(255, 255, 255, 0.8);
  border-bottom: 2px solid rgba(255, 255, 255, 0.8);
  transform: rotate(45deg);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

@keyframes scrollBounce {
  0%, 100% { 
    transform: translateX(-50%) translateY(0);
    opacity: 0.7;
  }
  50% { 
    transform: translateX(-50%) translateY(-8px);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .slide-content {
    padding: 0 1rem;
    max-width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-indicator {
    animation: none;
  }
}
</style>