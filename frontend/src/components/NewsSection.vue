<template>
  <section id="news" class="news-section">
    <div class="container">
      <h2 class="section-title">Latest News</h2>
      
      <div class="news-grid" :class="{ expanded: showMore }">
        <div 
          v-for="article in displayedNews" 
          :key="article.id" 
          class="news-card"
        >
          <div class="news-image">
            <img 
              :src="article.image_url || '/placeholder-image.jpg'" 
              :alt="article.title"
              @error="handleImageError"
            />
          </div>
          <div class="news-content">
            <h3 class="news-title">{{ article.title }}</h3>
            <p class="news-description">{{ truncateDescription(article.description) }}</p>
            <div class="news-meta">
              <span class="creator">By: {{ article.creator }}</span>
              <span class="date">{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="load-more-container" v-if="newsList.length > 6">
        <button @click="toggleShowMore" class="load-more-btn">
          {{ showMore ? 'Show Less' : 'Load More' }}
        </button>
      </div>
      
      <div v-if="loading" class="loading">
        Loading news...
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface NewsItem {
  id: number
  title: string
  description: string
  image_url?: string
  creator: string
  created_at: string
}

const newsList = ref<NewsItem[]>([])
const loading = ref(false)
const error = ref('')
const showMore = ref(false)

const displayedNews = computed(() => {
  return showMore.value ? newsList.value : newsList.value.slice(0, 6)
})

const toggleShowMore = () => {
  showMore.value = !showMore.value
}

const truncateDescription = (text: string) => {
  const words = text.split(' ')
  if (words.length > 20) {
    return words.slice(0, 20).join(' ') + '...'
  }
  return text
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjI0MCIgdmlld0JveD0iMCAwIDQwMCAyNDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMjQwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xNzUgMTAwTDE2NSAxMTBMMTc1IDEyMEgxNzVWMTAwWiIgZmlsbD0iIzlDQTNBRiIvPgo8cGF0aCBkPSJNMjI1IDEwMEwyMzUgMTEwTDIyNSAxMjBIMjI1VjEwMFoiIGZpbGw9IiM5Q0EzQUYiLz4KPHN2Zz4K'
}

const fetchNews = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/news?limit=20`)
    newsList.value = response.data
  } catch (err: any) {
    error.value = 'Failed to load news'
    console.error('Error fetching news:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchNews()
})
</script>

<style scoped>
.news-section {
  min-height: 100vh;
  padding: 80px 0;
  background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  font-size: 3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 3rem;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
  transition: all 0.3s ease;
}

.news-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.news-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.news-card:hover .news-image img {
  transform: scale(1.05);
}

.news-content {
  padding: 1.5rem;
}

.news-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.8rem;
  line-height: 1.4;
}

.news-description {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #868e96;
}

.creator {
  font-weight: 600;
  color: #667eea;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
}

.load-more-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.load-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

@media (max-width: 768px) {
  .news-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .news-card {
    margin: 0 10px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 15px;
  }
  
  .news-content {
    padding: 1rem;
  }
  
  .news-title {
    font-size: 1.1rem;
  }
}
</style>