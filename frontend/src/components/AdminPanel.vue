<template>
  <div v-if="isOpen" class="admin-overlay" @click="$emit('close')">
    <div class="admin-panel" @click.stop>
      <div class="admin-header">
        <h2>News Management</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="admin-content">
        <div class="admin-tabs">
          <button 
            @click="activeTab = 'create'"
            :class="{ active: activeTab === 'create' }"
            class="tab-btn"
          >
            Create News
          </button>
          <button 
            @click="activeTab = 'manage'"
            :class="{ active: activeTab === 'manage' }"
            class="tab-btn"
          >
            Manage News
          </button>
        </div>
        
        <!-- Create News Tab -->
        <div v-if="activeTab === 'create'" class="tab-content">
          <div class="quick-templates">
            <h4>🚀 快速开始</h4>
            <div class="template-buttons">
              <button 
                v-for="(template, index) in quickTemplates"
                :key="index"
                @click="useTemplate(template)"
                type="button"
                class="template-btn"
              >
                {{ template.title }}
              </button>
            </div>
          </div>
          
          <form @submit.prevent="handleCreateNews" class="news-form">
            <div class="form-group">
              <label for="news-title">Title</label>
              <input
                id="news-title"
                v-model="newNews.title"
                type="text"
                required
                :disabled="loading"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label for="news-description">Description</label>
              <textarea
                id="news-description"
                v-model="newNews.description"
                required
                :disabled="loading"
                class="form-textarea"
                rows="4"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="news-image">Image URL</label>
              <input
                id="news-image"
                v-model="newNews.image_url"
                type="url"
                :disabled="loading"
                class="form-input"
                placeholder="https://example.com/image.jpg"
              />
              <div class="image-suggestions">
                <p class="suggestion-title">🖼️ 推荐图片 (点击使用):</p>
                <div class="suggestion-grid">
                  <div 
                    v-for="(img, index) in suggestedImages" 
                    :key="index"
                    @click="newNews.image_url = img.url"
                    class="suggestion-item"
                    :title="img.description"
                  >
                    <img :src="img.url" :alt="img.description" />
                    <span>{{ img.description }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="createError" class="error-message">
              {{ createError }}
            </div>
            
            <div v-if="createSuccess" class="success-message">
              {{ createSuccess }}
            </div>
            
            <button type="submit" :disabled="loading" class="submit-btn">
              {{ loading ? 'Creating...' : 'Create News' }}
            </button>
          </form>
        </div>
        
        <!-- Manage News Tab -->
        <div v-if="activeTab === 'manage'" class="tab-content">
          <div class="news-list">
            <div v-if="loadingNews" class="loading">Loading your news...</div>
            
            <div v-else-if="userNews.length === 0" class="no-news">
              You haven't created any news yet.
            </div>
            
            <div v-else>
              <div 
                v-for="news in userNews" 
                :key="news.id" 
                class="news-item"
              >
                <div class="news-item-content">
                  <h4>{{ news.title }}</h4>
                  <p>{{ truncateText(news.description, 100) }}</p>
                  <small>Created: {{ formatDate(news.created_at) }}</small>
                </div>
                <div class="news-item-actions">
                  <button @click="editNews(news)" class="edit-btn">
                    Edit
                  </button>
                  <button @click="deleteNews(news.id)" class="delete-btn">
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Edit Modal -->
        <div v-if="editingNews" class="edit-modal">
          <div class="edit-modal-content">
            <h3>Edit News</h3>
            <form @submit.prevent="handleEditNews" class="news-form">
              <div class="form-group">
                <label>Title</label>
                <input
                  v-model="editingNews.title"
                  type="text"
                  required
                  class="form-input"
                />
              </div>
              
              <div class="form-group">
                <label>Description</label>
                <textarea
                  v-model="editingNews.description"
                  required
                  class="form-textarea"
                  rows="4"
                ></textarea>
              </div>
              
              <div class="form-group">
                <label>Image URL</label>
                <input
                  v-model="editingNews.image_url"
                  type="url"
                  class="form-input"
                />
              </div>
              
              <div class="edit-actions">
                <button type="button" @click="cancelEdit" class="cancel-btn">
                  Cancel
                </button>
                <button type="submit" class="submit-btn">
                  Update
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

interface NewsItem {
  id: number
  title: string
  description: string
  image_url?: string
  creator: string
  created_at: string
  updated_at: string
}

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const activeTab = ref('create')
const loading = ref(false)
const loadingNews = ref(false)
const createError = ref('')
const createSuccess = ref('')
const userNews = ref<NewsItem[]>([])
const editingNews = ref<NewsItem | null>(null)

const newNews = reactive({
  title: '',
  description: '',
  image_url: ''
})

// 推荐图片
const suggestedImages = [
  {
    url: 'https://images.unsplash.com/photo-1459749187778-3663c29ab4b3?w=500',
    description: '音乐节'
  },
  {
    url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500',
    description: '摇滚演出'
  },
  {
    url: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500',
    description: '钢琴表演'
  },
  {
    url: 'https://images.unsplash.com/photo-1483032469466-b937c425697b?w=500',
    description: '说唱文化'
  },
  {
    url: 'https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=500',
    description: '古典音乐'
  },
  {
    url: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500',
    description: '独立音乐'
  }
]

// 快速创建模板
const quickTemplates = [
  {
    title: '🎵 音乐活动新消息',
    description: '最新的音乐活动即将开始，敬请期待...',
    image_url: 'https://images.unsplash.com/photo-1459749187778-3663c29ab4b3?w=500'
  },
  {
    title: '🎸 艺人动态更新',
    description: '知名艺人最新动态，为粉丝带来精彩内容...',
    image_url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500'
  }
]

const useTemplate = (template: any) => {
  newNews.title = template.title
  newNews.description = template.description
  newNews.image_url = template.image_url
}

const handleCreateNews = async () => {
  if (!authStore.isAuthenticated) {
    createError.value = 'You must be logged in to create news'
    return
  }

  loading.value = true
  createError.value = ''
  createSuccess.value = ''
  
  try {
    await axios.post(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/news/`, {
      title: newNews.title,
      description: newNews.description,
      image_url: newNews.image_url || null
    })
    
    createSuccess.value = 'News created successfully!'
    
    // Reset form
    newNews.title = ''
    newNews.description = ''
    newNews.image_url = ''
    
    // Refresh news list if on manage tab
    if (activeTab.value === 'manage') {
      fetchUserNews()
    }
    
  } catch (error: any) {
    createError.value = error.response?.data?.detail || 'Failed to create news'
  } finally {
    loading.value = false
  }
}

const fetchUserNews = async () => {
  if (!authStore.isAuthenticated) return
  
  loadingNews.value = true
  
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/news/`)
    userNews.value = response.data.filter((news: NewsItem) => 
      news.creator === authStore.username
    )
  } catch (error) {
    console.error('Failed to fetch user news:', error)
  } finally {
    loadingNews.value = false
  }
}

const editNews = (news: NewsItem) => {
  editingNews.value = { ...news }
}

const cancelEdit = () => {
  editingNews.value = null
}

const handleEditNews = async () => {
  if (!editingNews.value) return
  
  try {
    await axios.put(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/news/${editingNews.value.id}`, {
      title: editingNews.value.title,
      description: editingNews.value.description,
      image_url: editingNews.value.image_url || null
    })
    
    editingNews.value = null
    fetchUserNews()
  } catch (error: any) {
    console.error('Failed to update news:', error)
  }
}

const deleteNews = async (newsId: number) => {
  if (!confirm('Are you sure you want to delete this news?')) return
  
  try {
    await axios.delete(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/news/${newsId}`)
    fetchUserNews()
  } catch (error: any) {
    console.error('Failed to delete news:', error)
  }
}

const truncateText = (text: string, maxLength: number) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

watch(() => activeTab.value, (newTab) => {
  if (newTab === 'manage') {
    fetchUserNews()
  }
})

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    activeTab.value = 'create'
    createError.value = ''
    createSuccess.value = ''
    newNews.title = ''
    newNews.description = ''
    newNews.image_url = ''
    editingNews.value = null
  }
})
</script>

<style scoped>
.admin-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.admin-panel {
  background: white;
  border-radius: 15px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e9ecef;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.admin-header h2 {
  margin: 0;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.admin-content {
  max-height: calc(80vh - 70px);
  overflow-y: auto;
}

.admin-tabs {
  display: flex;
  border-bottom: 1px solid #e9ecef;
}

.tab-btn {
  flex: 1;
  padding: 15px;
  border: none;
  background: #f8f9fa;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.tab-btn.active {
  background: white;
  color: #667eea;
  border-bottom: 3px solid #667eea;
}

.tab-btn:hover:not(.active) {
  background: #e9ecef;
}

.tab-content {
  padding: 25px;
}

.news-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-input, .form-textarea {
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.error-message {
  background: #ffe6e6;
  color: #dc3545;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 14px;
  border-left: 4px solid #dc3545;
}

.success-message {
  background: #e6ffe6;
  color: #28a745;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 14px;
  border-left: 4px solid #28a745;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.loading, .no-news {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.news-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}

.news-item:hover {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.news-item-content {
  flex: 1;
}

.news-item-content h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.news-item-content p {
  margin: 0 0 8px 0;
  color: #6c757d;
  line-height: 1.4;
}

.news-item-content small {
  color: #868e96;
}

.news-item-actions {
  display: flex;
  gap: 8px;
  margin-left: 15px;
}

.edit-btn, .delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: #17a2b8;
  color: white;
}

.edit-btn:hover {
  background: #138496;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.edit-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.edit-modal-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 400px;
  max-height: 80%;
  overflow-y: auto;
}

.edit-modal-content h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.edit-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

.quick-templates {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.quick-templates h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.template-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.template-btn {
  padding: 8px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-btn:hover {
  background: #5a6fd8;
  transform: translateY(-1px);
}

.image-suggestions {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.suggestion-title {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #2c3e50;
}

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.suggestion-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.suggestion-item:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.suggestion-item img {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 0.25rem;
}

.suggestion-item span {
  font-size: 0.75rem;
  text-align: center;
  color: #6c757d;
}

@media (max-width: 768px) {
  .admin-panel {
    width: 95%;
    margin: 20px;
  }
  
  .news-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .news-item-actions {
    margin-left: 0;
    justify-content: flex-end;
  }
  
  .template-buttons {
    flex-direction: column;
  }
  
  .suggestion-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>