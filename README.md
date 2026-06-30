# Poet AI Studio

Poet AI Studio is a friendly desktop app for creating songs, stories, and AI-assisted writing ideas with a polished Flet interface. It combines a welcoming landing page, a guided creative workspace, and chat-style AI flows powered by Gemini.

## ✨ What it does

- Generate song lyrics with a dedicated AI composer experience
- Build story ideas and narrative drafts with a story-focused AI assistant
- Save favorite ideas locally for later review
- Enjoy a lighter, more animated experience with a modern, user-friendly UI

## 🛠️ Tech stack

- Python
- Flet
- Google GenAI SDK
- SQLite (with optional MySQL compatibility)

## 🚀 Setup

1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd Poet_AI
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Gemini API key
   ```bash
   copy .env.example .env
   ```
   Then edit the file and add your key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Run the app
   ```bash
   python app.py
   ```

## 🧪 Verification

Run the built-in regression test:
```bash
python -m unittest discover -s tests -v
```

## 📁 Notes

- The app stores saved content in a local SQLite database file named poet_ai.db by default.
- If MySQL is configured and reachable, the app can also use it.
- The AI features require a valid Gemini API key to work.
