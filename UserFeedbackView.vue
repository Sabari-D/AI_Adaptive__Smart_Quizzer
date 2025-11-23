<!-- <script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

// Form State
const experience = ref('ok'); // Default to 'ok'
const rating = ref(3); // Default to 3 stars
const suggestion = ref('');
const statusMessage = ref('');
const isLoading = ref(false);

const experienceOptions = [
    { value: 5, label: 'Very Good' },
    { value: 4, label: 'Good' },
    { value: 3, label: 'Okay' },
    { value: 2, label: 'Poor' },
    { value: 1, label: 'Very Poor' },
];

// Function to handle star click
const setRating = (starValue: number) => {
    rating.value = starValue;
};

// Function to submit feedback
const submitFeedback = async () => {
    statusMessage.value = '';
    
    if (!suggestion.value.trim()) {
        statusMessage.value = '❌ Please provide a suggestion.';
        return;
    }

    isLoading.value = true;
    
    const payload = {
        experience_rating: experience.value,
        star_rating: rating.value,
        suggestion_text: suggestion.value,
    };

    try {
        await axios.post(
            'http://localhost:5000/api/feedback/submit',
            payload,
            authStore.authHeader 
        );

        statusMessage.value = '✅ Feedback submitted successfully! Redirecting in 3 seconds...';
        
        // Clear form after success
        experience.value = 'ok';
        rating.value = 3;
        suggestion.value = '';

        // Redirect back to profile after a short delay
        setTimeout(() => {
            router.push('/profile');
        }, 3000);

    } catch (error: any) {
        statusMessage.value = '❌ Error submitting feedback. Check your session.';
        console.error('Feedback submission failed:', error);
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
  <div class="feedback-container">
    <h1>📝 Feedback</h1>
    <p class="subtitle">Help us improve the Smart Quizzer adaptive engine and user interface.</p>

    <div class="feedback-card">
        <form @submit.prevent="submitFeedback">

            <div class="form-group">
                <label class="group-label">How was the overall experience?</label>
                <div class="radio-group">
                    <label v-for="option in experienceOptions" :key="option.value" class="radio-label">
                        <input type="radio" :value="option.label" v-model="experience" required>
                        {{ option.label }}
                    </label>
                </div>
            </div>

            <div class="form-group">
                <label class="group-label">Rate your satisfaction (1-5 Stars):</label>
                <div class="star-rating">
                    <span 
                        v-for="star in 5" 
                        :key="star" 
                        @click="setRating(star)"
                        :class="{ 'star-filled': star <= rating }"
                        class="star-icon"
                    >
                        ★
                    </span>
                </div>
                <p class="current-rating">Current Rating: {{ rating }} out of 5</p>
            </div>

            <div class="form-group">
                <label for="suggestionText" class="group-label">Your Suggestions for Improvement:</label>
                <textarea 
                    id="suggestionText" 
                    v-model="suggestion" 
                    rows="5" 
                    placeholder="E.g., The adaptive selection is great, but the Fill-up questions need better spacing."></textarea>
            </div>

            <p v-if="statusMessage" :class="{'success-message': statusMessage.startsWith('✅'), 'error-message': statusMessage.startsWith('❌') }">
                {{ statusMessage }}
            </p>

            <button type="submit" :disabled="isLoading">
                <span v-if="isLoading">Submitting...</span>
                <span v-else>Submit Feedback</span>
            </button>
        </form>
    </div>
  </div>
</template>

<style scoped>
.feedback-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 30px;
}
.feedback-card {
    background-color: #2a2a44;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
}
.form-group {
    margin-bottom: 25px;
}
.group-label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    color: #e0e0e0;
    font-size: 1.1rem;
}

/* --- Radio Button Styling --- */
.radio-group {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}
.radio-label {
    flex-grow: 1;
    display: block;
    text-align: center;
    padding: 10px 5px;
    background-color: #3e3e5a;
    border: 2px solid #3e3e5a;
    border-radius: 8px;
    color: #c0c0c0;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
}
.radio-label:has(input:checked) {
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}
.radio-label input {
    display: none;
}

/* --- Star Rating Styling --- */
.star-rating {
    font-size: 2.5rem;
    color: #777;
    margin-bottom: 5px;
    text-align: center;
}
.star-icon {
    cursor: pointer;
    transition: color 0.2s;
    margin: 0 5px;
    color: #f39c12; /* Default gold color */
}
.star-filled {
    color: #f1c40f; 
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}
.current-rating {
    text-align: center;
    color: #9b59b6;
    font-style: italic;
    font-size: 0.9rem;
}

/* --- Text Area Styling --- */
textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #555;
    border-radius: 8px;
    background-color: #3e3e5a;
    color: #fff;
    box-sizing: border-box;
    resize: vertical;
}

/* --- Button Styling --- */
button[type="submit"] {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: #1a1a2e; 
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
}
button[type="submit"]:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
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





<!-- <script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter(); // Correct local instance of router

// Form State
const experience = ref('ok'); // Default to 'ok'
const rating = ref(3); // Default to 3 stars
const suggestion = ref('');
const statusMessage = ref('');
const isLoading = ref(false);

const experienceOptions = [
    { value: 5, label: 'Very Good' },
    { value: 4, label: 'Good' },
    { value: 3, label: 'Okay' },
    { value: 2, label: 'Poor' },
    { value: 1, label: 'Very Poor' },
];

// Function to handle star click
const setRating = (starValue: number) => {
    rating.value = starValue;
};

// Function to submit feedback
const submitFeedback = async () => {
    statusMessage.value = '';
    
    if (!suggestion.value.trim()) {
        statusMessage.value = '❌ Please provide a suggestion.';
        return;
    }

    isLoading.value = true;
    
    const payload = {
        experience_rating: experience.value,
        star_rating: rating.value,
        suggestion_text: suggestion.value,
    };

    try {
        await axios.post(
            'http://localhost:5000/api/feedback/submit',
            payload,
            authStore.authHeader 
        );

        statusMessage.value = '✅ Feedback submitted successfully! Redirecting in 3 seconds...';
        
        // Clear form after success
        experience.value = 'ok';
        rating.value = 3;
        suggestion.value = '';

        // Redirect back to profile after a short delay
        setTimeout(() => {
            router.push('/profile');
        }, 3000);

    } catch (error: any) {
        statusMessage.value = '❌ Error submitting feedback. Check your session.';
        console.error('Feedback submission failed:', error);
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
  <div class="feedback-container">
    <h1>📝 Feedback</h1>
    <p class="subtitle">Help us improve the Smart Quizzer adaptive engine and user interface.</p>

    <div class="feedback-card">
        <form @submit.prevent="submitFeedback">

            <div class="form-group">
                <label class="group-label">How was the overall experience?</label>
                <div class="radio-group">
                    <label v-for="option in experienceOptions" :key="option.value" class="radio-label">
                        <input type="radio" :value="option.label" v-model="experience" required>
                        {{ option.label }}
                    </label>
                </div>
            </div>

            <div class="form-group">
                <label class="group-label">Rate your satisfaction (1-5 Stars):</label>
                <div class="star-rating">
                    <span 
                        v-for="star in 5" 
                        :key="star" 
                        @click="setRating(star)"
                        :class="{ 'star-filled': star <= rating }"
                        class="star-icon"
                    >
                        ★
                    </span>
                </div>
                <p class="current-rating">Current Rating: {{ rating }} out of 5</p>
            </div>

            <div class="form-group">
                <label for="suggestionText" class="group-label">Your Suggestions for Improvement:</label>
                <textarea 
                    id="suggestionText" 
                    v-model="suggestion" 
                    rows="5" 
                    placeholder="E.g., The adaptive selection is great, but the Fill-up questions need better spacing."></textarea>
            </div>

            <p v-if="statusMessage" :class="{'success-message': statusMessage.startsWith('✅'), 'error-message': statusMessage.startsWith('❌') }">
                {{ statusMessage }}
            </p>

            <button type="submit" :disabled="isLoading">
                <span v-if="isLoading">Submitting...</span>
                <span v-else>Submit Feedback</span>
            </button>
        </form>
    </div>
  </div>
</template>

<style scoped>
.feedback-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}
h1 {
    color: var(--color-primary);
    margin-bottom: 5px;
}
.subtitle {
    color: var(--color-text); /* Use theme variable */
    margin-bottom: 30px;
}
.feedback-card {
    /* Use theme variables for card background and border */
    background-color: var(--color-card-bg);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    border: 1px solid var(--color-border);
    text-align: left;
}
.form-group {
    margin-bottom: 25px;
}
.group-label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
    color: var(--color-text); /* Use theme variable */
    font-size: 1.1rem;
}

/* --- Radio Button Styling (Optimized for theme) --- */
.radio-group {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}
.radio-label {
    flex-grow: 1;
    display: block;
    text-align: center;
    padding: 10px 5px;
    /* Use theme variables for base button state */
    background-color: var(--color-background);
    border: 2px solid var(--color-border);
    border-radius: 8px;
    color: var(--color-text);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
}
.radio-label:has(input:checked) {
    /* Hardcoded primary color for selected state */
    background-color: #3498db;
    border-color: #2980b9;
    color: white;
}
.radio-label input {
    display: none;
}

/* --- Star Rating Styling --- */
.star-rating {
    font-size: 2.5rem;
    color: #777;
    margin-bottom: 5px;
    text-align: center;
}
.star-icon {
    cursor: pointer;
    transition: color 0.2s;
    margin: 0 5px;
    color: var(--color-text); /* Default color should respect theme */
    opacity: 0.3;
}
.star-filled {
    color: #f1c40f; /* Fixed gold color */
    opacity: 1;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}
.current-rating {
    text-align: center;
    color: var(--color-primary); /* Use primary color */
    font-style: italic;
    font-size: 0.9rem;
}

/* --- Text Area Styling --- */
textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    /* Use theme variables for input contrast */
    background-color: var(--color-background);
    color: var(--color-text);
    box-sizing: border-box;
    resize: vertical;
}

/* --- Button Styling --- */
button[type="submit"] {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; 
    color: #1a1a2e; /* Fixed dark text for contrast on green */
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
}
button[type="submit"]:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
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















<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter(); 

// Form State
const experience = ref('Okay'); // Default to 'Okay' (Matching label value)
const rating = ref(3); // Default to 3 stars
const suggestion = ref('');
const statusMessage = ref('');
const isLoading = ref(false);

const experienceOptions = [
  { value: 5, label: 'Very Good' },
  { value: 4, label: 'Good' },
  { value: 3, label: 'Okay' },
  { value: 2, label: 'Poor' },
  { value: 1, label: 'Very Poor' },
];

// Function to handle star click
const setRating = (starValue: number) => {
  rating.value = starValue;
};

// Function to submit feedback
const submitFeedback = async () => {
  statusMessage.value = '';
  
  if (!suggestion.value.trim()) {
    statusMessage.value = '❌ Please provide a suggestion.';
    return;
  }

  isLoading.value = true;
  
  // *** CORRECTION APPLIED HERE ***
  // Changed the payload key from 'star_rating' back to 'rating' to match app.py
  const payload = {
    experience_rating: experience.value, 
    rating: rating.value,          
    suggestions: suggestion.value,      
  };

  try {
    await axios.post(
      'http://localhost:5000/api/feedback/submit',
      payload,
      authStore.authHeader 
    );

    statusMessage.value = '✅ Feedback submitted successfully! Redirecting in 3 seconds...';
    
    // Clear form after success
    experience.value = 'Okay';
    rating.value = 3;
    suggestion.value = '';

    // Redirect back to profile after a short delay
    setTimeout(() => {
      router.push('/profile');
    }, 3000);

  } catch (error: any) {
    statusMessage.value = '❌ Error submitting feedback. Check your session.';
    console.error('Feedback submission failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="feedback-container">
    <h1>📝 Feedback</h1>
    <p class="subtitle">Help us improve the Smart Quizzer adaptive engine and user interface.</p>

    <div class="feedback-card">
      <form @submit.prevent="submitFeedback">

        <div class="form-group">
          <label class="group-label">How was the overall experience?</label>
          <div class="radio-group">
            <label v-for="option in experienceOptions" :key="option.value" class="radio-label">
              <input type="radio" :value="option.label" v-model="experience" required>
              {{ option.label }}
            </label>
          </div>
        </div>

        <div class="form-group">
          <label class="group-label">Rate your satisfaction (1-5 Stars):</label>
          <div class="star-rating">
            <span 
              v-for="star in 5" 
              :key="star" 
              @click="setRating(star)"
              :class="{ 'star-filled': star <= rating }"
              class="star-icon"
            >
              ★
            </span>
          </div>
          <p class="current-rating">Current Rating: {{ rating }} out of 5</p>
        </div>

        <div class="form-group">
          <label for="suggestionText" class="group-label">Your Suggestions for Improvement:</label>
          <textarea 
            id="suggestionText" 
            v-model="suggestion" 
            rows="5" 
            placeholder="E.g., The adaptive selection is great, but the Fill-up questions need better spacing."></textarea>
        </div>

        <p v-if="statusMessage" :class="{'success-message': statusMessage.startsWith('✅'), 'error-message': statusMessage.startsWith('❌') }">
          {{ statusMessage }}
        </p>

        <button type="submit" :disabled="isLoading">
          <span v-if="isLoading">Submitting...</span>
          <span v-else>Submit Feedback</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.feedback-container {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
}

h1 {
  color: var(--color-primary);
  margin-bottom: 5px;
}

.subtitle {
  color: var(--color-text);
  margin-bottom: 30px;
}

.feedback-card {
  background-color: var(--color-card-bg);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  border: 1px solid var(--color-border);
  text-align: left;
}

.form-group {
  margin-bottom: 25px;
}

.group-label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: var(--color-text);
  font-size: 1.1rem;
}

/* --- Radio Button Styling --- */
.radio-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.radio-label {
  flex-grow: 1;
  display: block;
  text-align: center;
  padding: 10px 5px;
  background-color: var(--color-background);
  border: 2px solid var(--color-border);
  border-radius: 8px;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.radio-label:hover {
  border-color: var(--color-primary);
}

.radio-label:has(input:checked) {
  background-color: #9b59b6; 
  border-color: #8e44ad;
  color: white;
}

.radio-label input {
  display: none;
}

/* --- Star Rating Styling --- */
.star-rating {
  font-size: 2.5rem;
  color: #777;
  margin-bottom: 5px;
  text-align: center;
}

.star-icon {
  cursor: pointer;
  transition: color 0.2s;
  margin: 0 5px;
  color: var(--color-text);
  opacity: 0.3;
}

.star-filled {
  color: #f1c40f; 
  opacity: 1;
  text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.current-rating {
  text-align: center;
  color: var(--color-primary);
  font-style: italic;
  font-size: 0.9rem;
}

/* --- Text Area Styling --- */
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background);
  color: var(--color-text);
  box-sizing: border-box;
  resize: vertical;
  box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.4);
}

/* --- Button Styling --- */
button[type="submit"] {
  width: 100%;
  padding: 14px; 
  background-color: #2ecc71; 
  color: #1a1a2e;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 700;
  transition: all 0.15s ease;
  box-shadow: 0 6px 0 #219d5c;
  transform: translateY(0);
}

button[type="submit"]:active {
  box-shadow: 0 2px 0 #219d5c;
  transform: translateY(4px);
}

button[type="submit"]:disabled {
  background-color: #3e3a51;
  box-shadow: none;
  cursor: not-allowed;
  transform: translateY(0);
  color: #959595;
}

.success-message {
  color: #2ecc71;
  background-color: rgba(46, 204, 113, 0.1);
  border: 1px solid #2ecc71;
  padding: 10px;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 15px;
}

.error-message {
  color: #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
  border: 1px solid #e74c3c;
  padding: 10px;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 15px;
}
</style>