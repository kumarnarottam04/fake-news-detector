/**
 * VeriNews AI - Client Side Controller Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const predictionForm = document.getElementById('predictionForm');
    const articleTitle = document.getElementById('articleTitle');
    const articleText = document.getElementById('articleText');
    const charCounter = document.getElementById('charCounter');
    const btnClear = document.getElementById('btnClear');
    const btnSubmit = document.getElementById('btnSubmit');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnTextContent = btnSubmit.querySelector('.btn-text-content');
    
    const resultsCard = document.getElementById('resultsCard');
    const predictionResult = document.getElementById('predictionResult');
    const predictionBadge = document.getElementById('predictionBadge');
    const confidenceValue = document.getElementById('confidenceValue');
    const latencyBadge = document.getElementById('latencyBadge');
    const explanationList = document.getElementById('explanationList');
    
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');
    const themeToggleBtn = document.getElementById('themeToggleBtn');

    // 1. Character Counter
    articleText.addEventListener('input', () => {
        const len = articleText.value.length;
        charCounter.textContent = `${len.toLocaleString()} / 10,000 characters`;
        if (len > 10000) {
            charCounter.style.color = 'var(--accent-fake)';
        } else {
            charCounter.style.color = 'var(--text-muted)';
        }
    });

    // 2. Clear Input
    btnClear.addEventListener('click', () => {
        articleTitle.value = '';
        articleText.value = '';
        charCounter.textContent = '0 / 10,000 characters';
        hideAlert();
        resultsCard.style.display = 'none';
        articleTitle.focus();
    });

    // 3. Theme Toggle
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
    });

    // 4. Form Submission & Real-time Inference
    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const title = articleTitle.value.trim();
        const text = articleText.value.trim();

        if (!title) {
            showAlert('Please enter an article title.');
            return;
        }

        if (text.length < 50) {
            showAlert('Please enter at least 50 characters of article text to analyze.');
            return;
        }

        const combinedText = `${title}\n\n${text}`;

        setLoading(true);

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: combinedText })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const errorMsg = data.error ? data.error.message : 'Prediction request failed.';
                showAlert(errorMsg);
                resultsCard.style.display = 'none';
                return;
            }

            renderResults(data);

        } catch (err) {
            console.error('API Error:', err);
            showAlert('Network error or server unreachable. Please check connection.');
        } finally {
            setLoading(false);
        }
    });

    // 5. UI Render Functions
    function renderResults(data) {
        const pred = data.prediction;
        const explanation = data.explanation;
        const meta = data.meta;

        // Display results card
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Update Prediction Result Badge
        const isReal = pred.label === 'REAL';
        predictionResult.textContent = isReal ? '🟢 REAL NEWS' : '🔴 FAKE NEWS';
        predictionBadge.className = `prediction-badge ${isReal ? 'badge-real' : 'badge-fake'}`;

        // Update Confidence Percentage
        confidenceValue.textContent = `${pred.confidence}%`;
        latencyBadge.textContent = `Processing time: ${meta.latency_ms}ms`;

        // Render Explanation Bullet Points
        explanationList.innerHTML = '';
        if (explanation.top_indicative_words && explanation.top_indicative_words.length > 0) {
            explanation.top_indicative_words.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `<span class="bullet-dot">•</span> <span>${escapeHtml(item.word)}</span>`;
                explanationList.appendChild(li);
            });
        } else {
            explanationList.innerHTML = '<li class="text-muted"><span class="bullet-dot">•</span> <span>No specific keyword features extracted.</span></li>';
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            btnSubmit.disabled = true;
            btnSpinner.style.display = 'block';
            btnTextContent.textContent = 'Analyzing News...';
        } else {
            btnSubmit.disabled = false;
            btnSpinner.style.display = 'none';
            btnTextContent.textContent = 'Analyze News';
        }
    }

    function showAlert(msg) {
        alertMessage.textContent = msg;
        alertBox.style.display = 'block';
    }

    function hideAlert() {
        alertBox.style.display = 'none';
    }

    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
        })[m]);
    }
});
