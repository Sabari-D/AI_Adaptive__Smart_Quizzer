


<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()

// Determine if we are on the login or register path
const isLogin = computed(() => route.path === '/login')
const formTitle = computed(() => isLogin.value ? 'User Login' : 'User Registration')
const buttonText = computed(() => isLogin.value ? 'Log In' : 'Sign Up')

// Form State
const email = ref('')
const password = ref('')
// ✨ NEW STATE FIELDS ✨
const username = ref('')
const mobile_number = ref('')

const errorMsg = ref('')
const isLoading = ref(false)

// Handle Form Submission
async function handleSubmit() {
    errorMsg.value = ''
    isLoading.value = true
    
    const endpoint = isLogin.value ? 'login' : 'register';

    // --- 1. FRONTEND VALIDATION ---
    if (!email.value || !password.value) {
        errorMsg.value = 'Email and password are required.';
        isLoading.value = false;
        return;
    }
    
    // Validation for Registration Mode
    if (!isLogin.value) {
        if (!username.value || !mobile_number.value) {
            errorMsg.value = 'Username and Mobile Number are required for registration.';
            isLoading.value = false;
            return;
        }
        
        // Mobile Number Length Validation (10 digits)
        if (mobile_number.value.length !== 10 || !/^\d+$/.test(mobile_number.value)) {
            errorMsg.value = 'Enter a valid mobile number (must be exactly 10 digits).';
            isLoading.value = false;
            return;
        }
    }
    // ----------------------------

    try {
        // Assemble credentials, including new fields for registration
        const credentials = { 
            email: email.value, 
            password: password.value,
            // ✨ Pass new fields conditionally for registration ✨
            ...(!isLogin.value && { username: username.value, mobile_number: mobile_number.value })
        };

        // Call the Pinia store action
        await authStore.authenticateUser(endpoint, credentials);
        
    } catch (err: any) {
        errorMsg.value = err.message || 'An unknown error occurred during authentication.';
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
  <div class="auth-card">
    <h2>{{ formTitle }}</h2>
    <form @submit.prevent="handleSubmit">
      
      <div v-if="!isLogin" class="form-group">
        <label for="username">Username:</label>
        <input id="username" type="text" v-model="username" required>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="email" required>
      </div>
      
      <div v-if="!isLogin" class="form-group">
        <label for="mobile">Mobile Number:</label>
        <input id="mobile" type="tel" v-model="mobile_number" maxlength="10" required>
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" type="password" v-model="password" required>
      </div>

      <div v-if="isLogin" class="login-help-section">
          <RouterLink to="/account-support" class="link-help">
            Trouble Logging In?
          </RouterLink>
      </div>
      
      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>

      <button type="submit" :disabled="isLoading">
        <span v-if="isLoading">Processing...</span>
        <span v-else>{{ buttonText }}</span>
      </button>

      <div class="switch-link">
        <p v-if="isLogin">
          Don't have an account? 
          <RouterLink to="/register">Register here</RouterLink>
        </p>
        <p v-else>
          Already have an account? 
          <RouterLink to="/login">Log in here</RouterLink>
        </p>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Basic Card and Form Styling */
.auth-card {
    padding: 30px;
    border: 1px solid var(--color-border); 
    border-radius: 8px;
    max-width: 400px;
    margin: 50px auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    background-color: var(--color-card-bg); 
}

h2 {
    color: var(--color-primary); 
    margin-bottom: 20px;
}
.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: var(--color-text); 
}

.form-group input {
    width: 100%; 
    padding: 10px; 
    border: 1px solid var(--color-border); 
    background-color: var(--color-background); 
    color: var(--color-text);
    border-radius: 4px; 
    box-sizing: border-box;
}

/* Help Link Styling */
.login-help-section {
    text-align: right;
    margin-bottom: 15px;
    font-size: 0.9em;
}
.link-help {
    color: #9b59b6; 
    text-decoration: none;
}
.link-help:hover {
    text-decoration: underline;
}


/* --- UPDATED 3D BUTTON STYLES --- */
button {
    width: 100%;
    padding: 12px; 
    background-color: #3498db; 
    color: white;
    border: none;
    border-radius: 12px; 
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 600;
    transition: all 0.15s ease;
    
    /* 3D EFFECT STYLES */
    box-shadow: 0 5px 0 #2980b9; 
    transform: translateY(0);
    margin-top: 20px;
}

button:hover:not(:disabled) {
    background-color: #2980b9; 
}

button:active:not(:disabled) {
    box-shadow: 0 2px 0 #2980b9;
    transform: translateY(3px);
}

button:disabled {
    background-color: #95a5a6;
    box-shadow: 0 4px 0 #7f8c8d;
    cursor: not-allowed;
    transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.error-message {
    color: #e74c3c;
    margin-bottom: 15px;
    text-align: center;
    padding: 10px;
    border: 1px solid #e74c3c;
    border-radius: 4px;
}

.switch-link {
    margin-top: 20px;
    text-align: center;
    font-size: 0.9em;
    color: var(--color-text); 
}

.switch-link a {
    color: var(--color-primary); 
    text-decoration: none;
    font-weight: bold;
}

</style>
