


<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useQuizStore } from '@/stores/quiz_store'; 
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const quizStore = useQuizStore();
const router = useRouter();

// State
const contentList = ref<any[]>([]);
const selectedContentId = ref<string | null>(null);
const numQuestions = ref(10); // Default to 10 questions
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Content List ---
const fetchContentList = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    try {
        const response = await axios.get(
            'http://localhost:5000/api/content/list',
            authStore.authHeader
        );
        contentList.value = response.data;
        if (contentList.value.length > 0) {
            // Select the most recently uploaded content by default (or the first one)
            selectedContentId.value = contentList.value[0]._id; 
        }
    } catch (error: any) {
        // The message is displayed to the user if the fetch fails
        errorMsg.value = 'Failed to load content list. Please upload notes.';
    } finally {
        isLoading.value = false;
    }
};

// --- Start Quiz Action ---
const startQuiz = () => {
    // 1. Basic Validation
    if (!selectedContentId.value) {
        errorMsg.value = "Please select a set of notes.";
        return;
    }
    if (numQuestions.value < 1) {
        errorMsg.value = "Please enter a valid number of questions.";
        return;
    }
    
    // 2. Pass the required configuration to the store
    quizStore.setConfig(selectedContentId.value, numQuestions.value);
    
    // 3. Navigate to the Active Quiz Runner page
    router.push({ name: 'activeQuiz' }); 
};

// --- Analytics Handler (CRITICAL: Navigation logic) ---
const viewAnalytics = () => {
    router.push({ name: 'analytics' });
};

onMounted(fetchContentList);
</script>

<template>
    <div class="quiz-config-container">
        <h1>Get ready to begin your Quiz</h1>

        <div class="config-card">
            <p class="section-subtitle">Select the material and quiz length.</p>

            <div v-if="isLoading">Loading content...</div>
            <div v-else-if="contentList.length === 0" class="empty-state">
                No notes found. Please <router-link to="/content">Upload Notes</router-link> first!
            </div>
            <div v-else>
                <div class="form-group">
                    <label for="contentSelect">Study Material:</label>
                    <select v-model="selectedContentId" id="contentSelect" class="content-select">
                        <option v-for="content in contentList" :key="content._id" :value="content._id">
                            {{ content.title }} ({{ content.chunk_count }} Chunks)
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="numQuestions">Number of Questions (1-50):</label>
                    <input type="number" id="numQuestions" v-model.number="numQuestions" min="1" max="50">
                </div>
                
                <p class="note">Difficulty: <strong class="difficulty">{{ authStore.userProfile?.difficulty_level || 'Intermediate' }}</strong> (Set in Profile)</p>
                
                <button @click="startQuiz" :disabled="!selectedContentId || numQuestions < 1" class="start-btn">
                    Start Quiz Generation
                </button>
            </div>
            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<style scoped>
/* Use theme variables for the container text */
.quiz-config-container {
    max-width: 600px;
    margin: 50px auto;
    text-align: center;
}

h1 {
    /* Use primary color for headings */
    color: var(--color-primary); 
    margin-bottom: 40px;
    text-shadow: 0 0 5px var(--color-primary);
}

.config-card {
    /* Use theme variables for card background and border */
    background-color: var(--color-card-bg);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    margin-bottom: 20px;
    border: 1px solid var(--color-border);
}

.section-subtitle {
    color: var(--color-text); /* Use theme text color */
    margin-bottom: 20px;
    font-size: 1.1rem;
    text-align: center;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: var(--color-text); /* Use theme text color */
}

input[type="number"], .content-select {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    /* Use theme variables for input fields */
    background-color: var(--color-background); 
    color: var(--color-text);
    border: 1px solid var(--color-border);
    font-size: 1rem;
    box-sizing: border-box;
}

.note {
    color: var(--color-text); /* Use theme text color */
    font-size: 1rem;
    margin-top: 20px;
    margin-bottom: 25px;
    text-align: center;
}

.difficulty {
    color: #f1c40f; /* Specific highlight color */
}

.empty-state {
    color: #e74c3c;
    margin: 30px 0;
    text-align: center;
}

.start-btn {
    width: 100%;
    padding: 14px; 
    background-color: #2ecc71; /* Green for Start */
    color: #1a1a2e; /* Black/dark color for button text */
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
    transition: all 0.15s ease;
    box-shadow: 0 6px 0 #219d5c;
    transform: translateY(0);
    margin-top: 20px;
}

.start-btn:active {
    box-shadow: 0 2px 0 #219d5c;
    transform: translateY(4px);
}

.error-message {
    color: #e74c3c;
    margin-top: 15px;
    text-align: center;
}

</style>
