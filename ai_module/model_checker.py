import os
import urllib.request
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)
logger.propagate = False

def ensure_model_exists():
    model_path = "ships.pt"

    release_url = "https://github.com/Emmes1026/Satellite-Analysis-Dashboard/releases/download/v0.1.0-mvp/ships.pt"

    if not os.path.exists(model_path):
        logger.info(f"No File {model_path}. Start downloading...")
        try:
            urllib.request.urlretrieve(release_url, model_path)
            logger.info("Successfully downloaded AI model")
        except Exception as e:
            logger.error(f"Error during downloading: {e}")
    else:
        logger.info(f"Model {model_path} already exists.")

ensure_model_exists()