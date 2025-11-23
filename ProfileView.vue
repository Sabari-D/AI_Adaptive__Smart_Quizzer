<!-- <script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully!'
  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    setTimeout(() => updateStatus.value = '', 3000) // Clear status message after 3 seconds
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style> -->





<!-- 
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; // <-- NEW IMPORT

const authStore = useAuthStore()
const router = useRouter(); // <-- NEW INSTANCE

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully! Redirecting...'
    
    // --- CRITICAL: REDIRECT TO CONTENT INGESTION PAGE ---
    setTimeout(() => {
        router.push('/content'); // <-- REDIRECT AFTER 1.5 SECONDS
    }, 1500);
    // ----------------------------------------------------

  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    // Note: The success message is now cleared by the redirect, 
    // but the error message needs its own timeout if the redirect fails.
    if (updateStatus.value.startsWith('❌')) {
        setTimeout(() => updateStatus.value = '', 3000);
    }
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    /* Ensure text color is light for the dark background */
    color: #e0e0e0; 
}

/* Ensure inner elements are visible */
.current-stats h3, .current-stats strong {
    color: #fff;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style> -->






<!-- 
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; // <-- NEW IMPORT

const authStore = useAuthStore()
const router = useRouter(); // <-- NEW INSTANCE

// Local state for the form
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
  if (authStore.userProfile) {
    // Clone the array to avoid direct mutation of the store state
    selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
    selectedDifficulty.value = authStore.userProfile.difficulty_level
  }
}

// Initialize on component mount
onMounted(() => {
  // Ensure profile is loaded when accessing the page directly (e.g., refreshing the page)
  if (!authStore.userProfile) {
    authStore.loadUserProfile()
  }
  initializeForm()
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
  if (newProfile) {
    initializeForm()
  }
}, { deep: true })


// 2. Handle Profile Update Submission
async function updateProfile() {
  isLoading.value = true
  updateStatus.value = ''
  
  if (selectedSubjects.value.length === 0) {
      updateStatus.value = '❌ Please select at least one subject.'
      isLoading.value = false
      return
  }

  try {
    const dataToUpdate = {
      subjects_of_interest: selectedSubjects.value,
      difficulty_level: selectedDifficulty.value,
    }

    // Call the Pinia store action, which calls the backend API
    await authStore.updateProfile(dataToUpdate as any)

    updateStatus.value = '✅ Profile updated successfully! Redirecting...'
    
    // --- CRITICAL: REDIRECT TO CONTENT INGESTION PAGE ---
    setTimeout(() => {
        // Redirects to /content to allow user to upload material or be quizzed on existing material.
        router.push('/content'); 
    }, 1500);
    // ----------------------------------------------------

  } catch (err) {
    updateStatus.value = '❌ Failed to update profile. Please try again.'
  } finally {
    isLoading.value = false
    // Clear error message if redirect fails
    if (updateStatus.value.startsWith('❌')) {
        setTimeout(() => updateStatus.value = '', 3000);
    }
  }
}
</script>

<template>
  <div v-if="authStore.userProfile">
    <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
    <p class="intro-text">
      Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
    </p>

    <div class="profile-card">
        <h2>Learning Preferences</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="difficulty">Default Difficulty Level:</label>
                <select id="difficulty" v-model="selectedDifficulty" required>
                    <option v-for="level in availableDifficulties" :key="level" :value="level">
                        {{ level }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Subjects of Interest (Select one or more):</label>
                <div class="checkbox-group">
                    <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                        <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                        {{ subject }}
                    </label>
                </div>
            </div>

            <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                {{ updateStatus }}
            </p>

            <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                <span v-if="isLoading">Saving...</span>
                <span v-else>Save Preferences</span>
            </button>
        </form>
    </div>
    
    <div class="current-stats">
        <h3>Current Profile Data</h3>
        <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
        <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Loading profile data... Please ensure you are logged in.</p>
  </div>
</template>

<style scoped>
/* Standardized Styling */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    /* Hides the default browser checkbox */
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- UPDATED 3D BUTTON STYLES --- */
button {
  width: 100%;
  padding: 14px; /* Slightly larger padding */
  background-color: #2ecc71; /* Green background */
  color: white;
  border: none;
  border-radius: 12px; /* Rounded corners */
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;

  /* 3D EFFECT STYLES */
  box-shadow: 0 6px 0 #27ae60; /* Darker shadow to create 3D base */
  transform: translateY(0);
}

button:hover:not(:disabled) {
  background-color: #27ae60; /* Darken slightly on hover */
}

button:active:not(:disabled) {
  /* Pressing effect: move button down, reduce shadow */
  box-shadow: 0 2px 0 #27ae60;
  transform: translateY(4px);
}

button:disabled {
  background-color: #a9d4b4;
  box-shadow: 0 4px 0 #89b49b;
  cursor: not-allowed;
  transform: translateY(0);
}
/* --- END UPDATED BUTTON STYLES --- */

.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    /* Ensure text color is light for the dark background */
    color: #e0e0e0; 
}

/* Ensure inner elements are visible */
.current-stats h3, .current-stats strong {
    color: #fff;
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}
</style> -->











<!-- 
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; 
import axios from 'axios'; // Needed for gamification stats fetch

// --- Store & Router Setup ---
const authStore = useAuthStore()
const router = useRouter(); 
const API_URL = 'http://localhost:5000/api'; // Define API URL for stats fetch

// --- State: Profile Configuration ---
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// --- State: Gamification Stats (NEW) ---
const streak = ref(0);
const badges = ref<string[]>([]);
const totalAnswered = ref(0);

// --- Profile Configuration Logic ---

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
    if (authStore.userProfile) {
        selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
        selectedDifficulty.value = authStore.userProfile.difficulty_level
    }
}

// 2. Handle Profile Update Submission
async function updateProfile() {
    isLoading.value = true
    updateStatus.value = ''
    
    if (selectedSubjects.value.length === 0) {
        updateStatus.value = '❌ Please select at least one subject.'
        isLoading.value = false
        return
    }

    try {
        const dataToUpdate = {
            subjects_of_interest: selectedSubjects.value,
            difficulty_level: selectedDifficulty.value,
        }

        // Call the Pinia store action, which calls the backend API
        await authStore.updateProfile(dataToUpdate as any)

        updateStatus.value = '✅ Profile updated successfully! Redirecting...'
        
        // --- CRITICAL: REDIRECT TO CONTENT INGESTION PAGE ---
        setTimeout(() => {
            router.push('/content'); 
        }, 1500);
        // ----------------------------------------------------

    } catch (err) {
        updateStatus.value = '❌ Failed to update profile. Please try again.'
    } finally {
        isLoading.value = false
        if (updateStatus.value.startsWith('❌')) {
            setTimeout(() => updateStatus.value = '', 3000);
        }
    }
}

// --- Gamification Logic (NEW) ---

// Fetch the gamification statistics from Route 20
async function fetchGamificationStats() {
    if (!authStore.isAuthenticated) return;
    try {
        // We use authStore.authHeader to pass the JWT token
        const url = `${API_URL}/gamification/stats`; 
        const response = await axios.get(url, authStore.authHeader);
        
        streak.value = response.data.login_streak;
        badges.value = response.data.badges;
        totalAnswered.value = response.data.total_answered;
        
    } catch (error) {
        console.error("Failed to load gamification stats:", error);
    }
}

// --- Lifecycle Hooks ---

onMounted(() => {
    // 1. Load Profile
    if (!authStore.userProfile) {
        authStore.loadUserProfile()
    }
    initializeForm()
    
    // 2. Load Gamification Stats
    fetchGamificationStats();
})

// Watch the Pinia store for changes (e.g., after initial login/load) and update the form
watch(() => authStore.userProfile, (newProfile) => {
    if (newProfile) {
        initializeForm()
    }
}, { deep: true })
</script>

<template>
    <div v-if="authStore.userProfile">
        <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
        <p class="intro-text">
            Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
        </p>

        <div class="profile-card">
            <h2>Learning Preferences</h2>
            <form @submit.prevent="updateProfile">
                <div class="form-group">
                    <label for="difficulty">Default Difficulty Level:</label>
                    <select id="difficulty" v-model="selectedDifficulty" required>
                        <option v-for="level in availableDifficulties" :key="level" :value="level">
                            {{ level }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Subjects of Interest (Select one or more):</label>
                    <div class="checkbox-group">
                        <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                            <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                            {{ subject }}
                        </label>
                    </div>
                </div>

                <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                    {{ updateStatus }}
                </p>

                <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                    <span v-if="isLoading">Saving...</span>
                    <span v-else>Save Preferences</span>
                </button>
            </form>
        </div>
        
        <div class="gamification-panel">
            <h3>🏆 My Achievements</h3>

            <div class="stat-box">
                <h4>🔥 Daily Streak</h4>
                <p class="stat-value">{{ streak }} Days</p>
            </div>

            <div class="stat-box">
                <h4>💯 Questions Answered</h4>
                <progress :value="totalAnswered" max="100"></progress>
                <p>{{ totalAnswered }} / 100</p>
            </div>

            <div class="badges-area">
                <h4>Badges Unlocked:</h4>
                <div v-if="badges.includes('Q100_MASTER')" class="badge-icon">
                    🥇 **100 Q Master**
                </div>
                <div v-else class="badge-placeholder">
                    Keep quizzing to earn your first badge!
                </div>
            </div>
        </div>
        <div class="current-stats">
            <h3>Current Profile Data</h3>
            <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
            <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
        </div>
    </div>
    <div v-else>
        <p>Loading profile data... Please ensure you are logged in.</p>
    </div>
</template>

<style scoped>
/* --- Profile Card Styling --- */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: #f9f9f9;
    margin-bottom: 30px; /* Added spacing */
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox .hidden-checkbox {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- Button Styling --- */
button {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: white;
    border: none;
    border-radius: 12px; 
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #27ae60; 
    transform: translateY(0);
}

button:hover:not(:disabled) {
    background-color: #27ae60; 
}

button:active:not(:disabled) {
    box-shadow: 0 2px 0 #27ae60;
    transform: translateY(4px);
}

button:disabled {
    background-color: #a9d4b4;
    box-shadow: 0 4px 0 #89b49b;
    cursor: not-allowed;
    transform: translateY(0);
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

/* --- Gamification Panel Styling (NEW) --- */
.gamification-panel {
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 30px; /* Added spacing */
}
.gamification-panel h3 {
    border-bottom: 2px solid #9b59b6;
    padding-bottom: 10px;
    margin-bottom: 20px;
    color: #9b59b6;
}
.stat-box {
    margin-bottom: 15px;
}
.stat-value {
    font-size: 1.5em;
    font-weight: bold;
    color: #3498db;
}
progress {
    width: 100%;
    height: 10px;
    margin-top: 5px;
}
.badge-icon {
    font-size: 1.1em;
    padding: 5px 10px;
    background-color: #f0e0ff;
    border: 1px solid #9b59b6;
    border-radius: 5px;
    display: inline-block;
}
.badge-placeholder {
    color: #7f8c8d;
    font-style: italic;
}
/* --- Current Stats Styling --- */
.current-stats {
    margin-top: 40px;
    padding: 20px;
    background-color: #0022ff;
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    color: #e0e0e0; 
}

.current-stats h3, .current-stats strong {
    color: #fff;
}
</style> -->







<!-- 

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; 
import axios from 'axios';
// Import the component file you created for the CBSD feature
import BlindSpotDetector from '@/views/BlindSpotDetector.vue'; 

// --- Store & Router Setup ---
const authStore = useAuthStore()
const router = useRouter(); 
// Define API URL for stats fetch (Ensure this matches your backend)
const API_URL = 'http://localhost:5000/api'; 

// --- State: Profile Configuration ---
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// --- State: Gamification Stats ---
const streak = ref(0);
const badges = ref<string[]>([]);
const totalAnswered = ref(0);

// --- Profile Configuration Logic ---

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
    if (authStore.userProfile) {
        selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
        selectedDifficulty.value = authStore.userProfile.difficulty_level
    }
}

// 2. Handle Profile Update Submission
async function updateProfile() {
    isLoading.value = true
    updateStatus.value = ''
    
    if (selectedSubjects.value.length === 0) {
        updateStatus.value = '❌ Please select at least one subject.'
        isLoading.value = false
        return
    }

    try {
        const dataToUpdate = {
            subjects_of_interest: selectedSubjects.value,
            difficulty_level: selectedDifficulty.value,
        }

        await authStore.updateProfile(dataToUpdate as any)

        updateStatus.value = '✅ Profile updated successfully! Redirecting...'
        
        setTimeout(() => {
            router.push('/content'); 
        }, 1500);

    } catch (err) {
        updateStatus.value = '❌ Failed to update profile. Please try again.'
    } finally {
        isLoading.value = false
        if (updateStatus.value.startsWith('❌')) {
            setTimeout(() => updateStatus.value = '', 3000);
        }
    }
}

// --- Gamification Logic ---

// Fetch the gamification statistics from Route 20
async function fetchGamificationStats() {
    if (!authStore.isAuthenticated) return;
    try {
        const url = `${API_URL}/gamification/stats`; 
        const response = await axios.get(url, authStore.authHeader);
        
        streak.value = response.data.login_streak;
        badges.value = response.data.badges;
        totalAnswered.value = response.data.total_answered;
        
    } catch (error) {
        console.error("Failed to load gamification stats:", error);
    }
}

// --- Lifecycle Hooks ---

onMounted(() => {
    if (!authStore.userProfile) {
        authStore.loadUserProfile()
    }
    initializeForm()
    fetchGamificationStats();
})

// Watch the Pinia store for changes and update the form
watch(() => authStore.userProfile, (newProfile) => {
    if (newProfile) {
        initializeForm()
    }
}, { deep: true })
</script>

<template>
    <div v-if="authStore.userProfile">
        <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
        <p class="intro-text">
            Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
        </p>

        <div class="profile-card">
            <h2>Learning Preferences</h2>
            <form @submit.prevent="updateProfile">
                <div class="form-group">
                    <label for="difficulty">Default Difficulty Level:</label>
                    <select id="difficulty" v-model="selectedDifficulty" required>
                        <option v-for="level in availableDifficulties" :key="level" :value="level">
                            {{ level }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Subjects of Interest (Select one or more):</label>
                    <div class="checkbox-group">
                        <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                            <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                            {{ subject }}
                        </label>
                    </div>
                </div>

                <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                    {{ updateStatus }}
                </p>

                <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                    <span v-if="isLoading">Saving...</span>
                    <span v-else>Save Preferences</span>
                </button>
            </form>
        </div>
        
        <BlindSpotDetector /> 
        
        <div class="gamification-panel">
            <h3>🏆 My Achievements</h3>

            <div class="stat-box">
                <h4>🔥 Daily Streak</h4>
                <p class="stat-value">{{ streak }} Days</p>
            </div>

            <div class="stat-box">
                <h4>💯 Questions Answered</h4>
                <progress :value="totalAnswered" max="100"></progress>
                <p>{{ totalAnswered }} / 100</p>
            </div>

            <div class="badges-area">
                <h4>Badges Unlocked:</h4>
                <div v-if="badges.includes('Q100_MASTER')" class="badge-icon">
                    🥇 **100 Q Master**
                </div>
                <div v-else class="badge-placeholder">
                    Keep quizzing to earn your first badge!
                </div>
            </div>
        </div>
        
        <div class="current-stats"> 
            <h3>Current Profile Data</h3>
            <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
            <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
        </div>
        
        <div class="final-scroll-spacer"></div>

    </div>
    <div v-else>
        <p>Loading profile data... Please ensure you are logged in.</p>
    </div>
</template>

<style scoped>
/* --- Profile Card Styling --- */
.intro-text {
    margin-bottom: 30px;
    color: #555;
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: var(--color-card-bg); /* Use theme variable */
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: var(--color-text); /* Use theme variable */
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid var(--color-border); /* Use theme variable */
    border-radius: 4px;
    background-color: var(--color-background); /* Use theme variable */
    color: var(--color-text);
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.subject-checkbox {
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
}

.subject-checkbox.checked {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}

/* --- Button Styling --- */
button {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: white;
    border: none;
    border-radius: 12px; 
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #27ae60; 
    transform: translateY(0);
}

button:hover:not(:disabled) {
    background-color: #27ae60; 
}

button:active:not(:disabled) {
    box-shadow: 0 2px 0 #27ae60;
    transform: translateY(4px);
}

button:disabled {
    background-color: #a9d4b4;
    box-shadow: 0 4px 0 #89b49b;
    cursor: not-allowed;
    transform: translateY(0);
}

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

/* --- Gamification Panel Styling (NEW) --- */
.gamification-panel {
    border: 1px solid var(--color-border);
    padding: 20px;
    border-radius: 8px;
    background: var(--color-card-bg); /* Use theme variable */
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
.gamification-panel h3 {
    border-bottom: 2px solid #9b59b6;
    padding-bottom: 10px;
    margin-bottom: 20px;
    color: #9b59b6;
}
.stat-box {
    margin-bottom: 15px;
}
.stat-value {
    font-size: 1.5em;
    font-weight: bold;
    color: var(--color-primary);
}
progress {
    width: 100%;
    height: 10px;
    margin-top: 5px;
}
.badge-icon {
    font-size: 1.1em;
    padding: 5px 10px;
    background-color: #f0e0ff;
    border: 1px solid #9b59b6;
    border-radius: 5px;
    display: inline-block;
}
.badge-placeholder {
    color: var(--color-text);
    font-style: italic;
}
/* --- Current Stats Styling --- */
.current-stats {
    margin-top: 40px;
    padding: 20px;
    /* Adjusted background colors to fit the dark mode aesthetic you established */
    background-color: #0022ff40; /* Semi-transparent blue for visibility */
    border: 1px solid #2e04ff;
    border-radius: 8px;
    font-size: 0.9em;
    color: #e0e0e0; 
}

.current-stats h3, .current-stats strong {
    color: #fff;
}

/* --- CRITICAL SCROLL FIX CSS --- */
.final-scroll-spacer {
    height: 100px; /* Forces 100px of empty space below the final element */
    width: 100%;
}
</style> -->



































































<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'; 
import axios from 'axios';
// Import the component file you created for the CBSD feature
import BlindSpotDetector from '@/views/BlindSpotDetector.vue'; 

// --- Store & Router Setup ---
const authStore = useAuthStore()
const router = useRouter(); 
const API_URL = 'http://localhost:5000/api'; // Define API URL for stats fetch

// --- State: Profile Configuration ---
const selectedSubjects = ref<string[]>([])
const selectedDifficulty = ref<'Beginner' | 'Intermediate' | 'Expert'>('Beginner')
const availableSubjects = ['Physics', 'Calculus', 'History', 'Programming', 'Biology', 'Chemistry', 'Economics', 'Literature']
const availableDifficulties = ['Beginner', 'Intermediate', 'Expert']
const updateStatus = ref('')
const isLoading = ref(false)

// --- State: Gamification Stats ---
const streak = ref(0);
const badges = ref<string[]>([]);
const totalAnswered = ref(0);

// --- Profile Configuration Logic ---

// 1. Initialize form state from Pinia store data
const initializeForm = () => {
    if (authStore.userProfile) {
        selectedSubjects.value = [...authStore.userProfile.subjects_of_interest]
        selectedDifficulty.value = authStore.userProfile.difficulty_level
    }
}

// 2. Handle Profile Update Submission
async function updateProfile() {
    isLoading.value = true
    updateStatus.value = ''
    
    if (selectedSubjects.value.length === 0) {
        updateStatus.value = '❌ Please select at least one subject.'
        isLoading.value = false
        return
    }

    try {
        const dataToUpdate = {
            subjects_of_interest: selectedSubjects.value,
            difficulty_level: selectedDifficulty.value,
        }

        await authStore.updateProfile(dataToUpdate as any)

        updateStatus.value = '✅ Profile updated successfully! Redirecting...'
        
        setTimeout(() => {
            router.push('/content'); 
        }, 1500);

    } catch (err) {
        updateStatus.value = '❌ Failed to update profile. Please try again.'
    } finally {
        isLoading.value = false
        if (updateStatus.value.startsWith('❌')) {
            setTimeout(() => updateStatus.value = '', 3000);
        }
    }
}

// --- Gamification Logic ---

// Fetch the gamification statistics from Route 20
async function fetchGamificationStats() {
    if (!authStore.isAuthenticated) return;
    try {
        const url = `${API_URL}/gamification/stats`; 
        const response = await axios.get(url, authStore.authHeader);
        
        streak.value = response.data.login_streak;
        badges.value = response.data.badges;
        totalAnswered.value = response.data.total_answered;
        
    } catch (error) {
        console.error("Failed to load gamification stats:", error);
    }
}

// --- Lifecycle Hooks ---

onMounted(() => {
    if (!authStore.userProfile) {
        authStore.loadUserProfile()
    }
    initializeForm()
    fetchGamificationStats();
})

// Watch the Pinia store for changes and update the form
watch(() => authStore.userProfile, (newProfile) => {
    if (newProfile) {
        initializeForm()
    }
}, { deep: true })
</script>

<template>
    <div v-if="authStore.userProfile">
        <h1>Welcome, {{ authStore.userProfile.email }}!</h1>
        <p class="intro-text">
            Configure your learning path. These settings will be used by the AI to select and generate personalized quizzes for you.
        </p>

        <div class="profile-card">
            <h2>Learning Preferences</h2>
            <form @submit.prevent="updateProfile">
                <div class="form-group">
                    <label for="difficulty">Default Difficulty Level:</label>
                    <select id="difficulty" v-model="selectedDifficulty" required>
                        <option v-for="level in availableDifficulties" :key="level" :value="level">
                            {{ level }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Subjects of Interest (Select one or more):</label>
                    <div class="checkbox-group">
                        <label v-for="subject in availableSubjects" :key="subject" class="subject-checkbox" :class="{'checked': selectedSubjects.includes(subject)}">
                            <input type="checkbox" :value="subject" v-model="selectedSubjects" class="hidden-checkbox">
                            {{ subject }}
                        </label>
                    </div>
                </div>

                <p v-if="updateStatus" :class="{'success-message': updateStatus.startsWith('✅'), 'error-message': updateStatus.startsWith('❌') }">
                    {{ updateStatus }}
                </p>

                <button type="submit" :disabled="isLoading || selectedSubjects.length === 0">
                    <span v-if="isLoading">Saving...</span>
                    <span v-else>Save Preferences</span>
                </button>
            </form>
        </div>
        
        <BlindSpotDetector /> 
        
        <div class="gamification-panel">
            <h3>🏆 My Achievements</h3>

            <div class="stat-box">
                <h4>🔥 Daily Streak</h4>
                <p class="stat-value">{{ streak }} Days</p>
            </div>

            <div class="stat-box">
                <h4>💯 Questions Answered</h4>
                <progress :value="totalAnswered" max="100"></progress>
                <p>{{ totalAnswered }} / 100</p>
            </div>

            <div class="badges-area">
                <h4>Badges Unlocked:</h4>
                <div v-if="badges.includes('Q100_MASTER')" class="badge-icon">
                    🥇 **100 Q Master**
                </div>
                <div v-else class="badge-placeholder">
                    Keep quizzing to earn your first badge!
                </div>
            </div>
        </div>
        
        <div class="current-stats"> 
            <h3>Current Profile Data</h3>
            <p><strong>Difficulty:</strong> {{ authStore.userProfile.difficulty_level }}</p>
            <p><strong>Subjects:</strong> {{ authStore.userProfile.subjects_of_interest.join(', ') || 'None selected' }}</p>
        </div>
        
        <div class="final-scroll-spacer"></div>

    </div>
    <div v-else>
        <p>Loading profile data... Please ensure you are logged in.</p>
    </div>
</template>

<style scoped>
/* --- Profile Card Styling --- */
.intro-text {
    margin-bottom: 30px;
    color: var(--color-text); /* Theme variable */
    text-align: center;
}
.profile-card {
    padding: 30px;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    background-color: var(--color-card-bg); 
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: var(--color-text); 
}

/* --- Input and Select Fields FIX --- */
select {
    width: 100%;
    padding: 10px;
    /* Theme variables for proper contrast in all modes */
    border: 1px solid var(--color-border); 
    background-color: var(--color-background); 
    color: var(--color-text);
    border-radius: 4px;
    
}
/* Ensure option buttons/checkboxes also use theme variables */
.subject-checkbox {
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    padding: 8px 15px;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    font-size: 0.9em;
    user-select: none;
    display: flex;
    align-items: center;
    color: var(--color-text); /* Use text color */
}

.subject-checkbox.checked {
    background-color: var(--color-primary); /* Use primary theme color for checked state */
    border-color: var(--color-primary);
    color: white; /* Keep white text for high contrast on primary color */
}

/* --- Button Styling (Kept as high-contrast constants) --- */
button {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: white;
    border: none;
    border-radius: 12px; 
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #27ae60; 
    transform: translateY(0);
}

button:hover:not(:disabled) {
    background-color: #27ae60; 
}
/* ... rest of button styles ... */

.success-message {
    color: #2ecc71;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.error-message {
    color: #e74c3c;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

/* --- Gamification Panel Styling (Now fully consistent) --- */
.gamification-panel {
    border: 1px solid var(--color-border);
    padding: 20px;
    border-radius: 8px;
    background: var(--color-card-bg); 
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
.gamification-panel h3 {
    border-bottom: 2px solid #9b59b6;
    padding-bottom: 10px;
    margin-bottom: 20px;
    color: #9b59b6;
}
.stat-box {
    margin-bottom: 15px;
}
.stat-value {
    font-size: 1.5em;
    font-weight: bold;
    color: var(--color-primary);
}
/* ... rest of gamification styles ... */

/* --- Current Stats Styling FIX --- */
.current-stats {
    margin-top: 40px;
    padding: 20px;
    /* Use theme variables for light/dark mode compatibility */
    background-color: var(--color-border); /* Use border color as a subtle background */
    border: 1px solid var(--color-primary); 
    border-radius: 8px;
    font-size: 0.9em;
    color: var(--color-text); /* Use main text color */
}

/* Ensure inner elements use theme text color */
.current-stats h3, .current-stats strong {
    color: var(--color-text);
}

/* --- CRITICAL SCROLL FIX CSS --- */
.final-scroll-spacer {
    height: 100px; /* Forces 100px of empty space below the final element */
    width: 100%;
}
</style>