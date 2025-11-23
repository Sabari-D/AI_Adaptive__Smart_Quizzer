<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// Handler for the moderation button (Future implementation)
const goToModeration = () => {
    alert("Navigating to Question Moderation Queue (Feature placeholder).");
    // router.push({ name: 'moderationQueue' }); // Future route
};

// Handler for the moderation button (Future implementation)
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
    
    <div v-else class="dashboard-grid">
        
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
        <h2>Content Quality & Feedback Management</h2>
        
        <button @click="goToModeration" class="action-btn-moderation">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </button>
        
        <button @click="goToContentReview" class="action-btn-secondary">
             <span class="emoji">📚</span> Manage User Content
        </button>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
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

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style> -->







<!-- 

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; // CRITICAL: Import RouterLink

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// Handler for content review (still an alert, but kept separate for structure)
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
    
    <div v-else class="dashboard-grid">
        
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
        <h2>Content Quality & Feedback Management</h2>
        
        <RouterLink :to="{ name: 'moderationQueue' }" class="action-btn-moderation router-link">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </RouterLink>
        
        <button @click="goToContentReview" class="action-btn-secondary">
             <span class="emoji">📚</span> Manage User Content
        </button>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
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
    color: white !important; /* Forces link text color */
}

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style> -->








<!-- <script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; // CRITICAL: Import RouterLink

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const isLoading = ref(true);
const errorMsg = ref('');

// --- Fetch Admin Statistics ---
const fetchAdminStats = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    // NOTE: This is a placeholder check. In production, real admin role verification would happen here.
    if (!authStore.isAuthenticated) {
        errorMsg.value = 'Access Denied: Must be logged in.';
        isLoading.value = false;
        return;
    }
    
    try {
        const response = await axios.get(
            'http://localhost:5000/api/admin/stats', // Route 12
            authStore.authHeader
        );
        stats.value = response.data;
    } catch (error: any) {
        // A 403 or 401 error means authentication/role failure
        errorMsg.value = 'Failed to fetch Admin Stats. Status: ' + (error.response?.statusText || 'Network Error');
        console.error("Admin Fetch Failed:", error);
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchAdminStats);

// The goToContentReview alert handler has been DELETED, replaced by the RouterLink.
</script>

<template>
  <div class="admin-container">
    <h1><span class="emoji">👑</span> Admin Dashboard</h1>
    <p class="subtitle">Platform Health and Performance Overview</p>

    <div v-if="isLoading" class="loading-state">Loading system metrics...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    
    <div v-else class="dashboard-grid">
        
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
        <h2>Content Quality & Feedback Management</h2>
        
        <RouterLink :to="{ name: 'moderationQueue' }" class="action-btn-moderation router-link">
             <span class="emoji">🚨</span> Review Question Flags (0)
        </RouterLink>
        
        <RouterLink :to="{ name: 'contentManagement' }" class="action-btn-secondary router-link">
             <span class="emoji">📚</span> Manage User Content
        </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
    max-width: 1000px;
    margin: 50px auto;
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; /* Purple accent */
}

.stat-primary {
    border-left: 5px solid #2ecc71; /* Green accent for high importance */
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.action-btn-moderation, .action-btn-secondary, .action-btn-refresh {
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
    color: white !important; /* Forces link text color */
}

.action-btn-moderation {
    background-color: #e74c3c; /* Red for alerts/warnings */
    color: white;
    box-shadow: 0 4px 0 #c0392b;
}

.action-btn-secondary {
    background-color: #3498db; /* Blue for management */
    color: white;
    box-shadow: 0 4px 0 #2980b9;
}

.action-btn-moderation:active, .action-btn-secondary:active {
    box-shadow: 0 1px 0;
    transform: translateY(3px);
}
</style>

  -->
















  <!-- <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; 

// CRITICAL: Import chart components and register them
import { LineChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables); // Register all necessary components

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const leaderboard = ref<any[]>([]); // State for leaderboard data
const isLoading = ref(true);
const errorMsg = ref('');

// --- Chart Options (Customizing the look and feel) ---
const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#e0e0e0',
            },
        },
        title: {
            display: true,
            text: 'Top 5 User Accuracy Comparison',
            color: '#f1c40f', 
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
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                // Displaying the Rank as the label
                callback: function(this: any, val: any, index: number) {
                    if (leaderboard.value[index]) {
                         return `Rank ${leaderboard.value[index].rank}`;
                    }
                    return '';
                }
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)', 
            },
        },
        y: {
            title: {
                display: true,
                text: 'Accuracy (%)',
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                callback: (value: any) => `${value}%`, 
                stepSize: 10,
            },
            min: 0,
            max: 100,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            },
        },
    },
});


// --- Chart Data computed property ---
const chartData = computed(() => {
    // Define colors for visual rank distinction
    const colors = [
        '#3498db', // Rank 1: Blue
        '#2ecc71', // Rank 2: Green
        '#e74c3c', // Rank 3: Red
        '#9b59b6', // Rank 4: Purple
        '#f1c40f'  // Rank 5: Gold
    ];
    
    // We create a separate dataset for *each user* so they can be differentiated by color
    const datasets = leaderboard.value.map((user, index) => {
        const userColor = colors[index % colors.length]; 
        
        // Use the actual user's accuracy as the data point
        return {
            label: `${user.email.substring(0, user.email.indexOf('@'))} (${user.accuracy}%)`,
            data: [user.accuracy], // CRITICAL: Use accuracy for the Y-value
            fill: false,
            borderColor: userColor,
            tension: 0.4, // Makes the line curved like a real graph
            pointBackgroundColor: userColor,
            pointRadius: 8,
        };
    });

    // The labels on the X-axis (showing the Rank position)
    const labels = leaderboard.value.map(user => `Rank ${user.rank}`); 

    return {
        labels: labels.length > 0 ? labels : ['N/A'], // Ensure at least one label exists
        datasets: datasets,
    };
});


// --- Fetch Admin Statistics & Leaderboard ---
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
            
            <h2 class="leaderboard-title">📊 Top 5 User Performance Comparison</h2>
            
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
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; 
}

.stat-primary {
    border-left: 5px solid #2ecc71;
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS & LEADERBOARD STYLES --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

/* LEADERBOARD CHART CONTAINER */
.leaderboard-chart-container {
    padding: 15px;
    background-color: #3e3e5a;
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: left; 
}

.leaderboard-title {
    color: #f1c40f;
    font-size: 1.6rem;
    margin-bottom: 20px;
    text-align: center;
}

.user-bar-item {
    margin-bottom: 15px;
}

.user-label {
    display: block;
    text-align: left;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 3px;
}

.score-bar-track {
    background-color: #1a1a2e;
    height: 25px;
    border-radius: 4px;
    overflow: hidden;
}

/* Dynamic CSS Bar for Leaderboard Chart */
.score-bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    font-weight: bold;
    color: #1a1a2e; 
    text-align: left;
    transition: width 1s ease-out;
}

/* Rank Coloring for Bars and Table */
.score-bar-fill.rank-1 { background-color: #3498db; } /* Blue (High Rank) */
.score-bar-fill.rank-2 { background-color: #2ecc71; } /* Green */
.score-bar-fill.rank-3 { background-color: #e74c3c; } /* Red */
.score-bar-fill.rank-4 { background-color: #9b59b6; } /* Purple */
.score-bar-fill.rank-5 { background-color: #f1c40f; } /* Gold */

.leaderboard-table th, .leaderboard-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #444;
    font-size: 0.9rem;
}

/* Apply colors to the table rows for consistency */
.leaderboard-table tr.rank-1 td { color: #3498db; background-color: #3498db33; font-weight: bold; }
.leaderboard-table tr.rank-2 td { color: #2ecc71; background-color: #2ecc7133; }
.leaderboard-table tr.rank-3 td { color: #e74c3c; background-color: #e74c3c33; }
.leaderboard-table tr.rank-4 td { color: #9b59b6; background-color: #9b59b633; }
.leaderboard-table tr.rank-5 td { color: #f1c40f; background-color: #f1c40f33; }

.score-high {
    color: #2ecc71; 
}

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
    color: white !important;
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

 -->





















<!-- 


 <script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; 

// CRITICAL: Import BarChart and register Chart.js components
import { BarChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables); // Register all necessary components

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const leaderboard = ref<any[]>([]); // State for leaderboard data
const isLoading = ref(true);
const errorMsg = ref('');

// --- Chart Options (Customizing the look and feel) ---
const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#e0e0e0',
            },
        },
        title: {
            display: true,
            text: 'Top 5 User Accuracy Comparison',
            color: '#f1c40f', 
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
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                // Displaying the Rank as the label
                callback: function(this: any, val: any, index: number) {
                    if (leaderboard.value[index]) {
                         return `Rank ${leaderboard.value[index].rank}`;
                    }
                    return '';
                }
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)', 
            },
        },
        y: {
            title: {
                display: true,
                text: 'Accuracy (%)',
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                callback: (value: any) => `${value}%`, 
                stepSize: 10,
            },
            min: 0,
            max: 100,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            },
        },
    },
});


// --- Chart Data computed property ---
const chartData = computed(() => {
    // Define colors for visual rank distinction
    const colors = [
        '#3498db', // Rank 1: Blue
        '#2ecc71', // Rank 2: Green
        '#e74c3c', // Rank 3: Red
        '#9b59b6', // Rank 4: Purple
        '#f1c40f'  // Rank 5: Gold
    ];
    
    // We create a separate dataset for *each user* so they can be differentiated by color
    const datasets = leaderboard.value.map((user, index) => {
        const userColor = colors[index % colors.length]; 
        
        // CRITICAL FIX: Ensure the dataset contains the required properties for a bar chart
        return {
            label: `${user.email.substring(0, user.email.indexOf('@'))} (${user.accuracy}%)`,
            data: [user.accuracy], // Single bar height
            backgroundColor: userColor, // Use backgroundColor for bars
            borderColor: userColor,
            borderWidth: 1,
        };
    });

    // The labels on the X-axis (showing the Rank position)
    const labels = leaderboard.value.map(user => `Rank ${user.rank}`); 

    return {
        // Since BarChart requires an array of data points for its X-axis, we use the rank labels
        labels: labels.length > 0 ? labels : ['N/A'], 
        datasets: datasets,
    };
});


// --- Fetch Admin Statistics & Leaderboard ---
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
            
            <h2 class="leaderboard-title">📊 Top 5 User Performance Comparison</h2>
            
            <div class="chart-container">
                <BarChart 
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
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; 
}

.stat-primary {
    border-left: 5px solid #2ecc71;
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS & LEADERBOARD STYLES --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

/* LEADERBOARD CHART CONTAINER */
.leaderboard-chart-container {
    padding: 15px;
    background-color: #3e3e5a;
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: left; 
}

.leaderboard-title {
    color: #f1c40f;
    font-size: 1.6rem;
    margin-bottom: 20px;
    text-align: center;
}

.user-bar-item {
    margin-bottom: 15px;
}

.user-label {
    display: block;
    text-align: left;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 3px;
}

.score-bar-track {
    background-color: #1a1a2e;
    height: 25px;
    border-radius: 4px;
    overflow: hidden;
}

/* Dynamic CSS Bar for Leaderboard Chart */
.score-bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    font-weight: bold;
    color: #1a1a2e; 
    text-align: left;
    transition: width 1s ease-out;
}

/* Rank Coloring for Bars and Table */
.score-bar-fill.rank-1 { background-color: #3498db; } /* Blue (High Rank) */
.score-bar-fill.rank-2 { background-color: #2ecc71; } /* Green */
.score-bar-fill.rank-3 { background-color: #e74c3c; } /* Red */
.score-bar-fill.rank-4 { background-color: #9b59b6; } /* Purple */
.score-bar-fill.rank-5 { background-color: #f1c40f; } /* Gold */

.leaderboard-table th, .leaderboard-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #444;
    font-size: 0.9rem;
}

/* Apply colors to the table rows for consistency */
.leaderboard-table tr.rank-1 td { color: #3498db; background-color: #3498db33; font-weight: bold; }
.leaderboard-table tr.rank-2 td { color: #2ecc71; background-color: #2ecc7133; }
.leaderboard-table tr.rank-3 td { color: #e74c3c; background-color: #e74c3c33; }
.leaderboard-table tr.rank-4 td { color: #9b59b6; background-color: #9b59b633; }
.leaderboard-table tr.rank-5 td { color: #f1c40f; background-color: #f1c40f33; }

.score-high {
    color: #2ecc71; 
}

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
    color: white !important;
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
</style> -->















//LINE CHART
<!-- 
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useRouter, RouterLink } from 'vue-router'; 

// CRITICAL: Import LineChart and register Chart.js components
import { LineChart } from 'vue-chart-3'; // THIS IS NOW LineChart
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables); // Register all necessary components

const authStore = useAuthStore();
const router = useRouter();

const stats = ref<any>({});
const leaderboard = ref<any[]>([]); // State for leaderboard data
const isLoading = ref(true);
const errorMsg = ref('');

// --- Chart Options (Customizing the look and feel) ---
const chartOptions = ref({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#e0e0e0',
            },
        },
        title: {
            display: true,
            text: 'Top 5 User Accuracy Comparison',
            color: '#f1c40f', 
            font: {
                size: 18,
            },
        },
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'User Rank', // Still using rank for X-axis labels
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                // Displaying the Rank as the label
                callback: function(this: any, val: any, index: number) {
                    if (leaderboard.value[index]) {
                         return `Rank ${leaderboard.value[index].rank}`;
                    }
                    return '';
                }
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)', 
            },
        },
        y: {
            title: {
                display: true,
                text: 'Accuracy (%)',
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                callback: (value: any) => `${value}%`, 
                stepSize: 10,
            },
            min: 0,
            max: 100,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            },
        },
    },
});


// --- Chart Data computed property ---
const chartData = computed(() => {
    // Define colors for visual rank distinction
    const colors = [
        '#3498db', // Rank 1: Blue
        '#2ecc71', // Rank 2: Green
        '#e74c3c', // Rank 3: Red
        '#9b59b6', // Rank 4: Purple
        '#f1c40f'  // Rank 5: Gold
    ];
    
    // For a Line Chart, if we want separate lines for each user's single data point,
    // we create a dataset for *each user*.
    // However, if you only have one data point per line, it will only render as a point, not a connected line.
    const datasets = leaderboard.value.map((user, index) => {
        const userColor = colors[index % colors.length]; 
        
        return {
            label: `${user.email.substring(0, user.email.indexOf('@'))} (${user.accuracy}%)`,
            data: [user.accuracy], // CRITICAL: Only one data point here
            fill: false, // Don't fill area under the line
            borderColor: userColor,
            tension: 0.4, // Provides curve if multiple points were present
            pointBackgroundColor: userColor,
            pointRadius: 8, // Make the point visible
            pointHoverRadius: 10,
        };
    });

    // The labels on the X-axis (showing the Rank position). 
    // This will appear under each point.
    const labels = leaderboard.value.map(user => `Rank ${user.rank}`); 

    return {
        labels: labels.length > 0 ? labels : ['N/A'], // Ensure at least one label exists
        datasets: datasets,
    };
});


// --- Fetch Admin Statistics & Leaderboard ---
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
            
            <h2 class="leaderboard-title">📊 Top 5 User Performance Comparison</h2>
            
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
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; 
}

.stat-primary {
    border-left: 5px solid #2ecc71;
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS & LEADERBOARD STYLES --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

/* LEADERBOARD CHART CONTAINER */
.leaderboard-chart-container {
    padding: 15px;
    background-color: #3e3e5a;
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: left; 
}

.leaderboard-title {
    color: #f1c40f;
    font-size: 1.6rem;
    margin-bottom: 20px;
    text-align: center;
}

.user-bar-item {
    margin-bottom: 15px;
}

.user-label {
    display: block;
    text-align: left;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 3px;
}

.score-bar-track {
    background-color: #1a1a2e;
    height: 25px;
    border-radius: 4px;
    overflow: hidden;
}

/* Dynamic CSS Bar for Leaderboard Chart */
.score-bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    font-weight: bold;
    color: #1a1a2e; 
    text-align: left;
    transition: width 1s ease-out;
}

/* Rank Coloring for Bars and Table */
.score-bar-fill.rank-1 { background-color: #3498db; } /* Blue (High Rank) */
.score-bar-fill.rank-2 { background-color: #2ecc71; } /* Green */
.score-bar-fill.rank-3 { background-color: #e74c3c; } /* Red */
.score-bar-fill.rank-4 { background-color: #9b59b6; } /* Purple */
.score-bar-fill.rank-5 { background-color: #f1c40f; } /* Gold */

.leaderboard-table th, .leaderboard-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #444;
    font-size: 0.9rem;
}

/* Apply colors to the table rows for consistency */
.leaderboard-table tr.rank-1 td { color: #3498db; background-color: #3498db33; font-weight: bold; }
.leaderboard-table tr.rank-2 td { color: #2ecc71; background-color: #2ecc7133; }
.leaderboard-table tr.rank-3 td { color: #e74c3c; background-color: #e74c3c33; }
.leaderboard-table tr.rank-4 td { color: #9b59b6; background-color: #9b59b633; }
.leaderboard-table tr.rank-5 td { color: #f1c40f; background-color: #f1c40f33; }

.score-high {
    color: #2ecc71; 
}

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
    color: white !important;
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
</style> -->










 
<!-- 

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

// --- Chart Options (Remains the same) ---
const chartOptions = ref({
    // ... (omitted chartOptions code - it remains the same) ...
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                color: '#e0e0e0',
            },
        },
        title: {
            display: true,
            text: 'Top  Users Accuracy Comparison',
            color: '#f1c40f', 
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
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                // Displaying the Rank as the label
                callback: function(this: any, val: any, index: number) {
                    if (index === 0) return 'Start'; // Use 'Start' for the first point
                    if (leaderboard.value.length > 0) {
                         // Use a placeholder for the X-axis label on the second point
                         return leaderboard.value[0].email.substring(0, leaderboard.value[0].email.indexOf('@')) + '...'; 
                    }
                    return '';
                }
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)', 
            },
        },
        y: {
            title: {
                display: true,
                text: 'Accuracy (%)',
                color: '#c0c0c0',
            },
            ticks: {
                color: '#e0e0e0',
                callback: (value: any) => `${value}%`, 
                stepSize: 10,
            },
            min: 0,
            max: 100,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            },
        },
    },
});


// --- Chart Data computed property (CRITICAL FIX) ---
const chartData = computed(() => {
    // Define colors for visual rank distinction
    const colors = [
        '#3498db', // Rank 1: Blue
        '#2ecc71', // Rank 2: Green
        '#e74c3c', // Rank 3: Red
        '#9b59b6', // Rank 4: Purple
        '#f1c40f'  // Rank 5: Gold
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
    color: #e0e0e0;
    text-align: center;
}
.subtitle {
    color: #c0c0c0;
    margin-bottom: 40px;
}
.emoji {
    margin-right: 10px;
}
.loading-state, .error-state {
    color: #f1c40f;
    padding: 20px;
    background-color: #2a2a44;
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
    background-color: #2a2a44;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: left;
    border-left: 5px solid #c990ff; 
}

.stat-primary {
    border-left: 5px solid #2ecc71;
}

.card-label {
    font-size: 0.9rem;
    color: #c0c0c0;
    margin-bottom: 5px;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.card-detail {
    font-size: 0.8rem;
    color: #999;
    margin-top: 5px;
}

/* --- ADMIN ACTIONS & LEADERBOARD STYLES --- */
.admin-actions {
    padding: 20px;
    text-align: center;
    background-color: #1a1a2e;
    border-radius: 12px;
}
.admin-actions h2 {
    color: #c990ff;
    margin-bottom: 20px;
    font-size: 1.5rem;
}

/* LEADERBOARD CHART CONTAINER */
.leaderboard-chart-container {
    padding: 15px;
    background-color: #3e3e5a;
    border-radius: 10px;
    margin-bottom: 30px;
    text-align: left; 
}

.leaderboard-title {
    color: #f1c40f;
    font-size: 1.6rem;
    margin-bottom: 20px;
    text-align: center;
}

.user-bar-item {
    margin-bottom: 15px;
}

.user-label {
    display: block;
    text-align: left;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 3px;
}

.score-bar-track {
    background-color: #1a1a2e;
    height: 25px;
    border-radius: 4px;
    overflow: hidden;
}

/* Dynamic CSS Bar for Leaderboard Chart */
.score-bar-fill {
    height: 100%;
    line-height: 25px;
    padding-left: 10px;
    font-weight: bold;
    color: #1a1a2e; 
    text-align: left;
    transition: width 1s ease-out;
}

/* Rank Coloring for Bars and Table */
.score-bar-fill.rank-1 { background-color: #3498db; } /* Blue (High Rank) */
.score-bar-fill.rank-2 { background-color: #2ecc71; } /* Green */
.score-bar-fill.rank-3 { background-color: #e74c3c; } /* Red */
.score-bar-fill.rank-4 { background-color: #9b59b6; } /* Purple */
.score-bar-fill.rank-5 { background-color: #f1c40f; } /* Gold */

.leaderboard-table th, .leaderboard-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #444;
    font-size: 0.9rem;
}

/* Apply colors to the table rows for consistency */
.leaderboard-table tr.rank-1 td { color: #3498db; background-color: #3498db33; font-weight: bold; }
.leaderboard-table tr.rank-2 td { color: #2ecc71; background-color: #2ecc7133; }
.leaderboard-table tr.rank-3 td { color: #e74c3c; background-color: #e74c3c33; }
.leaderboard-table tr.rank-4 td { color: #9b59b6; background-color: #9b59b633; }
.leaderboard-table tr.rank-5 td { color: #f1c40f; background-color: #f1c40f33; }

.score-high {
    color: #2ecc71; 
}

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
    color: white !important;
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


 -->







































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
 





