



<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
// ✨ NEW: Import the Theme store for the accessibility feature ✨
import { useThemeStore } from '@/stores/theme';

const authStore = useAuthStore()
const themeStore = useThemeStore(); // Instantiate the theme store
</script>

<template>
  <header class="navbar">
    <nav>
      <RouterLink to="/">SmartQuizzer</RouterLink>
      <div class="nav-links">
        <template v-if="authStore.isAuthenticated">
          
          <RouterLink to="/content">Upload Notes</RouterLink> 
          <RouterLink to="/quiz">Start Quiz</RouterLink> 
          <RouterLink to="/analytics">Analytics</RouterLink> 
          
         
          
          <RouterLink to="/admin/leaderboard">Leaderboard</RouterLink> 
          <RouterLink to="/admin">Admin</RouterLink> 
          <RouterLink to="/feedback">Feedback</RouterLink> 
          <RouterLink to="/profile">Profile</RouterLink>
          
          <button @click="themeStore.toggleTheme" class="theme-toggle">
            <span v-if="themeStore.isDarkMode">☀️ Light Mode</span>
            <span v-else>🌙 Dark Mode</span>
          </button>
          
          <button @click="authStore.logout()" class="logout-btn">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register">Register</RouterLink>
        </template>
      </div>
    </nav>
  </header>

  <main class="container">
    <RouterView /> 
  </main>
</template>

<style scoped>
/* Basic styling for the navigation bar */
.navbar {
  /* Using CSS variables now for theme consistency */
  background-color: var(--color-card-bg); 
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); 
  border-bottom: 1px solid var(--color-border);
}

.navbar nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
}

.navbar a {
  color: var(--color-text); /* Use text color variable */
  text-decoration: none;
  padding: 0 10px;
  font-weight: bold;
}

.nav-links a {
  margin-left: 10px;
  font-size: 0.95rem;
}

/* Styling for the new Diagnostics link for visibility */
.diag-link {
    color: var(--color-primary) !important; /* Make it stand out */
    border-bottom: 2px solid var(--color-primary);
    padding-bottom: 2px;
}

/* --- THEME TOGGLE STYLES (FROM YOUR PROVIDED CODE) --- */
.theme-toggle {
    padding: 8px 12px;
    border: 1px solid var(--color-border);
    background-color: var(--color-card-bg);
    color: var(--color-text);
    cursor: pointer;
    border-radius: 5px;
    font-size: 0.85rem;
    margin-left: 15px; /* Spacing from previous link */
}
/* --- END THEME TOGGLE STYLES --- */


.logout-btn {
  background: none;
  border: none;
  color: var(--color-primary); /* Use primary color for highlight */
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  margin-left: 15px;
  padding: 0;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: var(--color-text);
}

.container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
}
</style>
