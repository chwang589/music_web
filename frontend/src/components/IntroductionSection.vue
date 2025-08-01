<template>
  <section id="introduction" class="introduction-section">
    <div class="background-animation"></div>
    <div class="content-wrapper">
      <div class="scrolling-text-container">
        <h1 class="main-title">MUSIC WEB</h1>
        <div class="scrolling-text">
          <p class="scroll-item">Discover Amazing Music</p>
          <p class="scroll-item">Share Your Stories</p>
          <p class="scroll-item">Connect With Artists</p>
          <p class="scroll-item">Experience The Beat</p>
        </div>
        <p class="subtitle">Where music meets community</p>
      </div>
      
      <div class="cta-buttons">
        <button @click="scrollToNews" class="explore-btn">
          Explore News
        </button>
        <button @click="$emit('openLogin')" class="join-btn">
          Join Community
        </button>
      </div>
    </div>
    
    <div class="scroll-indicator" @click="scrollToNews">
      <div class="scroll-arrow"></div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineEmits(['openLogin'])

const scrollToNews = () => {
  const newsSection = document.getElementById('news')
  if (newsSection) {
    newsSection.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.introduction-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  animation: backgroundMove 20s ease-in-out infinite;
}

@keyframes backgroundMove {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(-2%, -1%) scale(1.02); }
  50% { transform: translate(1%, -2%) scale(0.98); }
  75% { transform: translate(-1%, 1%) scale(1.01); }
}

.content-wrapper {
  text-align: center;
  color: white;
  z-index: 2;
  position: relative;
}

.main-title {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 2rem;
  letter-spacing: 0.2em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 1s ease-out;
}

.scrolling-text-container {
  height: 120px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.scrolling-text {
  animation: scroll 8s linear infinite;
}

.scroll-item {
  font-size: 1.8rem;
  font-weight: 300;
  margin: 0.5rem 0;
  opacity: 0.9;
  height: 30px;
  line-height: 30px;
}

@keyframes scroll {
  0% { transform: translateY(0); }
  25% { transform: translateY(-30px); }
  50% { transform: translateY(-60px); }
  75% { transform: translateY(-90px); }
  100% { transform: translateY(-120px); }
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.8;
  margin-bottom: 3rem;
  animation: fadeInUp 1s ease-out 0.5s both;
}

.cta-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  animation: fadeInUp 1s ease-out 1s both;
}

.explore-btn, .join-btn {
  padding: 12px 30px;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.explore-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.explore-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.join-btn {
  background: #ff6b6b;
  color: white;
}

.join-btn:hover {
  background: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.scroll-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  animation: bounce 2s infinite;
}

.scroll-arrow {
  width: 20px;
  height: 20px;
  border-right: 2px solid white;
  border-bottom: 2px solid white;
  transform: rotate(45deg);
  opacity: 0.7;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
  40% { transform: translateX(-50%) translateY(-10px); }
  60% { transform: translateX(-50%) translateY(-5px); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2.5rem;
  }
  
  .scroll-item {
    font-size: 1.4rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>