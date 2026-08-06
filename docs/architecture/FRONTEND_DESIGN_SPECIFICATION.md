# Master Frontend Architecture & UI/UX Design Specification

**Project Title:** Fake News Detection System  
**Document Type:** Frontend UI/UX Architecture, Glassmorphism Design System & Accessibility Specification  
**Author:** Principal Frontend Architect & UI/UX Lead  
**Target Tech Stack:** Semantic HTML5, Vanilla CSS3 (Custom Variables + Glassmorphism), ES6+ JavaScript  

---

## 1. Executive Summary & Design Aesthetics

The **Presentation Layer** (`templates/`, `static/`) delivers a high-end, SaaS-quality user interface for real-time news credibility verification. Designed with modern web aesthetics—vibrant HSL gradients, translucent glassmorphism backdrop blurs, animated progress gauges, and instant dark/light theme switching—the app provides a polished user experience across Desktop, Tablet, and Mobile viewports.

### Key UX Objectives
1. **Instant Clarity:** Visual classification badges (**REAL** vs **FAKE**) deliver unambiguous assessment results within 100 milliseconds of API response receipt.
2. **Explainability Visuals:** Keyword impact badges visualize specific vocabulary features ($\beta_j \times x_{i,j}$) driving the classifier's prediction.
3. **Accessibility (WCAG 2.1 AA Compliance):** Full keyboard focus indicators, screen reader ARIA live regions (`aria-live="polite"`), and high contrast ratios ($\ge 4.5:1$).
4. **Zero Heavy Dependencies:** Built entirely with vanilla HTML5, CSS3, and JavaScript, keeping initial page weight under **100 KB** and eliminating framework bloat.

---

## 2. Complete User Experience State Flow

```
[ LANDING / HERO SECTION ]
          |
          v
[ ARTICLE INPUT CARD ]
  - Character & Word Counter
  - Sample Buttons (Real Article / Fake Article)
  - Clear Form Button
          |
          | User Clicks "Analyze Article"
          v
[ VALIDATION CHECK ]
  - Is text length >= 50 characters?
          |
     +----+------------------------+
     | (Invalid)                   | (Valid)
     v                             v
[ INLINE ERROR ALERT ]       [ LOADING STATE ]
  "Text must be >= 50 chars"   - Button Spinner & Disabled State
                               - Async POST /api/predict Fetch
                                           |
                                           v
                             [ RESULTS CARD VISUALIZATION ]
                               - REAL / FAKE Color-coded Badge
                               - Animated Confidence Meter
                               - Probability Split P(Real) / P(Fake)
                               - Word Impact Explanation Badges
                               - Latency Badge (--ms)
```

---

## 3. Design System & CSS Variables (`static/css/style.css`)

The design system utilizes HSL color tokens and CSS custom properties supporting seamless Dark and Light mode switching:

```css
:root {
    /* Color Palette (Dark Theme Default) */
    --bg-primary: #0b0f19;
    --bg-secondary: #111827;
    --card-bg: rgba(17, 24, 39, 0.75);
    --card-border: rgba(255, 255, 255, 0.08);
    
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --text-muted: #6b7280;
    
    --brand-primary: #3b82f6;
    --brand-gradient: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
    
    --accent-real: #10b981;
    --accent-real-bg: rgba(16, 185, 129, 0.15);
    --accent-real-border: rgba(16, 185, 129, 0.3);
    
    --accent-fake: #ef4444;
    --accent-fake-bg: rgba(239, 68, 68, 0.15);
    --accent-fake-border: rgba(239, 68, 68, 0.3);
    
    --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    --radius-lg: 16px;
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

[data-theme="light"] {
    --bg-primary: #f8fafc;
    --bg-secondary: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.85);
    --card-border: rgba(0, 0, 0, 0.08);
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
}
```

---

## 4. Component Design Wireframes

### 1. Header & Navigation Bar
```
+-----------------------------------------------------------------------------------+
|  [Logo Icon] VeriNews AI Engine                [Active Status] [Theme Toggle 🌙]  |
+-----------------------------------------------------------------------------------+
```

### 2. Article Submission Input Card
```
+-----------------------------------------------------------------------------------+
|  📄 Article Text Submission        [Try Sample Real]  [Try Sample Fake]           |
|  +-----------------------------------------------------------------------------+  |
|  | Paste news headline and article text here (Minimum 50 characters)...        |  |
|  |                                                                             |  |
|  +-----------------------------------------------------------------------------+  |
|  Character Count: 0 / 10,000                                [Clear Text]          |
|                                                                                   |
|                           [   ANALYZE ARTICLE   ]                                 |
+-----------------------------------------------------------------------------------+
```

### 3. Prediction Results Card
```
+-----------------------------------------------------------------------------------+
|  📊 Analysis & Prediction Results                      Latency: 38.4ms            |
|  +---------------------------------------+  +----------------------------------+  |
|  |  PREDICTED AUTHENTICITY               |  |  PREDICTION CONFIDENCE           |  |
|  |  +---------------------------------+  |  |  96.45%                          |  |
|  |  |           REAL NEWS             |  |  |  [=======================>.....] |  |
|  |  +---------------------------------+  |  |  P(Real): 0.96  P(Fake): 0.04    |  |
|  +---------------------------------------+  +----------------------------------+  |
|                                                                                   |
|  Linguistic Word Impact Breakdown (TF-IDF Feature Weights):                       |
|  [ official (+1.42) ]   [ report (+1.15) ]   [ claim (-0.85) ]                      |
+-----------------------------------------------------------------------------------+
```

---

## 5. Responsive Design Breakpoint Matrix

| Device Class | Breakpoint Range | Layout Adjustments |
| :--- | :--- | :--- |
| **Mobile Portrait** | $320\text{px} - 480\text{px}$ | Single column grid; stacked result cards; touch target minimum 44px. |
| **Mobile Landscape / Tablet**| $481\text{px} - 768\text{px}$ | Flexible grid layout; condensed sample buttons; full-width input card. |
| **Laptop / Desktop** | $769\text{px} - 1200\text{px}+$| 2-Column results grid (Badge + Confidence Gauge side-by-side); max width 900px centered. |

---

## 6. Accessibility Features (WCAG 2.1 AA Compliance)

1. **Semantic Structure:** Native `<header>`, `<main>`, `<section>`, `<article>`, and `<footer>` elements.
2. **Keyboard Navigation:** Explicit `:focus-visible` styling (`outline: 2px solid var(--input-focus)`).
3. **Screen Reader Hints:** ARIA attributes (`aria-label`, `aria-live="polite"` for dynamic results updates, `aria-required="true"` on text area).
4. **Color Contrast:** Text-to-background contrast ratio $\ge 4.5:1$ across both light and dark themes.

---

## 7. Frontend Package Directory Layout (`static/` & `templates/`)

```
templates/
└── index.html                      # Single Page Application HTML5 view
static/
├── css/
│   └── style.css                   # Responsive design system & glassmorphism theme
├── js/
│   └── main.js                     # Async REST client & dynamic DOM updates
└── images/
    └── favicon.ico                 # Web application icon
```
