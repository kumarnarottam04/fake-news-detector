/**
 * VeriNews AI - Client Side Controller Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const predictionForm = document.getElementById('predictionForm');
    const articleText = document.getElementById('articleText');
    const charCounter = document.getElementById('charCounter');
    const btnClear = document.getElementById('btnClear');
    const btnSubmit = document.getElementById('btnSubmit');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnTextContent = btnSubmit.querySelector('.btn-text-content');
    
    const btnSampleReal = document.getElementById('btnSampleReal');
    const btnSampleFake = document.getElementById('btnSampleFake');
    
    const resultsCard = document.getElementById('resultsCard');
    const predictionResult = document.getElementById('predictionResult');
    const predictionBadge = document.getElementById('predictionBadge');
    const confidenceValue = document.getElementById('confidenceValue');
    const meterFill = document.getElementById('meterFill');
    const probReal = document.getElementById('probReal');
    const probFake = document.getElementById('probFake');
    const latencyBadge = document.getElementById('latencyBadge');
    const wordBadgesContainer = document.getElementById('wordBadgesContainer');
    
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
        articleText.value = '';
        charCounter.textContent = '0 / 10,000 characters';
        hideAlert();
        resultsCard.style.display = 'none';
        articleText.focus();
    });

    // 3. Theme Toggle
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
    });

    // 4. Sample Article Buttons
    let sampleDataCache = null;
    
    async function loadSamples() {
        if (sampleDataCache) return sampleDataCache;
        try {
            const response = await fetch('/api/samples');
            const data = await response.json();
            if (data.success) {
                sampleDataCache = data.samples;
                return sampleDataCache;
            }
        } catch (e) {
            console.error('Failed to fetch samples:', e);
        }
        return null;
    }

    btnSampleReal.addEventListener('click', async () => {
        const samples = await loadSamples();
        if (samples && samples.real_article) {
            articleText.value = `${samples.real_article.title}\n\n${samples.real_article.text}`;
            articleText.dispatchEvent(new Event('input'));
            hideAlert();
        }
    });

    btnSampleFake.addEventListener('click', async () => {
        const samples = await loadSamples();
        if (samples && samples.fake_article) {
            articleText.value = `${samples.fake_article.title}\n\n${samples.fake_article.text}`;
            articleText.dispatchEvent(new Event('input'));
            hideAlert();
        }
    });

    // 5. Form Submission & Real-time Inference
    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const text = articleText.value.trim();
        if (text.length < 50) {
            showAlert('Please enter at least 50 characters of article text to analyze.');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
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

    // 6. UI Render Functions
    function renderResults(data) {
        const pred = data.prediction;
        const explanation = data.explanation;
        const meta = data.meta;

        // Display results container
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Update Classification Badge
        predictionResult.textContent = `${pred.label} NEWS`;
        predictionBadge.className = `prediction-badge ${pred.label === 'REAL' ? 'badge-real' : 'badge-fake'}`;

        // Update Confidence Meter
        confidenceValue.textContent = `${pred.confidence}%`;
        meterFill.style.width = `${pred.confidence}%`;
        meterFill.className = `meter-fill ${pred.label === 'REAL' ? 'meter-real' : 'meter-fake'}`;

        probReal.textContent = pred.probabilities.real;
        probFake.textContent = pred.probabilities.fake;

        latencyBadge.textContent = `Processing time: ${meta.latency_ms}ms`;

        // Render Top Word Badges
        wordBadgesContainer.innerHTML = '';
        if (explanation.top_indicative_words && explanation.top_indicative_words.length > 0) {
            explanation.top_indicative_words.forEach(item => {
                const badge = document.createElement('div');
                badge.className = `word-badge ${item.supports === 'REAL' ? 'word-badge-real' : 'word-badge-fake'}`;
                badge.innerHTML = `
                    <span>${escapeHtml(item.word)}</span>
                    <span class="word-score">(${item.score > 0 ? '+' : ''}${item.score})</span>
                `;
                wordBadgesContainer.appendChild(badge);
            });
        } else {
            wordBadgesContainer.innerHTML = '<span class="text-muted">No high-significance word features extracted.</span>';
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            btnSubmit.disabled = true;
            btnSpinner.style.display = 'block';
            btnTextContent.textContent = 'Analyzing Article...';
        } else {
            btnSubmit.disabled = false;
            btnSpinner.style.display = 'none';
            btnTextContent.textContent = 'Analyze Article';
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
