


 <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; 

// CRITICAL FIX: Import LineChart
import { LineChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables); 

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const leaderboard = ref<any[]>([]); // State for leaderboard data
const isLoading = ref(true);
const errorMsg = ref('');

// --- Chart Options (Updated to use theme variables) ---
const chartOptions = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top' as const,
            labels: {
                color: 'var(--color-text)', // Use theme variable
            },
        },
        title: {
            display: true,
            text: 'Top Users Accuracy Comparison',
            color: 'var(--color-primary)', // Use theme variable
            font: {
                size: 18,
            },
        },
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'User Rank',
                color: 'var(--color-text)', // Use theme variable
            },
            ticks: {
                color: 'var(--color-text)', // Use theme variable
                // Displaying the Rank as the label
                callback: function(this: any, val: any, index: number) {
                    if (index === 0) return 'Start';
                    if (leaderboard.value.length > 0) {
                          // Use a placeholder for the X-axis label on the second point
                          return leaderboard.value[0].email.substring(0, leaderboard.value[0].email.indexOf('@')) + '...'; 
                    }
                    return '';
                }
            },
            grid: {
                color: 'var(--color-border)', // Use theme variable
            },
        },
        y: {
            title: {
                display: true,
                text: 'Accuracy (%)',
                color: 'var(--color-text)', // Use theme variable
            },
            ticks: {
                color: 'var(--color-text)', // Use theme variable
                callback: (value: any) => `${value}%`, 
                stepSize: 10,
            },
            min: 0,
            max: 100,
            grid: {
                color: 'var(--color-border)', // Use theme variable
            },
        },
    },
}));


// --- Chart Data computed property (CRITICAL FIX) ---
const chartData = computed(() => {
    // Define colors for visual rank distinction
    const colors = [
        '#3498db', // Rank 1: Blue
        '#2ecc71', // Rank 2: Green
        '#e74c3c', // Rank 3: Red
        '#9b59b6', // Rank 4: Purple
        '#f1c40f'  // Rank 5: Gold
    ];
    
    // Generate a separate dataset for *each user*
    const datasets = leaderboard.value.map((user, index) => {
        const userColor = colors[index % colors.length]; 
        
        return {
            label: `${user.email.substring(0, user.email.indexOf('@'))} (${user.accuracy}%)`,
            // CRITICAL FIX: Use [0, user.accuracy] to force a line to be drawn from the baseline (0)
            data: [0, user.accuracy], 
            fill: false, 
            borderColor: userColor,
            tension: 0.4, 
            pointBackgroundColor: userColor,
            pointRadius: 8,
            pointHoverRadius: 10,
        };
    });

    // CRITICAL FIX: The X-axis labels must match the two points in the data array: [0, user.accuracy]
    const labels = ['Start', 'Accuracy']; 

    return {
        labels: labels, 
        datasets: datasets,
    };
});


// --- Fetch Admin Statistics & Leaderboard (Remains the same) ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        // 1. Fetch global stats (Route 12)
        const statsResponse = await axios.get(
            'http://localhost:5000/api/admin/stats',
            authStore.authHeader
        );
        stats.value = statsResponse.data;

        // 2. Fetch leaderboard data (Route 19)
        const leaderboardResponse = await axios.get(
            'http://localhost:5000/api/admin/leaderboard',
            authStore.authHeader
        );
        leaderboard.value = leaderboardResponse.data; 

    } catch (error: any) {
        errorMsg.value = 'Failed to load dashboard data. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Dashboard Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// Handler for content review (placeholder)
const goToContentReview = () => {
    alert("Navigating to Content Review (Feature placeholder).");
};
</script>

<template>
  <div class="admin-container">
    <h1><span class="emoji">👑</span> Admin Dashboard</h1>
    <p class="subtitle">Platform Health and Performance Overview</p>

    <div v-if="isLoading" class="loading-state">Loading system metrics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else>
        <div class="dashboard-grid">
            
            <div class="stat-card stat-primary">
                <p class="card-label">Overall Accuracy</p>
                <span class="card-value">{{ stats.overall_accuracy_percent }}%</span>
                <p class="card-detail">System average across all quizzes.</p>
            </div>

            <div class="stat-card">
                <p class="card-label">Total Users</p>
                <span class="card-value">{{ stats.total_users }}</span>
            </div>

            <div class="stat-card">
                <p class="card-label">Total Quizzes Taken</p>
                <span class="card-value">{{ stats.total_interactions }}</span>
            </div>

            <div class="stat-card">
                <p class="card-label">Content Items Uploaded</p>
                <span class="card-value">{{ stats.total_content_items }}</span>
            </div>

        </div>

        <div class="admin-actions">
            
            <h2 class="leaderboard-title">📊 Top Users Performance Comparison</h2>
            
            <div class="chart-container">
                <LineChart 
                    v-if="leaderboard.length > 0" 
                    :chartData="chartData" 
                    :options="chartOptions" 
                />
                <div v-else class="no-chart-data">No sufficient data to display the chart.</div>
            </div>
            
            <div class="leaderboard-card stat-card">
                <table v-if="leaderboard.length > 0" class="leaderboard-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>User Email</th>
                            <th>Accuracy</th>
                            <th>Attempts</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in leaderboard" :key="user.user_id" :class="[`rank-${user.rank}`]">
                            <td>{{ user.rank }}</td>
                            <td>{{ user.email.substring(0, user.email.indexOf('@')) }}...</td>
                            <td :class="{'score-high': user.accuracy >= 70}">{{ user.accuracy }}%</td>
                            <td>{{ user.total_attempts }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>


            <h2>Content Quality & Feedback Management</h2>
            
            <RouterLink :to="{ name: 'moderationQueue' }" class="action-btn-moderation router-link">
                    <span class="emoji">🚨</span> Review Question Flags (0)
            </RouterLink>
            
            <RouterLink :to="{ name: 'contentManagement' }" class="action-btn-secondary router-link">
                    <span class="emoji">📚</span> Manage User Content
            </RouterLink>
        </div>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: var(--color-text); /* Use theme variable */
    text-align: center;
}
.subtitle {
    color: var(--color-text); /* Use theme variable */
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: var(--color-primary); /* Use theme variable */
    padding: 20px;
    background-color: var(--color-card-bg); /* Use theme variable */
    border-radius: 10px;
}

/* --- DASHBOARD GRID --- */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
}

.stat-card {
    background-color: var(--color-card-bg); /* Use theme variable */
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid var(--color-primary); /* Use theme variable */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green highlight for accuracy */
}

.card-label {
    font-size: 0.9rem;
    color: var(--color-text); /* Use theme variable */
    opacity: 0.7;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: var(--color-text); /* Use theme variable */
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: var(--color-text); /* Use theme variable */
    opacity: 0.5;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS & LEADERBOARD STYLES --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: var(--color-background); /* Use background variable for clean separation */
    border-radius: 12px;
}
.admin-actions h2 {
    color: var(--color-primary); /* Use theme variable */
    margin-bottom: 20px;
    font-size: 1.5rem;
}

/* LEADERBOARD CHART CONTAINER */
.chart-container {
    padding: 15px;
    background-color: var(--color-card-bg); /* Use theme variable */
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: left; 
    border: 1px solid var(--color-border);
}

.leaderboard-title {
    color: var(--color-primary); /* Use theme primary color */
    font-size: 1.6rem;
    margin-bottom: 20px;
    text-align: center;
}

.no-chart-data {
    color: var(--color-text);
    text-align: center;
    padding: 20px;
    font-style: italic;
}

/* LEADERBOARD TABLE STYLES */
.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    color: var(--color-text);
    margin-top: 20px;
}
.leaderboard-table th, .leaderboard-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid var(--color-border); /* Use theme variable */
    font-size: 0.9rem;
}

.leaderboard-table thead th {
    color: var(--color-primary);
    font-weight: bold;
}

/* Dynamic Row Coloring (Using fixed colors for rank highlighting) */
.leaderboard-table tr.rank-1 td { color: #3498db; background-color: #3498db1a; font-weight: bold; }
.leaderboard-table tr.rank-2 td { color: #2ecc71; background-color: #2ecc711a; }
.leaderboard-table tr.rank-3 td { color: #e74c3c; background-color: #e74c3c1a; }

.score-high {
    color: #2ecc71; 
}

/* --- ACTION BUTTONS (MODERATION/MANAGEMENT) --- */
.action-btn-moderation, .action-btn-secondary {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
}

/* Ensure RouterLink inherits button styling */
.router-link {
    display: block; 
    text-decoration: none;
    text-align: center;
    color: white !important; /* Force white text for high contrast on buttons */
}

.action-btn-moderation {
    background-color: #e74c3c; 
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; 
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style>
 








































