<template>
  <div v-if="isOpen" class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Register</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="reg-username">Username</label>
          <input
            id="reg-username"
            v-model="formData.username"
            type="text"
            required
            :disabled="loading"
            class="form-input"
            autocomplete="username"
            minlength="3"
            maxlength="50"
            pattern="[a-zA-Z0-9_]{3,50}"
            title="Username must be 3-50 characters, letters, numbers and underscore only"
          />
        </div>
        
        <div class="form-group">
          <label for="reg-email">Email</label>
          <input
            id="reg-email"
            v-model="formData.email"
            type="email"
            required
            :disabled="loading"
            class="form-input"
            autocomplete="email"
            maxlength="100"
            pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"
            title="Please enter a valid email address"
          />
        </div>
        
        <div class="form-group">
          <label for="reg-password">Password</label>
          <input
            id="reg-password"
            v-model="formData.password"
            type="password"
            required
            :disabled="loading"
            class="form-input"
            autocomplete="new-password"
            minlength="6"
            maxlength="100"
            title="Password must be at least 6 characters long"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm-password">Confirm Password</label>
          <input
            id="confirm-password"
            v-model="formData.confirmPassword"
            type="password"
            required
            :disabled="loading"
            class="form-input"
            autocomplete="new-password"
            minlength="6"
            maxlength="100"
            title="Please confirm your password"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          {{ success }}
        </div>
        
        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? 'Creating account... (This may take 10-15 seconds)' : 'Register' }}
        </button>
      </form>
      
      <div class="modal-footer">
        <p>Already have an account? 
          <button @click="$emit('switchToLogin')" class="link-btn">
            Login here
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useAuthStore } from '../stores/auth'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits(['close', 'switchToLogin'])

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')
const success = ref('')

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateForm = () => {
  // Clear previous errors
  error.value = ''
  
  // Username validation
  if (!formData.username || formData.username.length < 3) {
    error.value = 'Username must be at least 3 characters long'
    return false
  }
  
  if (!/^[a-zA-Z0-9_]{3,50}$/.test(formData.username)) {
    error.value = 'Username can only contain letters, numbers, and underscores'
    return false
  }
  
  // Email validation
  if (!formData.email) {
    error.value = 'Email is required'
    return false
  }
  
  const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i
  if (!emailRegex.test(formData.email)) {
    error.value = 'Please enter a valid email address'
    return false
  }
  
  // Password validation
  if (!formData.password || formData.password.length < 6) {
    error.value = 'Password must be at least 6 characters long'
    return false
  }
  
  // Confirm password validation
  if (formData.password !== formData.confirmPassword) {
    error.value = 'Passwords do not match'
    return false
  }
  
  return true
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const result = await authStore.register({
      username: formData.username.trim(),
      email: formData.email.toLowerCase().trim(),
      password: formData.password
    })
    
    if (result.success) {
      success.value = 'Account created successfully! You can now login.'
      setTimeout(() => {
        emit('switchToLogin')
      }, 2000)
    } else {
      error.value = result.error || 'Registration failed'
    }
  } catch (err) {
    console.error('Registration error:', err)
    error.value = 'Network error. Please check your connection and try again.'
  } finally {
    loading.value = false
  }
}

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    error.value = ''
    success.value = ''
    formData.username = ''
    formData.email = ''
    formData.password = ''
    formData.confirmPassword = ''
  }
})
</script>

<style scoped>
.modal-overlay {
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

.modal-content {
  background: white;
  border-radius: 15px;
  padding: 0;
  width: 100%;
  max-width: 400px;
  margin: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
  max-height: 90vh;
  overflow-y: auto;
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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e9ecef;
  position: sticky;
  top: 0;
  background: white;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s ease;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #dc3545;
}

.register-form {
  padding: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px; /* 防止iOS缩放 */
  transition: all 0.3s ease;
  box-sizing: border-box;
  -webkit-appearance: none; /* 移除iOS默认样式 */
  -moz-appearance: none;
  appearance: none;
  background-color: #fff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.7;
}

.error-message {
  background: #ffe6e6;
  color: #dc3545;
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  border-left: 4px solid #dc3545;
}

.success-message {
  background: #e6ffe6;
  color: #28a745;
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  border-left: 4px solid #28a745;
}

.submit-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px;
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
  transform: none;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid #e9ecef;
  text-align: center;
}

.modal-footer p {
  margin: 0;
  color: #6c757d;
}

.link-btn {
  background: none;
  border: none;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.link-btn:hover {
  color: #764ba2;
}

/* iOS Safari 特殊修复 */
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  .form-input {
    -webkit-appearance: none;
    border-radius: 8px;
  }
  
  .submit-btn {
    -webkit-appearance: none;
    border-radius: 8px;
  }
}

/* iOS 16+ 修复 */
@supports (-webkit-touch-callout: none) {
  .form-input {
    font-size: 16px; /* 防止缩放 */
    -webkit-text-size-adjust: 100%;
  }
  
  .modal-content {
    -webkit-transform: translateZ(0); /* 硬件加速 */
    transform: translateZ(0);
  }
}

/* 移动端特殊处理 */
@media (max-width: 768px) {
  .modal-content {
    margin: 10px;
    max-height: 95vh;
  }
  
  .form-input {
    font-size: 16px; /* 必须16px以上防止iOS缩放 */
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
}
</style>