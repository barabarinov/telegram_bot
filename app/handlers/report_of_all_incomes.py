import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from db import Session
from models import User

logger = logging.getLogger(__name__)


def get_sum_of_all_incomes_categories(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        for group in user.groups_incomes:
            # logger.info(f'HERE IS GROUP {group}')
            result = sum(income.earned_money for income in group.incomes)
            update.message.reply_text(f'Sum of purchase in categorie {group.name}: ₴{result}')
        overall_result = sum(income.earned_money for income in user.incomes)
        update.message.reply_text(f'Total: ₴{overall_result}')
