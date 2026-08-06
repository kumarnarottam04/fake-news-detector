# Professional Development Environment Setup Guide

**Project:** Fake News Detection System  
**Document Version:** 1.0.0  
**Target OS:** Windows 11, macOS (Apple Silicon / Intel), Linux (Ubuntu 22.04+)  
**Domain:** Machine Learning & Web Engineering  

---

## 1. Python Environment & Version Selection

### Recommended Python Version: **Python 3.12+**

#### Why Python 3.12+?
1. **Performance Enhancements:** Python 3.12 introduces substantial interpreter optimizations via the Faster CPython initiative (up to $15-25\%$ faster execution over Python 3.10).
2. **Improved Error Tracebacks:** Precise error locations in tracebacks pinpoint the exact sub-expression causing an exception, significantly reducing debugging time.
3. **Enhanced Type Annotations:** Native support for type parameter syntax (PEP 695) improves static analysis in IDEs.
4. **Optimized Memory Management:** Reduced memory overhead for small objects, crucial when loading large Scikit-learn and NLTK data structures.

#### Why Avoid Older Python Versions?
- **Python 3.7 and Below:** End-Of-Life (EOL); no security updates or official package support.
- **Python 3.8 / 3.9:** Security-only support phase; missing modern typing and performance optimizations.
- **Python 3.10 / 3.11:** Fully functional, but lack Python 3.12's speed gains and improved error reporting.

### Package Management: Pip & Virtual Environments

#### What is `pip`?
`pip` (Pip Installs Packages) is the standard package manager for Python. It fetches, installs, updates, and manages third-party libraries hosted on the Python Package Index (PyPI).

#### What is a Virtual Environment?
A virtual environment is an isolated self-contained directory tree that contains its own Python interpreter and independent set of installed libraries.

#### Why Are Virtual Environments Mandatory in Production?
1. **Dependency Isolation:** Prevents version conflicts between different projects (e.g., Project A requiring Scikit-learn 1.2 vs Project B requiring Scikit-learn 1.5).
2. **System Python Protection:** Prevents polluting or corrupting the global operating system Python installation.
3. **Reproducibility:** Guarantees that production deployments install the exact dependencies used during development.

---

## 2. Integrated Development Environment (IDE): VS Code

### Installation Guide

| OS | Recommended Installation Method |
| :--- | :--- |
| **Windows 11** | Download user installer from [code.visualstudio.com](https://code.visualstudio.com/) or install via winget: `winget install Microsoft.VisualStudioCode` |
| **macOS** | Download ZIP from official site, move `Visual Studio Code.app` to `/Applications` folder, or via Homebrew: `brew install --cask visual-studio-code` |
| **Linux (Ubuntu)** | Install via Snap: `sudo snap install --classic code` or DEB package: `sudo dpkg -i code_*.deb` |

### Recommended Workspace Settings (`.vscode/settings.json`)

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "black-formatter.args": ["--line-length", "88"],
  "isort.args": ["--profile", "black"],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

### Essential VS Code Shortcuts

| Action | Windows / Linux | macOS |
| :--- | :--- | :--- |
| **Command Palette** | `Ctrl + Shift + P` | `Cmd + Shift + P` |
| **Select Python Interpreter** | `Ctrl + Shift + P` $\rightarrow$ type `Python: Select Interpreter` | `Cmd + Shift + P` $\rightarrow$ type `Python: Select Interpreter` |
| **Open Integrated Terminal** | `Ctrl + ~` | `Ctrl + ~` |
| **Format Document** | `Shift + Alt + F` | `Option + Shift + F` |
| **Toggle Line Comment** | `Ctrl + /` | `Cmd + /` |
| **Global File Search** | `Ctrl + P` | `Cmd + P` |

---

## 3. Required VS Code Extensions

| Extension Name | Publisher ID | Purpose & Necessity |
| :--- | :--- | :--- |
| **Python** | `ms-python.python` | Core extension providing debugging, linting, code navigation, and environment switching. |
| **Pylance** | `ms-python.vscode-pylance` | High-performance static language server offering autocompletion, type checking, and docstrings. |
| **Jupyter** | `ms-toolsai.jupyter` | Provides native support for running and debugging `.ipynb` notebooks inside VS Code for exploratory data analysis (EDA). |
| **Black Formatter** | `ms-python.black-formatter` | Enforces deterministic Python code formatting based on strict PEP 8 standards. |
| **isort** | `ms-python.isort` | Automatically sorts and categorizes Python `import` statements alphabetically and by section. |
| **GitLens** | `eamodio.gitlens` | Visualizes Git authorship line-by-line, branch comparisons, and repository commit history directly in the editor. |
| **Error Lens** | `usernamehw.errorlens` | Highlights syntax errors, warnings, and lint failures directly inline on the code line. |
| **Prettier** | `esbenp.prettier-vscode` | Formatter for HTML, CSS, JavaScript, JSON, and Markdown files. |
| **Markdown Preview** | `shd101wyy.markdown-preview-enhanced` | Side-by-side live rendering of Markdown files (`.md`). |
| **Docker (Optional)** | `ms-azuretools.vscode-docker` | Manages Docker containers, images, and `Dockerfile` syntax highlighting. |

---

## 4. Version Control Setup: Git

### Installation Commands

- **Windows 11:** Download from [git-scm.com](https://git-scm.com/) or run `winget install Git.Git`.
- **macOS:** Install Xcode Command Line Tools: `xcode-select --install` or via Homebrew: `brew install git`.
- **Linux (Ubuntu):** `sudo apt update && sudo apt install git -y`

### Global Configuration Commands

```bash
# Set global identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name to main
git config --global init.defaultBranch main

# Enable line ending normalization (Windows: true, Mac/Linux: input)
# Windows:
git config --global core.autocrlf true
# macOS / Linux:
# git config --global core.autocrlf input

# Verify configuration
git config --list
```

### Initializing Repository & First Commit

```bash
# Navigate to project directory
cd "path/to/Fake News Detection"

# Initialize Git repository
git init

# Check status
git status

# Stage all project configuration files
git add .

# Create initial commit
git commit -m "chore: initialize project repository structure and development environment"
```

---

## 5. GitHub Repository & Branching Strategy

### Repository Setup
1. Log in to [GitHub](https://github.com/).
2. Create a new public/private repository named: `fake-news-detection-system`.
3. Do **NOT** check "Initialize with README" if uploading an existing local codebase.
4. Link local repository to remote:
   ```bash
   git remote add origin https://github.com/your-username/fake-news-detection-system.git
   git branch -M main
   git push -u origin main
   ```

### Enterprise Branching Strategy (Gitflow Hybrid)

```
main (Production Deployments / Stable Releases)
  │
  ├── develop (Active Integration Branch)
  │     │
  │     ├── feature/nlp-preprocessing
  │     ├── feature/model-training
  │     └── feature/flask-api
  │
  └── fix/cors-policy-error
```

- **`main`:** Protected branch containing production-ready code. Every push triggers automated CI/CD deployment.
- **`develop`:** Staging branch where feature branches merge after passing code review and automated tests.
- **`feature/<feature-name>`:** Short-lived feature branches for isolated development.
- **`fix/<bug-name>`:** Dedicated bug fix branches.

### Conventional Commit Standards
Format: `<type>(<scope>): <short summary>`
- `feat`: A new feature (e.g., `feat(nlp): add WordNet lemmatization routine`)
- `fix`: A bug fix (e.g., `fix(api): resolve payload length validation error`)
- `docs`: Documentation changes (e.g., `docs(readme): update installation instructions`)
- `style`: Code style formatting changes (e.g., `style(css): format button glassmorphism rules`)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing unit tests or refactoring existing tests
- `chore`: Maintenance tasks, dependencies, environment setup

---

## 6. Virtual Environment Management

### Commands Across Operating Systems

#### Creating Virtual Environment
```bash
# Windows / macOS / Linux
python -m venv venv
```

#### Activating Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **macOS / Linux (Bash / Zsh):**
  ```bash
  source venv/bin/activate
  ```

#### Deactivating Virtual Environment
```bash
deactivate
```

#### Deleting and Recreating Environment
```bash
# Delete existing virtual environment
# Windows (PowerShell):
Remove-Item -Recurse -Force venv
# macOS / Linux:
rm -rf venv

# Recreate fresh environment
python -m venv venv
```

---

## 7. Project Directory Structure

```
fake_news_detection/
├── data/
│   ├── raw/                        # Unprocessed raw CSV dataset files
│   ├── processed/                  # Cleaned, tokenized CSV dataset files
│   └── samples/                    # Sample articles for UI testing
├── models/                         # Serialized binary models (.joblib)
├── src/
│   ├── preprocessing/              # NLP cleaning & vectorization engines
│   ├── training/                   # Model training & hyperparameter tuning
│   ├── prediction/                 # Real-time inference & explainability
│   └── utils/                      # Logging & helper utilities
├── static/
│   ├── css/                        # Responsive CSS styling
│   ├── js/                         # Async client fetch scripts
│   └── images/                     # Static media assets
├── templates/                      # HTML5 templates
├── tests/
│   ├── unit/                       # Preprocessing & utility unit tests
│   └── integration/                # Flask REST API integration tests
├── docs/                           # System architecture & setup documentation
├── .env.example                    # Environment variables template
├── .gitignore                      # Git exclusion rules
├── .editorconfig                   # Cross-editor formatting consistency
├── app.py                          # Flask entry point
├── config.py                       # Application configuration class
├── Procfile                        # Gunicorn production server command
├── render.yaml                     # Render cloud blueprint
├── requirements.txt                # Pinned dependencies
├── pyproject.toml                  # Black, isort, and pytest config
└── README.md                       # Project overview
```

---

## 8. Dependencies Breakdown

### Production Dependencies

| Package | Purpose & Justification |
| :--- | :--- |
| **`Flask`** | Lightweight WSGI web framework for serving REST API endpoints. |
| **`Flask-Cors`** | Enables Cross-Origin Resource Sharing for secure frontend-backend communication. |
| **`Flask-Limiter`** | Implements rate limiting to protect endpoints against DoS attacks. |
| **`pandas`** | High-performance tabular data structures required for dataset ingestion and cleaning. |
| **`numpy`** | Multi-dimensional array operations supporting vectorization calculations. |
| **`scikit-learn`** | Core ML library providing TF-IDF vectorization, Logistic Regression, and evaluation metrics. |
| **`nltk`** | Natural Language Toolkit for tokenization, stopword filtering, and lemmatization. |
| **`matplotlib`** | Graphing library for generating EDA plots and ROC-AUC curve figures. |
| **`joblib`** | Fast binary serialization of trained Scikit-learn models and vectorizers to disk. |
| **`gunicorn`** | Production-grade WSGI HTTP server for multi-threaded cloud deployments on Linux/Render. |
| **`python-dotenv`** | Reads key-value pairs from `.env` files into environment variables. |

### Development & Quality Assurance Dependencies

| Package | Purpose & Justification |
| :--- | :--- |
| **`pytest`** | Automated testing framework for unit, integration, and regression test suites. |
| **`black`** | Uncompromising code formatter enforcing PEP 8 compliance. |
| **`flake8`** | Linter checking for syntax errors, style violations, and unused imports. |
| **`isort`** | Automatic import sorting and section organizing utility. |
| **`jupyter`** | Interactive notebook environment for rapid data exploration and prototyping. |

---

## 9. Requirements Management (`requirements.txt`)

### Generating & Freezing Pinned Dependencies
To ensure complete build reproducibility across local and production cloud environments:

```bash
# Install core dependencies first
pip install Flask Flask-Cors Flask-Limiter scikit-learn nltk pandas numpy matplotlib joblib gunicorn python-dotenv pytest black flake8 isort

# Freeze exact installed versions into requirements.txt
pip freeze > requirements.txt
```

### Reinstalling Dependencies in New Environment
```bash
pip install -r requirements.txt
```

---

## 10. Project Configuration Files

### 1. `.editorconfig` (Cross-Editor Consistency)
```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{js,css,html,json,yaml,yml}]
indent_size = 2
```

### 2. `pyproject.toml` (Tool Configurations)
```toml
[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-v --tb=short"
testpaths = ["tests"]
```

### 3. `LICENSE` (MIT License Template)
```text
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 11. Code Quality & Standards (PEP 8)

### Naming Conventions Summary

| Code Element | Naming Convention | Example |
| :--- | :--- | :--- |
| **Variables & Functions** | `snake_case` | `clean_text()`, `raw_article_input` |
| **Classes** | `PascalCase` | `TextCleaner`, `ModelLoader` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_CONTENT_LENGTH`, `MODEL_PATH` |
| **Modules / Files** | `lowercase_snake_case` | `text_cleaner.py`, `app.py` |
| **Private Attributes** | `_leading_underscore` | `self._is_loaded`, `self._model` |

### Docstring Standards (Google Style Format)

```python
def predict_article(raw_text: str) -> dict:
    """Executes prediction pipeline on raw article text.

    Args:
        raw_text (str): Unprocessed news article string.

    Returns:
        dict: Prediction results including label, confidence percentage,
            and top word impact weights.

    Raises:
        ValueError: If raw_text length is less than 50 characters.
    """
```

---

## 12. Terminal Command Quick Reference Table

| Action | Windows 11 (PowerShell) | macOS / Linux (Bash) |
| :--- | :--- | :--- |
| **Navigate to Workspace** | `cd "C:\Path\To\Project"` | `cd "/path/to/project"` |
| **Create Virtual Env** | `python -m venv venv` | `python3 -m venv venv` |
| **Activate Virtual Env** | `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate` |
| **Deactivate Virtual Env**| `deactivate` | `deactivate` |
| **Install Requirements** | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| **Freeze Requirements** | `pip freeze > requirements.txt` | `pip freeze > requirements.txt` |
| **Run Flask Dev Server** | `python app.py` | `python3 app.py` |
| **Run Pytest Suite** | `pytest tests/ -v` | `pytest tests/ -v` |
| **Format Code (Black)** | `black src/ app.py` | `black src/ app.py` |
| **Lint Code (Flake8)** | `flake8 src/ app.py` | `flake8 src/ app.py` |

---

## 13. Troubleshooting & Common Setup Errors

> [!WARNING]
> **Issue 1: PowerShell ExecutionPolicy Error (`cannot be loaded because running scripts is disabled`)**
> - **Cause:** Windows blocks unsigned script execution by default.
> - **Fix:** Open PowerShell as Administrator and run:
>   ```powershell
>   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
>   ```

> [!WARNING]
> **Issue 2: `python` command opens Microsoft Store or is not recognized**
> - **Cause:** Python environment variables are missing from System PATH.
> - **Fix:** Re-run Python Windows Installer, check **"Add Python.exe to PATH"**, and restart terminal.

> [!WARNING]
> **Issue 3: VS Code uses wrong Python interpreter (`ModuleNotFoundError`)**
> - **Cause:** VS Code defaults to global Python instead of project `venv`.
> - **Fix:** Press `Ctrl + Shift + P` $\rightarrow$ Select `Python: Select Interpreter` $\rightarrow$ Choose `./venv/Scripts/python.exe`.

> [!WARNING]
> **Issue 4: Permission Denied during pip install**
> - **Cause:** Running pip globally without administrator privileges or within locked virtual env.
> - **Fix:** Ensure virtual environment is activated (`(venv)` indicator visible in prompt) before executing `pip install`.

---

## 14. Final Verification Checklist

- [x] **Python 3.12+** installed and verified via `python --version`
- [x] **Git** installed and configured globally (`user.name`, `user.email`)
- [x] **VS Code** installed with required extensions (Python, Pylance, Black, isort, GitLens)
- [x] **Git Repository** initialized (`git init`) and `.gitignore` configured
- [x] **Virtual Environment (`venv`)** created and active
- [x] **Production & Dev Packages** installed via `pip`
- [x] **Requirements file (`requirements.txt`)** generated
- [x] **Configuration files (`.env.example`, `.editorconfig`, `pyproject.toml`)** created
- [x] **Project Directory Structure** established (`src/`, `templates/`, `static/`, `data/`, `models/`, `tests/`)
- [x] **Workspace Verified** and ready for development
