from telegram import Update
from app.db import Session
from app.models import User


def get_effective_user(update: Update, session: Session):
    return session.query(User).get(update.effective_user.id)
