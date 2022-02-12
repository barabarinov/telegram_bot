import logging
from telegram import Update
from telegram.ext import CallbackContext

from app.db import Session
from app.models import User
from app.translate import (
    gettext as _,
    DELETE,
    INCOGNITO
)

logger = logging.getLogger(__name__)


def delete_my_telegram_id_from_telegram_bot(update: Update, context: CallbackContext):
    with Session() as session:
        user = session.query(User).get(update.effective_user.id)
        session.delete(user)
        session.commit()
    update.message.reply_text(
        _(DELETE, user.lang, user.username)
        if user.username is not None else _(DELETE, user.lang, _(INCOGNITO, user.lang))
    )
    # logger.info(f'USERLANG DELETE USER IS #####{user.lang}#####')
