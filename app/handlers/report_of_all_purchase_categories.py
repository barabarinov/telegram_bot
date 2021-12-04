import logging

from telegram import Update
from telegram.ext import CallbackContext

from db import Session
from models import User

logger = logging.getLogger(__name__)


def get_sum_of_all_purchases_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        for group in user.groups_purchases:
            logger.info(f'HERE IS GROUP {group}')
            result = sum(purchase.spent_money for purchase in group.purchases)
            logger.info(f'HERE IS RESULT {result}')
            update.message.reply_text(f'Sum of purchase in categorie {group.name}: ₴{result}')