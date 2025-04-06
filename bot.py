from telegram.ext import Application, MessageHandler, filters
from firebase_admin import firestore, credentials
import firebase_admin
import logging
from datetime import datetime

# ===== CONFIGURATION =====
TELEGRAM_TOKEN = "7718575949:AAFiwHybIjwohfkLBYEXeVLwx3oOT_PsYQ4"
FIREBASE_CREDENTIALS = r"C:\Users\Joshua\Downloads\telegram-gemini-bot\telegram-gemini-ai-assistant-c0d681a68cce.json"
FIRESTORE_COLLECTION = "telegram_logs"

# ===== INITIALIZATION =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Firebase setup
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db = firestore.client()

# ===== CORE FUNCTION =====
async def save_message(update, context):
    try:
        # Prepare document data (UTC timestamp first)
        doc_data = {
            "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "server_time": firestore.SERVER_TIMESTAMP,
            "chat_id": update.message.chat_id,
            "question": update.message.text,
            "answer": "[PLACEHOLDER]",
            "status": "processed"
        }
        
        # Save to Firestore
        db.collection(FIRESTORE_COLLECTION).add(doc_data)
        logger.info(f"Saved message from {update.message.chat_id}")
        
        # User feedback
        await update.message.reply_text("✓ Message logged successfully")
        
    except Exception as e:
        logger.error(f"Failed to save message: {str(e)}")
        await update.message.reply_text("⚠️ Couldn't save your message")

# ===== START BOT =====
if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, save_message))
    
    logger.info("Bot started in polling mode")
    app.run_polling()