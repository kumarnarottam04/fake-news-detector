# Enterprise Frontend Architecture & UI/UX Design System Specification

**Project Title:** Fake News Detection System  
**Document Type:** Enterprise Modular Frontend Architecture, Component System & UI/UX Guidelines  
**Author:** Principal Frontend Architect & Lead UI/UX Engineer  
**Stack:** Semantic HTML5, Vanilla CSS3 (BEM Architecture + Modern Custom Variables), ES6+ Vanilla JavaScript  

---

## 1. Executive Summary & Aesthetic Architecture

The **Enterprise Presentation Layer** provides a modern, high-speed, accessible, and responsive user interface for verifying news authenticity in real time. Designed with a commercial AI SaaS aesthetic, the UI combines glassmorphism backdrops, HSL themes, micro-interactions, custom status gauges, and bulleted Explainable AI (XAI) feature breakdowns.

### Core Frontend Principles
1. **Zero Framework Overhead:** Built using 100% native HTML5, CSS3, and ES6+ JavaScript, delivering a sub-100 KB initial payload and sub-50 ms DOM rendering performance.
2. **Modular Architecture:** CSS and JavaScript are organized into decoupled single-responsibility modules (`themes.css`, `animations.css`, `api.js`, `validation.js`, `theme.js`).
3. **Accessibility First (WCAG 2.1 AA Compliant):** Full ARIA state management (`aria-live="polite"`, `aria-invalid`), high-contrast colors ($\ge 4.5:1$), and visible focus indicators.
4. **Resilient API Integration:** Custom `api.js` client equipped with request timeout aborts (`AbortController`), automatic retry mechanisms, and network failure fallback UI.

---

## 2. Directory Layout & Module Responsibilities

```
frontend/ (static/ & templates/)
├── templates/
│   ├── index.html                  # Main Single-Page Application (SPA) view
│   ├── about.html                  # Architecture overview & project introduction
│   ├── 404.html                    # User-friendly Not Found page
│   └── 500.html                    # Service Error page
├── static/
│   ├── css/
│   │   ├── style.css               # Core design tokens, layout grid & card containers
│   │   ├── responsive.css          # Breakpoints for Mobile, Tablet, Desktop & Retina
│   │   ├── animations.css          # Subtle CSS keyframe transitions, spinners & skeleton loaders
│   │   └── themes.css              # Light & Dark theme custom properties
│   ├── js/
│   │   ├── app.js                  # Master application orchestrator
│   │   ├── api.js                  # Async Fetch REST client with timeout & retry logic
│   │   ├── validation.js           # Client-side input length & sanitization engine
│   │   ├── animations.js           # Smooth scroll, ripple & entrance effects
│   │   └── theme.js                # Theme switcher with local storage persistence
│   └── images/
│       ├── icons/                  # SVG brand icons and badges
│       └── favicon.ico             # Application shortcut icon
└── docs/
    └── FRONTEND_ENTERPRISE_SPECIFICATION.md
```

### Module Responsibilities Breakdown

| File Path | Role & Responsibilities |
| :--- | :--- |
| **`templates/index.html`** | Semantic HTML5 markup containing hero banner, input cards, prediction output badge, and explanation bullet lists. |
| **`static/css/style.css`** | Defines global CSS custom properties, grid layouts, form styling, badges, and glassmorphism card containers. |
| **`static/css/responsive.css`**| Media queries adjusting typography, flex direction, and card padding across viewport breakpoints. |
| **`static/css/animations.css`**| Keyframe definitions for loading spinners, skeleton shimmer effects, fade-in transitions, and progress bar fills. |
| **`static/css/themes.css`** | Theme token definitions (`[data-theme="dark"]` and `[data-theme="light"]`). |
| **`static/js/api.js`** | Encapsulates HTTP requests to `/api/predict`, handling status codes, timeouts, and JSON error parsing. |
| **`static/js/validation.js`**| Validates input fields (`articleTitle` required, `articleText` length $\ge 50$ chars) and updates character counters. |
| **`static/js/theme.js`** | Detects system preference (`prefers-color-scheme`), handles toggle clicks, and persists choice in `localStorage`. |
| **`static/js/app.js`** | Orchestrates form events, coordinates loading states, and updates DOM elements dynamically. |

---

## 3. Complete User Experience State Flow

```
[ LANDING PAGE HERO ] ─────────> Displays project headline & AI subtitle
          │
          ▼
[ NEWS INPUT CARD ] ───────────> Article Title input + News Article textarea
          │
          │ User types input
          ▼
[ CLIENT VALIDATION ] ─────────> Checks non-empty Title & Text length >= 50 chars
          │
     ┌────┴────────────────────────┐
     │ (Invalid)                   │ (Valid)
     ▼                             ▼
[ INLINE ERROR ALERT ]       [ LOADING STATE ]
  Displays red error box       - Disables "Analyze News" button
                               - Displays animated loading spinner
                               - Dispatches async POST /api/predict request
                                           │
                                           ▼
                             [ API RESPONSE RECEIVED ]
                                           │
                                           ▼
                             [ PREDICTION RESULT CARD ]
                               - Renders 🟢 REAL NEWS or 🔴 FAKE NEWS badge
                               - Renders Confidence percentage (e.g. 96.4%)
                               - Renders bulleted explanation keywords (• word)
                               - Displays latency metadata (--ms)
```

---

## 4. Input Section & Form Component Specification

### Component Wireframe Layout
```
+-----------------------------------------------------------------------------------+
|  Article Title *                                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | Breaking: Government launches new renewable energy initiative...            |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
|  News Article *                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Paste full article text here (Minimum 50 characters)...                     |  |
|  |                                                                             |  |
|  +-----------------------------------------------------------------------------+  |
|  Character Count: 0 / 10,000                                [Clear text]          |
|                                                                                   |
|                           [   ANALYZE NEWS   ]                                    |
+-----------------------------------------------------------------------------------+
```

### Form UX Requirements
- **Required Fields Indicator:** Red star asterisk (`*`) on label text.
- **Character Counter:** Real-time counter (`0 / 10,000 characters`) updating on keypress. Text turns red if length $> 10,000$.
- **Clear Text Button:** Resets form inputs, hides error boxes, and resets prediction results.
- **Submit Button State:** Displays `Analyze News` in idle state; displays spinner and `Analyzing News...` in loading state.

---

## 5. Result Visualization & XAI Component Specification

### Component Wireframe Layout
```
+-----------------------------------------------------------------------------------+
|  Prediction                                            Processing time: 38.4ms    |
|                                                                                   |
|  +-----------------------------------+                                            |
|  |           🟢 REAL NEWS            |                                            |
|  +-----------------------------------+                                            |
|                                                                                   |
|  Confidence: 96.4%                                                                |
|                                                                                   |
|  Explanation                                                                      |
|  • government                                                                     |
|  • minister                                                                       |
|  • parliament                                                                     |
|  • official                                                                       |
+-----------------------------------------------------------------------------------+
```

### Result Component Rules
- **🟢 REAL NEWS Badge:** Rendered in Emerald Green (`--accent-real-bg`, `--accent-real`) when class `label == "REAL"`.
- **🔴 FAKE NEWS Badge:** Rendered in Rose Red (`--accent-fake-bg`, `--accent-fake`) when class `label == "FAKE"`.
- **Confidence Display:** Expressed as a prominent bold percentage (`Confidence: 96.4%`).
- **Explanation List:** Rendered as clean, readable bullet points with a custom accent dot (`•`).

---

## 6. Responsive Breakpoint Specification (`responsive.css`)

```css
/* Mobile Viewports (<480px) */
@media (max-width: 480px) {
    .main-container { padding: 16px 12px; }
    .hero-title { font-size: 1.6rem; }
    .card { padding: 18px 14px; }
    .btn-lg { padding: 12px 20px; font-size: 0.95rem; }
    .prediction-badge { font-size: 1.2rem; }
}

/* Tablet Viewports (481px - 768px) */
@media (max-width: 768px) {
    .hero-title { font-size: 1.85rem; }
    .card { padding: 22px; }
}

/* Desktop Viewports (>769px) */
@media (min-width: 769px) {
    .main-container { max-width: 800px; margin: 0 auto; }
}
```

---

## 7. Accessibility (WCAG 2.1 AA) Implementation

1. **Semantic HTML5:** Native `<header>`, `<main>`, `<section>`, `<form>`, `<label>`, `<textarea>`, and `<footer>` tags.
2. **Keyboard Navigation:** Explicit focus styles using `:focus-visible`:
   ```css
   .form-control:focus-visible,
   .btn:focus-visible {
       outline: 2px solid var(--input-focus);
       outline-offset: 2px;
   }
   ```
3. **Screen Reader Live Regions:** Dynamic error and prediction update containers marked with `aria-live="polite"` and `role="status"`.
4. **Form Association:** Every input element has a matching `<label for="...">` attribute.

---

## 8. Dark & Light Theme System (`theme.js` & `themes.css`)

The theme system automatically detects system dark mode preferences (`prefers-color-scheme: dark`) and persists user manual overrides in `localStorage`:

```javascript
/**
 * Theme Manager Module (static/js/theme.js)
 */
export function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', initialTheme);
}

export function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
```
