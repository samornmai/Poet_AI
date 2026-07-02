# Poet AI Studio

## Project Description
Poet AI Studio is an AI-powered creative workspace built with Python and Flet. It helps users generate song lyrics, story ideas, and AI-assisted writing content in a modern and responsive interface. The app also allows users to save their work locally and continue creating later.

## Features
- Generate song lyrics with an AI-assisted songwriting experience
- Create stories and story ideas with a guided AI workflow
- Use a chat-style assistant for creative help
- Save generated content for future review
- Enjoy a responsive design for both web and mobile screens

## Installation and Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/samornmai/Poet_AI.git
   cd Poet_AI
   
      ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install flet
   python -m pip install google-generativeai                                                                   
   python -m pip install python-dotenv
   python -m pip install psycopg2-binary
   python -m pip install google-genai
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Make sure the API key is valid and has access to the Gemini API.

## Technologies Used
- Python
- Flet
- Google GenAI SDK
- SQLite
- Python-dotenv

## How to Run the Project
Run the application with:
```bash
python main.py
```

The app will start and open the main creative workspace.

## Deployment Link
Live deployment:
https://poet-ai-studio-a6c3g2dvd3g3fshd.canadacentral-01.azurewebsites.net/

## Team Member Contributions
- Samorn Mai – Project lead, app structure, UI/UX design, responsive layout, and AI integration
- Team members can expand this section with their specific contributions as the project grows

## Notes
- Saved content is stored locally in a SQLite database.
- AI features require a valid Gemini API key to function properly.
