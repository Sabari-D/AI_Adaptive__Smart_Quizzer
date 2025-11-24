


<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'; 
import { useQuizStore } from '@/stores/quiz_store';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { useAuthStore } from '@/stores/auth'; 

const quizStore = useQuizStore();
const router = useRouter();
const authStore = useAuthStore(); 

// State for active interaction
const userResponse = ref('');
const selectedOption = ref<string | null>(null); 
const feedbackMessage = ref('');
const showExplanation = ref(false);
const isProcessing = ref(false);

// --- TIMER STATE ---
const timerStart = ref(0); 
const elapsedTime = ref(0); // Time in seconds for display
let timerInterval: number | undefined;

// Function to start the visual counter
const startVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerStart.value = Date.now(); // Reset submission start time
    elapsedTime.value = 0; // Reset visual counter
    
    // Start counting up every second
    timerInterval = setInterval(() => {
        elapsedTime.value += 1;
    }, 1000) as unknown as number; 
};

// Function to reset and stop the counter
const stopVisualTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = undefined;
    }
};


// --- Computed Properties ---
const currentQuestion = computed(() => quizStore.currentQuestion);
const isQuizRunning = computed(() => quizStore.isQuizActive);
const isLastQuestion = computed(() => 
    quizStore.currentQuestionIndex >= (quizStore.quizConfig?.numQuestions || 0) - 1
);
const currentQuestionNumber = computed(() => quizStore.currentQuestionIndex + 1);

// Watch currentQuestion to start the timer automatically when a new question loads
watch(currentQuestion, (newQ, oldQ) => {
    if (newQ && newQ !== oldQ) {
        timerStart.value = Date.now(); 
        startVisualTimer(); 
    }
}, { immediate: true }); 

// Stop timer when explanation is shown
watch(showExplanation, (isShowing) => {
    if (isShowing) {
        stopVisualTimer();
    }
});


// --- Handlers ---

// Triggers when user clicks an MCQ/T/F option
const selectOption = (option: string) => {
    selectedOption.value = option;
    handleSubmit();
};

// Triggers when user clicks Submit for Fill-up/Short Answer or after selecting an option
const handleSubmit = async () => {
    // Determine the answer to submit based on the question type
    let answerToSubmit;

    if (currentQuestion.value?.type === 'MCQ' || currentQuestion.value?.type === 'True/False') {
        if (!selectedOption.value) return; 
        answerToSubmit = selectedOption.value;
    } else {
        if (!userResponse.value.trim()) return; 
        answerToSubmit = userResponse.value;
    }
    
    const timeTaken = Date.now() - timerStart.value; 

    if (isProcessing.value) return;
    
    isProcessing.value = true;
    feedbackMessage.value = '';
    
    // 1. Check answer using store (passing timeTaken)
    const { isCorrect, logData } = quizStore.submitAnswer(answerToSubmit, timeTaken); 
    
    // 2. Log result to the backend immediately (Module 4)
    try {
        await axios.post('http://localhost:5000/api/quiz/log-answer', logData, authStore.authHeader); 
        console.log(`Answer logged successfully. Time: ${timeTaken}ms, Correct: ${logData.is_correct}`);
    } catch (e) {
        console.error("Failed to log answer history.");
    }

    // 3. Update UI based on correctness (Explanation for ALL answers)
    showExplanation.value = true;
    
    if (isCorrect) {
        feedbackMessage.value = '✅ Correct! Review the explanation below before continuing.';
    } else {
        feedbackMessage.value = '❌ Incorrect. Review the explanation below.';
    }
    
    isProcessing.value = false;
};

// Handles moving to the next question or finishing the quiz
const handleAdvance = async () => {
    if (isProcessing.value) return;
    isProcessing.value = true;

    if (isLastQuestion.value) {
        quizStore.endQuiz();
        router.push({ name: 'quizResults' }); 
        return;
    }

    // Attempt to generate the next question
    const success = await quizStore.generateNextQuestion(); 

    if (success) {
        // Reset local state for the new question
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = '';
        showExplanation.value = false;
    } else {
        // Failsafe if generation quota runs out or API fails
        quizStore.endQuiz();
        router.push('/quiz');
    }
    isProcessing.value = false;
};

// --- NEW NAVIGATION HANDLER (Backward Button Logic) ---
const goToPreviousQuestion = () => {
    if (quizStore.currentQuestionIndex > 0) {
        stopVisualTimer();
        quizStore.moveToPreviousQuestion();
        
        showExplanation.value = true;
        
        selectedOption.value = null;
        userResponse.value = '';
        feedbackMessage.value = `Reviewing Question ${quizStore.currentQuestionIndex + 1}`;
    }
};

// --- NEW HANDLER FOR MODULE 6 FEEDBACK ---
const flagQuestion = async () => {
    if (!currentQuestion.value) return;

    const reason = prompt("Please briefly state why you are flagging this question (e.g., inaccurate answer, inappropriate content):");

    if (!reason) return; 

    try {
        await axios.post(
            'http://localhost:5000/api/feedback/flag', // Route 13
            {
                question_id: currentQuestion.value.content_id, 
                reason: reason 
            },
            authStore.authHeader
        );
        alert("Thank you. The question has been flagged for administrator review.");
    } catch (e) {
        alert("Failed to flag question. Please try again later.");
        console.error("Flagging failed:", e);
    }
};


// IMPORTANT: Clear the interval when the component is unmounted (prevents memory leak)
onUnmounted(() => {
    stopVisualTimer();
});

// --- Initialization ---
onMounted(() => {
    if (!quizStore.quizConfig) {
        router.push('/quiz');
        return;
    }
    
    if (quizStore.quizQuestions.length === 0) {
        quizStore.generateNextQuestion();
    }
});
</script>

<template>
    <div class="active-quiz-container">
        <div v-if="!isQuizRunning || !currentQuestion" class="loading-state">
            <h1>Starting Quiz...</h1>
            <p>Generating question {{ currentQuestionNumber }} of {{ quizStore.quizConfig?.numQuestions }}</p>
        </div>

        <div v-else class="quiz-card">
            <div class="score-progress-container">
                <div class="score-label">{{ quizStore.currentScorePercentage }}%</div>
                <div class="progress-bar">
                    <div 
                        class="progress-fill" 
                        :style="{ width: quizStore.currentScorePercentage + '%' }"
                        :data-score="quizStore.currentScorePercentage"
                    ></div>
                </div>
            </div>
            <header class="quiz-header">
                <h2>Active Quiz Session</h2>
                <div class="header-stats-group"> 
                    <div class="stats-row">
                        <span class="stat-difficulty">
                            Difficulty: <strong>{{ authStore.userProfile?.difficulty_level || 'Loading...' }}</strong>
                        </span>
                    </div>
                    <div class="stats-row">
                        <span class="timer">{{ elapsedTime }}s</span> 
                        <span class="progress">Question {{ currentQuestionNumber }} / {{ quizStore.quizConfig?.numQuestions }}</span>
                    </div>
                </div>
            </header>
            
            <div class="question-content">
                <p class="question-type-tag">{{ currentQuestion.type }} Question</p>
                
                <p class="type-accuracy-tracker">
                    Accuracy for {{ currentQuestion.type }} Questions: 
                    <strong :class="{'score-high': quizStore.getTypeAccuracy(currentQuestion.type).percentage >= 70, 
                                     'score-low': quizStore.getTypeAccuracy(currentQuestion.type).percentage < 50}">
                        {{ quizStore.getTypeAccuracy(currentQuestion.type).percentage }}%
                    </strong>
                    ({{ quizStore.getTypeAccuracy(currentQuestion.type).attempts }} attempts)
                </p>
                <p class="question-text">{{ currentQuestion.question }}</p>
                
                <button 
                    @click="flagQuestion" 
                    :disabled="isProcessing || showExplanation"
                    class="flag-btn"
                >
                    ⚠️ Flag Question for Review
                </button>
            </div>
            
            <div class="answer-area">
                
                <div v-if="currentQuestion.type === 'MCQ'" class="options-group mcq-options">
                    <button 
                        v-for="option in currentQuestion.options" 
                        :key="option" 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === option, 
                            'option-correct': showExplanation && option === currentQuestion.answer,
                            'option-incorrect': showExplanation && selectedOption === option && option !== currentQuestion.answer,
                        }"
                        @click="selectOption(option)" 
                        class="option-btn">
                        {{ option }}
                    </button>
                </div>
                
                <div v-else-if="currentQuestion.type === 'True/False'" class="options-group tf-options">
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'True', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'true',
                            'option-incorrect': showExplanation && selectedOption === 'True' && currentQuestion.answer.toLowerCase() !== 'true',
                        }"
                        @click="selectOption('True')" 
                        class="option-btn true-btn">
                        TRUE
                    </button>
                    <button 
                        :disabled="!!selectedOption || isProcessing || showExplanation"
                        :class="{ 
                            'option-selected': selectedOption === 'False', 
                            'option-correct': showExplanation && currentQuestion.answer.toLowerCase() === 'false',
                            'option-incorrect': showExplanation && selectedOption === 'False' && currentQuestion.answer.toLowerCase() !== 'false',
                        }"
                        @click="selectOption('False')" 
                        class="option-btn false-btn">
                        FALSE
                    </button>
                </div>


                <form v-else @submit.prevent="handleSubmit">
                    <input 
                        type="text" 
                        v-model="userResponse" 
                        :disabled="showExplanation || isProcessing"
                        placeholder="Type your answer here (e.g., The Sun)" 
                        class="text-input"
                    />
                    <button type="submit" :disabled="showExplanation || isProcessing" class="submit-text-btn">
                        {{ isProcessing ? 'Checking...' : 'Submit Answer' }}
                    </button>
                </form>

            </div>
            
            <div v-if="feedbackMessage" :class="{'success-message': feedbackMessage.startsWith('✅'), 'error-message': feedbackMessage.startsWith('❌') }" class="feedback-box">
                <p>{{ feedbackMessage }}</p>
                <div v-if="showExplanation" class="explanation-area"> 
                    <p><strong>Correct Answer:</strong> <span :class="{'final-answer': currentQuestion.type !== 'Fill-up'}">{{ currentQuestion.answer }}</span></p>
                    <p><strong>Explanation:</strong> {{ currentQuestion.explanation }}</p>
                    
                    <button @click="handleAdvance" class="next-question-btn">
                        {{ isLastQuestion ? 'View Results' : 'Next Question' }}
                    </button>
                </div>
            </div>
        </div>
        
        <div class="navigation-footer">
            <button 
                v-if="quizStore.currentQuestionIndex > 0 && !isProcessing" 
                @click="goToPreviousQuestion" 
                class="nav-arrow-btn prev-btn"
            >
                &#9664; Previous Question
            </button>
            
            <button v-if="isQuizRunning" @click="quizStore.endQuiz(); router.push('/quiz')" class="exit-quiz-btn">
                End Quiz and Return to Config
            </button>
        </div>
    </div>
</template>

<style scoped>
.active-quiz-container {
    max-width: 700px;
    margin: 50px auto;
    color: var(--color-text); /* Use theme variable */
    text-align: center;
}

.quiz-card {
    /* Use theme variables for background, text, and border */
    background-color: var(--color-card-bg);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    text-align: left;
    position: relative; 
    border: 1px solid var(--color-border); /* Add border for definition */
}

.loading-state h1 {
    color: var(--color-primary);
    text-shadow: 0 0 5px var(--color-primary);
}

/* --- DYNAMIC PROGRESS BAR STYLING --- */
.score-progress-container {
    position: absolute; 
    top: 5px; 
    right: 20px; 
    width: 180px; 
    padding: 10px 0 0 0; 
    text-align: right;
    z-index: 20;
}

.score-label {
    font-size: 1.2rem; 
    font-weight: bold;
    color: #f1c40f; /* Specific highlight color */
    margin-bottom: 5px;
    text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
}

.progress-bar {
    width: 100%;
    height: 10px; 
    background-color: var(--color-border); /* Use border color as background */
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.8s ease-out, background-color 0.8s ease; 
    background-color: #3498db; 
}
/* ... Color Change Logic (remains the same) ... */
/* ------------------------------------------------------------------- */


.quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px; 
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--color-border); /* Use theme variable */
}

.quiz-header h2 {
    color: var(--color-text); /* Use theme variable */
    font-size: 1.5rem;
    flex-grow: 1;
}

/* NEW: Style for the header stats container */
.header-stats-group {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
    font-size: 0.95rem;
}

.stats-row {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
}

/* Style for the Difficulty Level display */
.stat-difficulty {
    color: var(--color-primary); /* Use theme primary color */
}

.stat-difficulty strong {
    color: #f1c40f; 
    font-weight: 700;
}

.timer {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f39c12; 
    margin-bottom: 5px;
}
/* END NEW TIMER STYLES */


.progress {
    color: #f1c40f;
    font-weight: bold;
}

.question-type-tag {
    background-color: var(--color-border); /* Use a subtle background color */
    color: var(--color-text); 
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 15px;
}

.question-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--color-text); /* Use theme text color */
    margin-bottom: 25px;
}

/* --- OPTION BUTTONS --- */
.options-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.option-btn {
    padding: 15px;
    background-color: var(--color-background); /* Use background for options */
    border: 2px solid var(--color-border);
    border-radius: 8px;
    color: var(--color-text);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    box-shadow: 0 4px 0 var(--color-border);
}

.option-btn:hover:not(:disabled) {
    background-color: var(--color-border); /* Subtle hover effect */
}

.option-btn:disabled {
    cursor: default;
    box-shadow: none;
    transform: none;
    opacity: 0.8;
}

/* Option Feedback Styles */
.option-correct {
    background-color: #2ecc71 !important;
    border-color: #219d5c;
    color: #1a1a2e !important; /* Ensure black text on green */
    font-weight: bold;
}

.option-incorrect {
    background-color: #e74c3c !important;
    border-color: #c0392b;
    color: #fff !important;
    font-weight: bold;
}

/* --- TEXT INPUT / SUBMIT --- */
.text-input {
    width: 100%;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    color: var(--color-text);
    font-size: 1rem;
    box-sizing: border-box;
}

.submit-text-btn {
    width: 100%;
    padding: 14px;
    background-color: #f1c40f;
    color: #1a1a2e;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 6px 0 #d39d00;
    transition: all 0.15s ease;
}

.submit-text-btn:active {
    box-shadow: 0 2px 0 #d39d00;
    transform: translateY(4px);
}

/* --- FEEDBACK BOX --- */
.feedback-box {
    margin-top: 25px;
    padding: 15px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
    /* Ensure text color is black on success/error background, handled by specific class below */
}

.success-message {
    background-color: #219d5c33; /* Green tint */
    border: 1px solid #2ecc71;
    color: var(--color-text); /* Use theme text color for general message */
}

.error-message {
    background-color: #c0392b33; /* Red tint */
    border: 1px solid #e74c3c;
    color: var(--color-text); /* Use theme text color for general message */
}

.explanation-area {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid var(--color-border); /* Use theme variable */
    text-align: left;
    color: var(--color-text); /* ✨ FIX: Explanation text color (Crucial) ✨ */
}

.explanation-area strong {
    color: var(--color-primary); /* Highlight strong text */
}

.final-answer {
    color: #2ecc71;
    font-weight: bold;
}

/* ... Navigation button styles (remains the same) ... */
</style> 


