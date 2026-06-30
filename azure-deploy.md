# Azure deployment notes for Poet AI Studio

## Requirements
- Azure subscription with access to App Service.
- A GitHub repository or local clone to deploy from.
- A valid Gemini API key in the App Service application settings.

## Recommended deployment steps
1. Create a Linux Web App on Azure App Service using Python 3.13.
2. Use the app name: `samorndeploy`.
3. Set the startup command to:
   `bash startup.sh`
4. Add the application setting:
   - `GEMINI_API_KEY=<your_key>`
   - `PORT=8000`
5. Deploy the repository to the Web App.
6. Open the published URL.

## Notes
- The app uses a SQLite database stored in the repository by default, so Azure Files or persistent storage is recommended for production use.
- For a production-ready deployment, move the data store to Azure Database for PostgreSQL or MySQL and update the database connection settings.
