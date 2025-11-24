

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios' 

const API_URL = 'http://localhost:5000'; // Define API URL
const route = useRoute()
const router = useRouter()

// We need the email for the POST request body, even if the token contains it
const email = ref(''); 
const token = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMsg = ref('');
const successMsg = ref('');
const isLoading = ref(false);

onMounted(() => {
    // ✨ FIX 1: Extract TOKEN from URL PATH PARAMETERS (based on the email link format) ✨
    // We expect the URL to be: http://localhost:8080/reset-password/YOUR_TOKEN
    const pathToken = route.params.token as string || '';

    if (pathToken) {
        token.value = pathToken;
    } else {
        errorMsg.value = 'Missing reset token in the URL. Please use the complete link from your reset request email.';
    }
    
    // NOTE: The email is not included in the URL for security, so we ask the user for it in the form.
})

async function handleResetPassword() {
    errorMsg.value = '';
    successMsg.value = '';
    isLoading.value = true;

    if (!email.value || !token.value || !newPassword.value || !confirmPassword.value) {
        errorMsg.value = 'Email, token, and both password fields are required.';
        isLoading.value = false;
        return;
    }

    if (newPassword.value.length < 6) {
        errorMsg.value = 'New password must be at least 6 characters long.';
        isLoading.value = false;
        return;
    }

    if (newPassword.value !== confirmPassword.value) {
        errorMsg.value = 'Passwords do not match.';
        isLoading.value = false;
        return;
    }
    
    // If the token is manually pasted into the form, we must prevent running if the token is already invalid/missing
    if (!token.value) {
        errorMsg.value = 'Token is missing or invalid.';
        isLoading.value = false;
        return;
    }

    try {
        // ✨ FIX 2: Correctly use the full API URL for the POST request ✨
        const response = await axios.post(`${API_URL}/api/auth/reset-password`, {
            email: email.value, // Pass user-provided email for backend lookup (though backend may ignore it)
            token: token.value,
            new_password: newPassword.value,
        });
        
        successMsg.value = response.data.msg || 'Password has been reset successfully!';
        
        // Optionally redirect to login after a short delay
        setTimeout(() => {
            router.push({ name: 'login' });
        }, 3000);

    } catch (err: any) {
        console.error('Password reset failed:', err);
        // Display the specific error message from Flask (e.g., "Token expired.")
        errorMsg.value = err.response?.data?.msg || 'Failed to reset password. Please ensure your token is valid and try again.';
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <div class="reset-password-card">
        <h2><span class="icon-key">🔑</span> Password Reset</h2>
        <p class="subtitle">Securely regain access to your account.</p>

        <div v-if="successMsg" class="success-message">
            {{ successMsg }}
        </div>

        <form @submit.prevent="handleResetPassword" v-else>
            <div class="form-group" v-if="!token">
                 <p class="error-message">
                    {{ errorMsg || 'The reset token is missing from the URL. Please use the link provided in your email.' }}
                </p>
            </div>
            
            <div class="form-group">
                <label for="email">Email Address:</label>
                <input 
                    id="email" 
                    type="email" 
                    v-model="email" 
                    placeholder="Enter the email used for the reset request" 
                    required
                >
            </div>


            <div class="form-group">
                <label for="token">Reset Token:</label>
                <input 
                    id="token" 
                    type="text" 
                    v-model="token" 
                    placeholder="Token should be in the URL path" 
                    required
                    :disabled="!!route.params.token"
                >
            </div>

            <div class="form-group">
                <label for="newPassword">New Password:</label>
                <input 
                    id="newPassword" 
                    type="password" 
                    v-model="newPassword" 
                    placeholder="Minimum 6 characters" 
                    required
                >
            </div>

            <div class="form-group">
                <label for="confirmPassword">Confirm Password:</label>
                <input 
                    id="confirmPassword" 
                    type="password" 
                    v-model="confirmPassword" 
                    required
                >
            </div>

            <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>

            <button type="submit" :disabled="isLoading || !token">
                <span v-if="isLoading">Processing...</span>
                <span v-else>Reset Password</span>
            </button>

            <p class="info-message" v-if="!token">
                If the token is missing, please ensure you clicked the full link from the reset email.
            </p>

            <div class="back-to-login">
                <RouterLink :to="{ name: 'login' }">← Back to Login</RouterLink>
            </div>
        </form>
    </div>
</template>

<style scoped>
/* (All your existing CSS is perfectly fine and is kept here) */
.reset-password-card {
    padding: 30px;
    border: 1px solid #4a2d73; /* Darker border for contrast */
    border-radius: 8px;
    max-width: 450px; /* Slightly wider card */
    margin: 50px auto;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Deeper shadow */
    background-color: #2c1a4d; /* Darker purple background */
    color: #e0e0e0; /* Light text color */
    text-align: center;
}

h2 {
    font-size: 2.2em;
    color: #f0e0ff; /* Lighter purple for heading */
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-key {
    margin-right: 10px;
    font-size: 1.2em;
}

.subtitle {
    color: #c0a0d8; /* Muted purple for subtitle */
    margin-bottom: 25px;
    font-size: 1.1em;
}

.instruction-text {
    background-color: #3b2561; /* Slightly lighter background for instruction */
    border-left: 4px solid #9b59b6;
    padding: 15px;
    margin-bottom: 20px;
    text-align: left;
    font-size: 0.9em;
    color: #e0e0e0;
    line-height: 1.5;
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #f0e0ff;
}

.form-group input[type="text"],
.form-group input[type="password"],
.form-group input[type="email"] { /* Added email type */
    width: 100%;
    padding: 12px;
    border: 1px solid #6a4d9a; /* Border matching theme */
    border-radius: 6px;
    box-sizing: border-box;
    background-color: #3b2561; /* Darker input background */
    color: #e0e0e0;
    font-size: 1em;
}

.form-group input::placeholder {
    color: #a080c8;
}

/* Button Styling */
button {
    width: 100%;
    padding: 14px;
    background-color: #9b59b6; /* Purple button */
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.15rem;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 6px 0 #7e4a9e; /* Deeper 3D shadow */
    transform: translateY(0);
    margin-top: 15px;
}

button:hover:not(:disabled) {
    background-color: #7e4a9e; /* Darker purple on hover */
}

button:active:not(:disabled) {
    box-shadow: 0 2px 0 #7e4a9e;
    transform: translateY(4px);
}

button:disabled {
    background-color: #6c5b7b;
    box-shadow: 0 4px 0 #5a4b64;
    cursor: not-allowed;
    transform: translateY(0);
}

.error-message {
    color: #ff6b6b; /* Reddish error */
    margin-top: 15px;
    margin-bottom: 15px;
    text-align: center;
    background-color: rgba(255, 107, 107, 0.1);
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ff6b6b;
}

.success-message {
    color: #6bff94; /* Greenish success */
    margin-top: 15px;
    margin-bottom: 15px;
    text-align: center;
    background-color: rgba(107, 255, 148, 0.1);
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #6bff94;
    font-weight: bold;
}

.info-message {
    font-size: 0.85em;
    color: #a080c8;
    margin-top: 25px;
    line-height: 1.4;
}

.back-to-login {
    margin-top: 30px;
    font-size: 1em;
}

.back-to-login a {
    color: #f0e0ff;
    text-decoration: none;
    font-weight: bold;
    transition: color 0.2s ease;
}

.back-to-login a:hover {
    color: #9b59b6;
}

</style>
