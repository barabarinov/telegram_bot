import logging
from telegram import Update
from app.db import Session
from app.models import User

logger = logging.getLogger(__name__)


def find_user_lang(update: Update):
    with Session() as session:
        telegram_id = update.effective_user.id
        user = session.query(User).get(telegram_id)
        return user.lang


def find_effective_user_id(update: Update):
    with Session() as session:
        return session.query(User).get(update.effective_user.id)
