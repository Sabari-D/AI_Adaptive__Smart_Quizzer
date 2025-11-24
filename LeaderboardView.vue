
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const leaderboard = ref<any[]>([]);
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Live Leaderboard Data (Route 19) ---
const fetchLeaderboard = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/leaderboard', // Route 19
            authStore.authHeader
        );
        leaderboard.value = response.data;
    } catch (error: any) {
        errorMsg.value = 'Failed to load leaderboard. Server may be down or data unavailable.';
        console.error("Leaderboard Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchLeaderboard);
</script>

<template>
  <div class="leaderboard-page-container">
    <h1>🏆 Live Adaptive Quiz Leaderboard</h1>
    <p class="subtitle">Ranked by overall accuracy across all quizzes taken.</p>

    <div v-if="isLoading" class="loading-state">Fetching live scores...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    <div v-else-if="leaderboard.length === 0" class="empty-state">
        <p>No quiz activity has been recorded yet.</p>
    </div>
    
    <div v-else class="leaderboard-card">
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>User</th>
                    <th>Accuracy</th>
                    <th>Attempts</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in leaderboard" :key="user.user_id" :class="[`rank-${user.rank}`]">
                    <td class="rank-cell">{{ user.rank }}</td>
                    <td>{{ user.email.substring(0, user.email.indexOf('@')) }}...</td>
                    <td class="accuracy-cell">{{ user.accuracy }}%</td>
                    <td>{{ user.total_attempts }}</td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<style scoped>
.leaderboard-page-container {
    max-width: 800px;
    margin: 50px auto;
    color: var(--color-text); /* Use theme variable */
    text-align: center;
}
h1 {
    color: var(--color-primary); /* Use theme variable */
    text-shadow: 0 0 5px var(--color-primary);
    margin-bottom: 5px;
}
.subtitle {
    color: var(--color-text);
    opacity: 0.8;
    margin-bottom: 30px;
}

.leaderboard-card {
    /* Use theme variables for card background and border */
    background-color: var(--color-card-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    border: 1px solid var(--color-border);
}

.loading-state, .error-state, .empty-state {
    color: var(--color-text);
    background-color: var(--color-card-bg);
    padding: 20px;
    border-radius: 12px;
}

.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    color: var(--color-text); /* Table text uses theme color */
}

.leaderboard-table th, .leaderboard-table td {
    padding: 15px 10px;
    text-align: left;
    border-bottom: 1px solid var(--color-border); /* Use theme variable for border */
    font-size: 1rem;
}

.leaderboard-table th {
    color: var(--color-primary);
    font-weight: bold;
}

.rank-cell {
    font-weight: 800;
}

/* --- RANK COLORING SCHEME (Applying color to row cells) --- */

/* Base Rank highlight color and background tint */
.leaderboard-table tr.rank-1 { background-color: #3498db1a; }
.leaderboard-table tr.rank-2 { background-color: #2ecc711a; }
.leaderboard-table tr.rank-3 { background-color: #e74c3c1a; }
.leaderboard-table tr.rank-4 { background-color: #9b59b61a; }
.leaderboard-table tr.rank-5 { background-color: #f1c40f1a; }

/* Applying strong foreground color to specific data points (Rank and Accuracy) */
.leaderboard-table tr.rank-1 .rank-cell, .leaderboard-table tr.rank-1 .accuracy-cell {
    color: #3498db; /* Blue */
}

.leaderboard-table tr.rank-2 .rank-cell, .leaderboard-table tr.rank-2 .accuracy-cell {
    color: #2ecc71; /* Green */
}

.leaderboard-table tr.rank-3 .rank-cell, .leaderboard-table tr.rank-3 .accuracy-cell {
    color: #e74c3c; /* Red */
}

.leaderboard-table tr.rank-4 .rank-cell, .leaderboard-table tr.rank-4 .accuracy-cell {
    color: #9b59b6; /* Purple */
}

.leaderboard-table tr.rank-5 .rank-cell, .leaderboard-table tr.rank-5 .accuracy-cell {
    color: #f1c40f; /* Gold */
}

</style>



