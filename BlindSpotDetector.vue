<template>
    <div :class="['blindspot-card', blindSpot.severity]">
        <h3>🧠 Cognitive Blind Spot Detector</h3>
        <p class="status-title">{{ blindSpot.type }}</p>
        
        <div class="suggestion-area">
            <p v-if="blindSpot.type === 'Initial State'">{{ blindSpot.suggestion }}</p>
            <p v-else class="suggestion-text" v-html="blindSpot.suggestion"></p>
        </div>
        
        <button @click="fetchBlindSpot" :disabled="loading" class="refresh-btn">
            {{ loading ? 'Analyzing...' : 'Re-analyze Blind Spots' }}
        </button>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const API_URL = 'http://localhost:5000/api'; 

interface BlindSpot {
    type: string;
    suggestion: string;
    severity?: 'High' | 'Medium' | 'Low' | 'Initial State' | 'Clear Cognitive State';
}

const blindSpot = ref<BlindSpot>({
    type: 'Loading...',
    suggestion: 'Running deep diagnostic analysis...',
    severity: 'Initial State'
});
const loading = ref(false);

async function fetchBlindSpot() {
    if (!authStore.isAuthenticated) return;
    loading.value = true;
    try {
        const url = `${API_URL}/analytics/blindspot`;
        // Use authStore.authHeader to send the JWT token
        const response = await axios.get(url, authStore.authHeader);
        
        blindSpot.value = response.data;
        
    } catch (error) {
        console.error("Blindspot fetch failed:", error);
        blindSpot.value = {
            type: 'Error',
            suggestion: 'Could not load diagnostic analysis. Ensure the Flask server is running and data exists.',
            severity: 'High'
        };
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    fetchBlindSpot();
});
</script>

<style scoped>
.blindspot-card {
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-align: left;
    margin-top: 30px;
    transition: all 0.3s ease;
    border-left: 5px solid;
    /* Use CSS variables for theme compatibility */
    background-color: var(--color-card-bg); 
}

h3 {
    color: var(--color-primary);
    margin-top: 0;
    margin-bottom: 10px;
}

.status-title {
    font-size: 1.1em;
    font-weight: bold;
    margin-bottom: 15px;
    color: var(--color-text);
}

/* Severity Indicators */
.High { border-color: #e74c3c; } 
.High .status-title { color: #e74c3c; }

.Medium { border-color: #f39c12; } 
.Medium .status-title { color: #f39c12; }

.Low { border-color: #f1c40f; } 
.Low .status-title { color: #f1c40f; }

.Clear { border-color: #2ecc71; } 
.Clear .status-title { color: #2ecc71; }

.suggestion-text {
    line-height: 1.6;
    margin-bottom: 20px;
}

.refresh-btn {
    background-color: #3498db;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;
}
.refresh-btn:hover:not(:disabled) {
    background-color: #2980b9;
}
.refresh-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>