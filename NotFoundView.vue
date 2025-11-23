<template>
    <div class="not-found-container">
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for does not exist in SmartQuizzer.</p>
        <RouterLink to="/profile">Go to Dashboard</RouterLink>
    </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.not-found-container {
    padding: 50px;
    text-align: center;
    color: var(--color-text);
    background-color: var(--color-card-bg);
    border-radius: 10px;
    margin-top: 50px;
}
h1 {
    color: var(--color-primary);
    font-size: 2.5em;
    margin-bottom: 10px;
}
p {
    font-size: 1.2em;
    margin-bottom: 20px;
}
a {
    color: var(--color-primary);
    text-decoration: underline;
    font-weight: bold;
}
</style>