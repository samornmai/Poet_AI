# Poet AI

## Project Description

<<<<<<< HEAD
Poet AI is a desktop/web-style creative writing application built with Flet. The app helps users create poems, songs, story poems, and short stories with an AI assistant. It includes user authentication, a default admin account, chat sessions, song and story creator forms, an admin user management page, and a dashboard that displays real user activity data.
=======
## Features
- Generate song lyrics with an AI-assisted songwriting experience
- Create stories and story ideas with a guided AI workflow
- Use a chat-style assistant for creative help
- Save generated content for future review
>>>>>>> 61fce21092372244a28682f0967162a845fcbfb2

## Installation and Setup Instructions

1. Clone or download this project.

2. Open a terminal in the project folder:

   ```bash
   cd Poet
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment.

   Windows PowerShell:

   ```bash
   .venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:

   ```bash
   .venv\Scripts\activate.bat
   ```

5. Install the required packages:

   ```bash
   pip install -r req.txt
   ```

6. Create a `.env` file in the project root and add your Groq API key:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

   The app can still open without an API key, but AI generation will show a fallback message instead of calling the model.

## Technologies Used

- Python
- Flet
- SQLite
- LangChain Groq
- python-dotenv
- Groq Llama model
- unittest

## Frontend and Backend

- Frontend Technology: Flet
- Backend Technology: Python
- Database Technology: SQLite
- AI Technology: Groq API, LangChain Groq, LangChain Core
- Environment Technology: python-dotenv

## How to Run the Project

Run the application with:

```bash
python app.py
```

The app creates and uses a local SQLite database file named `users.db`.

Default admin login:

```text
Username: Admin
Password: Admin123
```

Run tests with:

```bash
python -m unittest discover -s tests
```

## Deployment Link

Not deployed yet.

Deployment link: `https://poet-ai-studio-a6c3g2dvd3g3fshd.canadacentral-01.azurewebsites.net/`

## Team Member Contributions

- SamornMai: Built the Poet AI application interface, authentication system, dashboard, chat workspace, admin user management, and AI writing features.
- BOTH Sokheang: Worked on project documentation, testing, and installation/setup guidance.
- Khon Sreymom: Supported UI review, feature checking, and project presentation preparation.
