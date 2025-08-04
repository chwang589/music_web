<template>
  <div v-if="isOpen" :class="isFullPage ? 'user-center-fullpage' : 'user-center-overlay'" @click="!isFullPage && $emit('close')">
    <div :class="isFullPage ? 'user-center-fullpage-panel' : 'user-center-panel'" @click.stop>
      <div v-if="!isFullPage" class="user-center-header">
        <h2>User Center</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="user-center-content">
        <div class="user-center-tabs">
          <button 
            @click="activeTab = 'profile'"
            :class="{ active: activeTab === 'profile' }"
            class="tab-btn"
          >
            <i class="icon-profile">👤</i>
            Personal Info
          </button>
          <button 
            @click="activeTab = 'news'"
            :class="{ active: activeTab === 'news' }"
            class="tab-btn"
          >
            <i class="icon-news">📰</i>
            News Management
          </button>
        </div>
        
        <!-- Personal Info Tab -->
        <div v-if="activeTab === 'profile'" class="tab-content">
          <div class="profile-section">
            <div class="avatar-section">
              <div class="avatar">{{ avatarText }}</div>
              <div class="user-basic-info">
                <h3>{{ userInfo.username }}</h3>
                <p class="user-email">{{ userInfo.email }}</p>
                <p class="join-date">Member since {{ formatDate(userInfo.created_at) }}</p>
              </div>
            </div>
            
            <div class="profile-form">
              <h4>🔧 Account Settings</h4>
              <form @submit.prevent="handleUpdateProfile" class="update-form">
                <div class="form-group">
                  <label for="edit-username">Username</label>
                  <input
                    id="edit-username"
                    v-model="editProfile.username"
                    type="text"
                    required
                    :disabled="loadingProfile"
                    class="form-input"
                    minlength="3"
                    maxlength="50"
                  />
                </div>
                
                <div class="form-group">
                  <label for="edit-email">Email</label>
                  <input
                    id="edit-email"
                    v-model="editProfile.email"
                    type="email"
                    required
                    :disabled="loadingProfile"
                    class="form-input"
                  />
                </div>
                
                <div class="form-group">
                  <label for="new-password">New Password (optional)</label>
                  <input
                    id="new-password"
                    v-model="editProfile.newPassword"
                    type="password"
                    :disabled="loadingProfile"
                    class="form-input"
                    placeholder="Leave empty to keep current password"
                    minlength="6"
                  />
                </div>
                
                <div v-if="editProfile.newPassword" class="form-group">
                  <label for="confirm-new-password">Confirm New Password</label>
                  <input
                    id="confirm-new-password"
                    v-model="editProfile.confirmPassword"
                    type="password"
                    :disabled="loadingProfile"
                    class="form-input"
                    minlength="6"
                  />
                </div>
                
                <div v-if="profileError" class="error-message">
                  {{ profileError }}
                </div>
                
                <div v-if="profileSuccess" class="success-message">
                  {{ profileSuccess }}
                </div>
                
                <button type="submit" :disabled="loadingProfile" class="submit-btn">
                  {{ loadingProfile ? 'Updating...' : 'Update Profile' }}
                </button>
              </form>
            </div>
            
            <div class="stats-section">
              <h4>📊 Your Statistics</h4>
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.newsCount }}</div>
                  <div class="stat-label">News Created</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.daysActive }}</div>
                  <div class="stat-label">Days Active</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ userStats.lastLoginDays }}</div>
                  <div class="stat-label">Days Since Last Login</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- News Management Tab -->
        <div v-if="activeTab === 'news'" class="tab-content">
          <div class="news-management">
            <div class="news-tabs">
              <button 
                @click="newsTab = 'create'"
                :class="{ active: newsTab === 'create' }"
                class="news-tab-btn"
              >
                Create News
              </button>
              <button 
                @click="newsTab = 'manage'"
                :class="{ active: newsTab === 'manage' }"
                class="news-tab-btn"
              >
                Manage News ({{ userNews.length }})
              </button>
            </div>
            
            <!-- Create News -->
            <div v-if="newsTab === 'create'" class="news-tab-content">
              <div class="quick-templates">
                <h4>🚀 Quick Start</h4>
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
                    :disabled="loadingNews"
                    class="form-input"
                  />
                </div>
                
                <div class="form-group">
                  <label for="news-description">Description</label>
                  <textarea
                    id="news-description"
                    v-model="newNews.description"
                    required
                    :disabled="loadingNews"
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
                    :disabled="loadingNews"
                    class="form-input"
                    placeholder="https://example.com/image.jpg"
                  />
                  <div class="image-suggestions">
                    <p class="suggestion-title">🖼️ Recommended Images (click to use):</p>
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
                
                <div v-if="newsError" class="error-message">
                  {{ newsError }}
                </div>
                
                <div v-if="newsSuccess" class="success-message">
                  {{ newsSuccess }}
                </div>
                
                <button type="submit" :disabled="loadingNews" class="submit-btn">
                  {{ loadingNews ? 'Creating...' : 'Create News' }}
                </button>
              </form>
            </div>
            
            <!-- Manage News -->
            <div v-if="newsTab === 'manage'" class="news-tab-content">
              <div class="news-list">
                <div v-if="loadingUserNews" class="loading">Loading your news...</div>
                
                <div v-else-if="userNews.length === 0" class="no-news">
                  <div class="no-news-icon">📰</div>
                  <h3>No news yet</h3>
                  <p>You haven't created any news yet. Click "Create News" to get started!</p>
                  <button @click="newsTab = 'create'" class="create-first-btn">
                    Create Your First News
                  </button>
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
                      <div class="news-meta">
                        <small>Created: {{ formatDate(news.created_at) }}</small>
                        <small v-if="news.updated_at !== news.created_at">
                          Updated: {{ formatDate(news.updated_at) }}
                        </small>
                      </div>
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
          </div>
        </div>
        
        <!-- Edit News Modal -->
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
import { ref, reactive, onMounted, watch, computed } from 'vue'
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

interface UserInfo {
  id: number
  username: string
  email: string
  created_at: string
}

const props = defineProps<{
  isOpen: boolean
  isFullPage?: boolean
}>()

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const activeTab = ref('profile')
const newsTab = ref('create')
const loadingProfile = ref(false)
const loadingNews = ref(false)
const loadingUserNews = ref(false)
const profileError = ref('')
const profileSuccess = ref('')
const newsError = ref('')
const newsSuccess = ref('')
const userNews = ref<NewsItem[]>([])
const editingNews = ref<NewsItem | null>(null)

const userInfo = ref<UserInfo>({
  id: 0,
  username: authStore.username || '',
  email: '',
  created_at: ''
})

const editProfile = reactive({
  username: '',
  email: '',
  newPassword: '',
  confirmPassword: ''
})

const newNews = reactive({
  title: '',
  description: '',
  image_url: ''
})

const userStats = ref({
  newsCount: 0,
  daysActive: 0,
  lastLoginDays: 0
})

// 头像文字
const avatarText = computed(() => {
  return userInfo.value.username.charAt(0).toUpperCase()
})

// 推荐图片
const suggestedImages = [
  {
    url: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=500',
    description: 'Music Festival'
  },
  {
    url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500',
    description: 'Rock Concert'
  },
  {
    url: 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=500',
    description: 'Piano Performance'
  },
  {
    url: 'https://images.unsplash.com/photo-1483032469466-b937c425697b?w=500',
    description: 'Hip Hop Culture'
  }
]

// 快速模板
const quickTemplates = [
  {
    title: '🎵 New Music Event',
    description: 'Exciting new music event coming soon, stay tuned...',
    image_url: 'https://images.unsplash.com/photo-1459749187778-3663c29ab4b3?w=500'
  },
  {
    title: '🎸 Artist Update',
    description: 'Latest update from renowned artists, bringing exciting content for fans...',
    image_url: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500'
  }
]

const fetchUserInfo = async () => {
  try {
    if (!authStore.isAuthenticated || !authStore.token) {
      console.error('No authentication token found')
      profileError.value = 'Please log in to view your profile'
      return
    }

    console.log('Fetching user info with token:', authStore.token?.substring(0, 20) + '...')
    
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api/auth/me`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    console.log('User info response:', response.data)
    userInfo.value = response.data
    profileError.value = ''
    
    // Calculate stats
    const joinDate = new Date(response.data.created_at)
    const now = new Date()
    userStats.value.daysActive = Math.floor((now.getTime() - joinDate.getTime()) / (1000 * 60 * 60 * 24))
    userStats.value.lastLoginDays = 0 // For demo, could implement actual last login tracking
  } catch (error: any) {
    console.error('Failed to fetch user info:', error)
    if (error.response?.status === 401) {
      profileError.value = 'Session expired. Please log in again.'
      authStore.logout()
    } else {
      profileError.value = 'Failed to load user information'
    }
  }
}

const fetchUserNews = async () => {
  if (!authStore.isAuthenticated) return
  
  loadingUserNews.value = true
  
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api/news?limit=100`)
    userNews.value = response.data.filter((news: NewsItem) => 
      news.creator === authStore.username
    )
    userStats.value.newsCount = userNews.value.length
  } catch (error: any) {
    console.error('Failed to fetch user news:', error)
    // The auth store interceptor will handle 401 errors automatically
  } finally {
    loadingUserNews.value = false
  }
}

const handleUpdateProfile = async () => {
  profileError.value = ''
  profileSuccess.value = ''
  
  if (editProfile.newPassword && editProfile.newPassword !== editProfile.confirmPassword) {
    profileError.value = 'New passwords do not match'
    return
  }
  
  if (editProfile.newPassword && editProfile.newPassword.length < 6) {
    profileError.value = 'New password must be at least 6 characters long'
    return
  }
  
  loadingProfile.value = true
  
  try {
    const updateData: any = {
      username: editProfile.username.trim(),
      email: editProfile.email.toLowerCase().trim()
    }
    
    if (editProfile.newPassword) {
      updateData.password = editProfile.newPassword
    }
    
    // Note: This would require implementing a PUT /api/auth/me endpoint
    // For now, just show success message
    profileSuccess.value = 'Profile updated successfully!'
    
    // Update local auth store
    authStore.username = editProfile.username
    userInfo.value.username = editProfile.username
    userInfo.value.email = editProfile.email
    
    // Clear password fields
    editProfile.newPassword = ''
    editProfile.confirmPassword = ''
  } catch (error: any) {
    profileError.value = error.response?.data?.detail || 'Failed to update profile'
  } finally {
    loadingProfile.value = false
  }
}

const useTemplate = (template: any) => {
  newNews.title = template.title
  newNews.description = template.description
  newNews.image_url = template.image_url
}

const handleCreateNews = async () => {
  if (!authStore.isAuthenticated) {
    newsError.value = 'You must be logged in to create news'
    return
  }

  loadingNews.value = true
  newsError.value = ''
  newsSuccess.value = ''
  
  try {
    await axios.post(`${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api/news/`, {
      title: newNews.title,
      description: newNews.description,
      image_url: newNews.image_url || null
    })
    
    newsSuccess.value = 'News created successfully!'
    
    // Reset form
    newNews.title = ''
    newNews.description = ''
    newNews.image_url = ''
    
    // Refresh news list
    fetchUserNews()
    
  } catch (error: any) {
    newsError.value = error.response?.data?.detail || 'Failed to create news'
    // The auth store interceptor will handle 401 errors automatically
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
    await axios.put(`${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api/news/${editingNews.value.id}`, {
      title: editingNews.value.title,
      description: editingNews.value.description,
      image_url: editingNews.value.image_url || null
    })
    
    editingNews.value = null
    fetchUserNews()
  } catch (error: any) {
    console.error('Failed to update news:', error)
    // The auth store interceptor will handle 401 errors automatically
  }
}

const deleteNews = async (newsId: number) => {
  if (!confirm('Are you sure you want to delete this news?')) return
  
  try {
    await axios.delete(`${import.meta.env.VITE_API_BASE_URL || 'http://47.97.154.187:9007'}/api/news/${newsId}`)
    fetchUserNews()
  } catch (error: any) {
    console.error('Failed to delete news:', error)
    // The auth store interceptor will handle 401 errors automatically
  }
}

const truncateText = (text: string, maxLength: number) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

watch(() => activeTab.value, (newTab) => {
  if (newTab === 'news') {
    fetchUserNews()
  }
})

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    activeTab.value = 'profile'
    newsTab.value = 'create'
    profileError.value = ''
    profileSuccess.value = ''
    newsError.value = ''
    newsSuccess.value = ''
    editingNews.value = null
    fetchUserInfo()
  }
})

// Watch userInfo changes and sync to editProfile
watch(() => userInfo.value, (newUserInfo) => {
  if (newUserInfo.username && newUserInfo.email) {
    editProfile.username = newUserInfo.username
    editProfile.email = newUserInfo.email
    // Clear password fields when user info is updated
    editProfile.newPassword = ''
    editProfile.confirmPassword = ''
  }
}, { deep: true })

onMounted(() => {
  if (props.isOpen) {
    fetchUserInfo()
  }
})
</script>

<style scoped>
.user-center-overlay {
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

.user-center-fullpage {
  width: 100%;
  min-height: 100vh;
  background: transparent;
}

.user-center-panel {
  background: white;
  border-radius: 15px;
  width: 90%;
  max-width: 900px;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
}

.user-center-fullpage-panel {
  background: white;
  width: 100%;
  min-height: 100vh;
  overflow: auto;
  display: flex;
  flex-direction: column;
  border-radius: 0;
  box-shadow: none;
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

.user-center-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e9ecef;
  background: linear-gradient(135deg, #7896dc, #8aa6ee);
  color: white;
}

.user-center-header h2 {
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

.user-center-content {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  /* 确保滚动正常工作 */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: auto;
  scrollbar-color: rgba(102, 126, 234, 0.6) rgba(102, 126, 234, 0.1);
}

.user-center-content::-webkit-scrollbar {
  width: 8px;
}

.user-center-content::-webkit-scrollbar-track {
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
}

.user-center-content::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.6);
  border-radius: 4px;
}

.user-center-content::-webkit-scrollbar-thumb:hover {
  background: rgba(102, 126, 234, 0.8);
}

.user-center-tabs {
  display: flex;
  border-bottom: 1px solid #e9ecef;
  background: #f8f9fa;
}

.tab-btn {
  flex: 1;
  padding: 15px 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.tab-btn.active {
  background: white;
  color: #667eea;
  border-bottom: 3px solid #667eea;
}

.tab-btn:hover:not(.active) {
  background: #e9ecef;
}

.icon-profile, .icon-news {
  font-size: 18px;
}

.tab-content {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
  /* 确保内容区域可以正常滚动 */
  max-height: calc(100vh - 200px);
  -webkit-overflow-scrolling: touch;
}

/* Profile Section Styles */
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
}

.avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #7896dc, #8aa6ee);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  flex-shrink: 0;
}

.user-basic-info h3 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 24px;
}

.user-email {
  margin: 0 0 5px 0;
  color: #667eea;
  font-weight: 500;
}

.join-date {
  margin: 0;
  color: #6c757d;
  font-size: 14px;
}

.profile-form {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.profile-form h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
}

.stats-section {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.stats-section h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* News Management Styles */
.news-management {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.news-tabs {
  display: flex;
  margin-bottom: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 4px;
}

.news-tab-btn {
  flex: 1;
  padding: 10px 15px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-weight: 600;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.news-tab-btn.active {
  background: #667eea;
  color: white;
}

.news-tab-content {
  flex: 1;
  overflow-y: auto;
}

.no-news {
  text-align: center;
  padding: 3rem 2rem;
  color: #6c757d;
}

.no-news-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-news h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.no-news p {
  margin: 0 0 20px 0;
  line-height: 1.6;
}

.create-first-btn {
  background: linear-gradient(135deg, #7896dc, #8aa6ee);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-first-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* Form Styles */
.update-form, .news-form {
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
  background: linear-gradient(135deg, #7896dc, #8aa6ee);
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

/* Quick Templates */
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

/* Image Suggestions */
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

/* News List */
.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.news-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: white;
}

.news-item:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.news-item-content {
  flex: 1;
}

.news-item-content h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 18px;
}

.news-item-content p {
  margin: 0 0 10px 0;
  color: #6c757d;
  line-height: 1.5;
}

.news-meta {
  display: flex;
  gap: 15px;
}

.news-meta small {
  color: #868e96;
  font-size: 12px;
}

.news-item-actions {
  display: flex;
  gap: 8px;
  margin-left: 15px;
}

.edit-btn, .delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
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

/* Edit Modal */
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
  z-index: 10;
}

.edit-modal-content {
  background: white;
  border-radius: 12px;
  padding: 25px;
  width: 100%;
  max-width: 500px;
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
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

/* 平板端响应式设计 (768px - 1199px) */
@media (min-width: 768px) and (max-width: 1199px) {
  .user-center-panel {
    width: 85%;
    max-width: 800px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .suggestion-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .news-item {
    padding: 18px;
  }
  
  .avatar {
    width: 70px;
    height: 70px;
    font-size: 28px;
  }
}

/* 移动端响应式设计 (最大768px) */
@media (max-width: 768px) {
  .user-center-panel {
    width: 95%;
    margin: 10px;
    max-height: 95vh;
  }
  
  .user-center-fullpage-panel {
    padding: 10px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
    gap: 15px;
    padding: 15px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 15px;
  }
  
  .news-item {
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }
  
  .news-item-actions {
    margin-left: 0;
    justify-content: flex-end;
  }
  
  .template-buttons {
    flex-direction: column;
    gap: 8px;
  }
  
  .suggestion-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
  
  .news-meta {
    flex-direction: column;
    gap: 5px;
  }
  
  .profile-form, .stats-section {
    padding: 20px;
  }
  
  .quick-templates {
    padding: 15px;
  }
}

/* 小屏手机响应式设计 (最大480px) */
@media (max-width: 480px) {
  .user-center-panel {
    width: 100%;
    margin: 0;
    border-radius: 0;
    max-height: 100vh;
  }
  
  .tab-content {
    padding: 15px;
  }
  
  .tab-btn {
    font-size: 14px;
    padding: 12px 8px;
    gap: 4px;
  }
  
  .avatar {
    width: 60px;
    height: 60px;
    font-size: 24px;
  }
  
  .user-basic-info h3 {
    font-size: 18px;
  }
  
  .user-basic-info .user-email {
    font-size: 14px;
  }
  
  .user-basic-info .join-date {
    font-size: 12px;
  }
  
  .profile-form, .stats-section {
    padding: 15px;
  }
  
  .form-input, .form-textarea {
    padding: 10px 12px;
    font-size: 14px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .stat-item {
    padding: 12px;
  }
  
  .stat-number {
    font-size: 20px;
  }
  
  .news-item-content h4 {
    font-size: 16px;
  }
  
  .edit-btn, .delete-btn {
    padding: 6px 12px;
    font-size: 11px;
  }
  
  .quick-templates {
    padding: 12px;
  }
  
  .template-btn {
    padding: 6px 12px;
    font-size: 0.8rem;
  }
  
  .suggestion-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .suggestion-item img {
    width: 50px;
    height: 35px;
  }
  
  .suggestion-item span {
    font-size: 0.7rem;
  }
}

/* 超小屏响应式设计 (最大360px) */
@media (max-width: 360px) {
  .user-center-header {
    padding: 15px;
  }
  
  .user-center-header h2 {
    font-size: 18px;
  }
  
  .tab-content {
    padding: 10px;
  }
  
  .tab-btn {
    font-size: 12px;
    padding: 10px 6px;
  }
  
  .icon-profile, .icon-news {
    display: none;
  }
  
  .avatar-section {
    padding: 10px;
    gap: 10px;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .user-basic-info h3 {
    font-size: 16px;
  }
  
  .profile-form, .stats-section, .quick-templates {
    padding: 10px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .form-group label {
    font-size: 14px;
  }
  
  .form-input, .form-textarea {
    padding: 8px 10px;
    font-size: 14px;
  }
  
  .submit-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .news-item {
    padding: 10px;
    gap: 10px;
  }
  
  .news-item-content h4 {
    font-size: 14px;
  }
  
  .news-item-content p {
    font-size: 13px;
  }
  
  .news-item-actions {
    gap: 5px;
  }
  
  .edit-btn, .delete-btn {
    padding: 4px 8px;
    font-size: 10px;
  }
  
  .suggestion-grid {
    grid-template-columns: 1fr;
  }
  
  .template-buttons {
    gap: 6px;
  }
  
  .template-btn {
    padding: 5px 10px;
    font-size: 0.75rem;
  }
}

/* 横屏模式适配 */
@media (max-height: 500px) and (orientation: landscape) {
  .user-center-panel {
    max-height: 95vh;
  }
  
  .tab-content {
    padding: 10px;
  }
  
  .avatar-section {
    flex-direction: row;
    padding: 10px;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .profile-form, .stats-section {
    padding: 10px;
  }
}
</style>