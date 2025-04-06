# Telegram + Gemini AI Bot

A Telegram bot integrated with Google's Gemini AI and Firebase Firestore.

## Features
- `/start`: Registers users in Firestore.
- AI responses via Gemini (implement your logic in `bot.py`).
- 24/7 deployment on Google Cloud Run.

## Setup
1. **Secrets**:  
   - Store Firebase credentials in Google Secret Manager as `firebase-creds`.
   - Set `TELEGRAM_TOKEN` in Cloud Run environment variables.

2. **Deploy**:
   ```bash
   gcloud builds submit --config deploy/cloudbuild.yaml