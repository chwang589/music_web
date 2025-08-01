<template>
  <section id="introduction" class="introduction-section">
    <canvas ref="starCanvas" class="star-canvas"></canvas>
    <div class="starwars-container" v-if="showStarWars">
      <div class="starwars-wrapper">
        <p v-for="(line, index) in starWarsText" :key="index" 
           :style="getStarWarsStyle(index)">
          {{ line }}
        </p>
      </div>
    </div>
    <div class="content-wrapper" :class="{ hidden: showStarWars }">
      <div class="text-content">
        <h1 class="main-title">MUSIC WEB</h1>
        <div class="dynamic-text">
          <span class="text-line" :class="{ active: currentText === 0 }">Discover Amazing Music</span>
          <span class="text-line" :class="{ active: currentText === 1 }">Share Your Stories</span>
          <span class="text-line" :class="{ active: currentText === 2 }">Connect With Artists</span>
          <span class="text-line" :class="{ active: currentText === 3 }">Experience The Beat</span>
        </div>
        <p class="subtitle">Where music meets community</p>
      </div>
      
      <div class="cta-buttons">
        <button @click="scrollToNews" class="primary-btn explore-btn">
          <span class="btn-text">Explore News</span>
          <div class="btn-glow"></div>
        </button>
        <button @click="$emit('openLogin')" class="primary-btn join-btn">
          <span class="btn-text">Join Community</span>
          <div class="btn-glow"></div>
        </button>
        <button @click="triggerStarWars" class="primary-btn magic-btn">
          <span class="btn-icon">✨</span>
          <span class="btn-text">Experience Magic</span>
          <div class="btn-glow"></div>
        </button>
      </div>
    </div>
    
    <div class="scroll-indicator" @click="scrollToNews" :class="{ hidden: showStarWars }">
      <div class="scroll-arrow"></div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'

defineEmits(['openLogin'])

const starCanvas = ref<HTMLCanvasElement>()
const currentText = ref(0)
const showStarWars = ref(false)
let textInterval: number
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera  
let renderer: THREE.WebGLRenderer
let stars: THREE.Points
let nebulaClouds: THREE.Mesh[] = []
let animationId: number
let time = 0

const starWarsText = [
  'When you want something,',
  'all the universe conspires',  
  'in helping you to achieve it.',
  '',
  'Paulo Coelho',
  '',
  '',
  'Music Web is that conspiracy:',
  'the conspiracy of creativity.',
  '',
  '',
  'Trust is the single',
  'most important ingredient',
  'missing from digital relationships.',
  '',
  '',
  'We believe in the power',
  'of music to connect souls',
  'across time and space.',
  '',
  '',
  'Music Web is a digital mechanism',
  'of trust and discovery'
]

const scrollToNews = () => {
  const newsSection = document.getElementById('news')
  if (newsSection) {
    newsSection.scrollIntoView({ behavior: 'smooth' })
  }
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

const triggerStarWars = () => {
  showStarWars.value = true
  
  nextTick(() => {
    const wrapper = document.querySelector('.starwars-wrapper')
    if (wrapper) {
      gsap.fromTo(wrapper, 
        { y: '100vh' },
        { y: '-200vh', duration: 25, ease: 'none' }
      )
    }

    setTimeout(() => {
      showStarWars.value = false
    }, 25000)
  })
}

const getStarWarsStyle = (index: number) => {
  const progress = index * 0.1
  return {
    transform: `translateY(${progress * 100}%) perspective(300px) rotateX(25deg)`,
    opacity: Math.max(0, 1 - progress * 0.3),
    fontSize: `${Math.max(0.8, 1 - progress * 0.1)}rem`
  }
}

const handleResize = () => {
  if (!camera || !renderer) return
  
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

onMounted(() => {
  textInterval = setInterval(() => {
    currentText.value = (currentText.value + 1) % 4
  }, 3000)

  nextTick(() => {
    initStarField()
  })

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (textInterval) {
    clearInterval(textInterval)
  }
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    renderer.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

.introduction-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.introduction-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(255, 107, 107, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(78, 205, 196, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(155, 89, 182, 0.18) 0%, transparent 50%),
    radial-gradient(circle at 60% 70%, rgba(52, 152, 219, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #001122 0%, #002244 50%, #000811 100%);
  animation: nebulaDrift 20s ease-in-out infinite;
  z-index: 0;
}

@keyframes nebulaDrift {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.8;
  }
  33% {
    transform: scale(1.05) rotate(1deg);
    opacity: 0.9;
  }
  66% {
    transform: scale(0.95) rotate(-1deg);
    opacity: 0.85;
  }
}

.star-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.starwars-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  perspective: 400px;
  overflow: hidden;
  background: radial-gradient(ellipse at center, #001122 0%, #000000 70%);
}

.starwars-wrapper {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  max-width: 800px;
  text-align: center;
  color: #ffd700;
  font-family: 'Arial', sans-serif;
  font-weight: bold;
  line-height: 1.8;
  transform-style: preserve-3d;
}

.starwars-wrapper p {
  font-size: 1.8rem;
  margin: 1rem 0;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  transform-origin: 50% 100%;
}

.content-wrapper {
  text-align: center;
  color: white;
  z-index: 10;
  position: relative;
  will-change: transform;
  transition: opacity 0.5s ease;
}

.content-wrapper.hidden {
  opacity: 0;
  pointer-events: none;
}

.text-content {
  margin-bottom: 3rem;
}

.main-title {
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: clamp(2.5rem, 8vw, 4.5rem);
  font-weight: 700;
  margin-bottom: 2rem;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #c7d2fe 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 40px rgba(255, 255, 255, 0.3);
  will-change: transform;
  animation: titleGlow 1.8s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

@keyframes titleGlow {
  0% {
    opacity: 0;
    transform: translateY(40px) scale(0.9);
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.8), 0 0 60px rgba(100, 150, 255, 0.6);
  }
}

.dynamic-text {
  position: relative;
  height: 60px;
  margin-bottom: 2rem;
  overflow: hidden;
}

.text-line {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%) translateY(100%);
  font-family: 'Inter', sans-serif;
  font-size: clamp(1.2rem, 4vw, 1.6rem);
  font-weight: 400;
  opacity: 0;
  white-space: nowrap;
  will-change: transform, opacity;
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
  color: rgba(255, 255, 255, 0.85);
  letter-spacing: 0.01em;
}

.text-line.active {
  transform: translateX(-50%) translateY(0);
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.95);
}

.subtitle {
  font-family: 'Inter', sans-serif;
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  font-weight: 400;
  opacity: 0.6;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.02em;
  will-change: transform;
  animation: subtitleGlow 1.8s cubic-bezier(0.23, 1, 0.32, 1) 0.4s forwards;
}

@keyframes subtitleGlow {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 0.8;
    transform: translateY(0);
    text-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
  }
}

.cta-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  will-change: transform;
  animation: buttonsGlow 1.8s cubic-bezier(0.23, 1, 0.32, 1) 0.8s forwards;
  opacity: 0;
}

@keyframes buttonsGlow {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.primary-btn {
  position: relative;
  padding: 16px 32px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  color: rgba(255, 255, 255, 0.9);
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  will-change: transform;
  overflow: hidden;
  min-width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.primary-btn:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(255, 255, 255, 0.1);
}

.primary-btn .btn-text {
  position: relative;
  z-index: 2;
}

.primary-btn .btn-icon {
  position: relative;
  z-index: 2;
  font-size: 1.1em;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  transition: opacity 0.3s ease;
  border-radius: 8px;
}

.primary-btn:hover .btn-glow {
  opacity: 1;
}

.explore-btn:hover {
  border-color: rgba(100, 150, 255, 0.4);
  box-shadow: 0 8px 32px rgba(100, 150, 255, 0.15);
}

.join-btn:hover {
  border-color: rgba(255, 107, 107, 0.4);
  box-shadow: 0 8px 32px rgba(255, 107, 107, 0.15);
}

.magic-btn:hover {
  border-color: rgba(167, 139, 250, 0.4);
  box-shadow: 0 8px 32px rgba(167, 139, 250, 0.15);
}

.magic-btn::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
  transform: rotate(45deg) translateX(-100%);
  transition: transform 0.6s ease;
  opacity: 0;
}

.magic-btn:hover::before {
  transform: rotate(45deg) translateX(100%);
  opacity: 1;
}

.scroll-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  will-change: transform;
  animation: starBounce 2.5s ease-in-out infinite;
  transition: opacity 0.3s ease;
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

@keyframes starBounce {
  0%, 100% { 
    transform: translateX(-50%) translateY(0);
    opacity: 0.8;
  }
  50% { 
    transform: translateX(-50%) translateY(-8px);
    opacity: 1;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
  }
}

@media (max-width: 768px) {
  .introduction-section {
    padding: 0 1rem;
  }

  .content-wrapper {
    max-width: 100%;
  }

  .text-content {
    margin-bottom: 2rem;
  }

  .cta-buttons {
    gap: 0.75rem;
    padding: 0 1rem;
  }
  
  .primary-btn {
    min-width: 100%;
    max-width: 320px;
    padding: 14px 24px;
    font-size: 0.85rem;
  }

  .starwars-wrapper {
    width: 95%;
    padding: 0 1rem;
  }

  .starwars-wrapper p {
    font-size: 1.2rem;
    line-height: 1.6;
  }
}

@media (max-width: 480px) {
  .cta-buttons {
    padding: 0;
  }

  .primary-btn {
    padding: 12px 20px;
    font-size: 0.8rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .main-title,
  .text-line,
  .subtitle,
  .cta-buttons,
  .scroll-indicator {
    animation: none;
  }
  
  .text-line.active {
    transition: opacity 0.3s ease;
  }

  .magic-btn::before,
  .magic-btn:hover::before {
    animation: none;
  }
}
</style>