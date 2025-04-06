# src/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
import json
import logging

logger = logging.getLogger(__name__)

def init_firebase(project_id: str, secret_name: str = "firebase-creds"):
    """Initialize Firebase using Secret Manager."""
    try:
        if not firebase_admin._apps:
            # Fetch credentials from Google Cloud Secret Manager
            client = secretmanager.SecretManagerServiceClient()
            secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(name=secret_path)
            cred_dict = json.loads(response.payload.data.decode("UTF-8"))
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized")
        return firestore.client()
    except Exception as e:
        logger.error(f"Firebase init failed: {e}")
        raise

# Example usage:
# db = init_firebase(os.getenv("GOOGLE_CLOUD_PROJECT"))