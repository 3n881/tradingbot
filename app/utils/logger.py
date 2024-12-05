import logging
from datetime import datetime

# Configure the logger
logging.basicConfig(
    filename="bot_actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_bot_action(bot_id, action, details):
    """Log bot actions with details."""
    logging.info(f"Bot ID: {bot_id} | Action: {action} | Details: {details}")
