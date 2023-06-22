import logging
from typing import Callable, List, Any, Optional, Self

import telegram.error
from telegram import (
    Update,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import CallbackContext

from app.models import User
from app.translate import (
    DEFAULT_LANG,
    TRANSLATES,
)

FORMATTER = Callable[[str], str]
FORMATTERS = List[FORMATTER]

logger = logging.getLogger(__name__)


class Message:
    def __init__(self,
                 update: Optional[Update] = None,
                 context: Optional[CallbackContext] = None,
                 language: str = DEFAULT_LANG,
                 parse_mode: str = ParseMode.MARKDOWN_V2):

        self._update = update
        self._context = context
        self._language = language
        self._parse_mode = parse_mode
        self._parts = []
        self._reply_keyboard = []
        self._reply_markup = None

    def translate(self, text: str) -> str:
        translate = TRANSLATES.get(text, {})
        return translate.get(self._language) or translate.get(DEFAULT_LANG) or text

    def add(self, message: str, *args: Any, formatters: Optional[FORMATTERS] = None, **kwargs: Any) -> Self:
        formatters = formatters or []
        translated_args = [self.translate(arg) for arg in args]
        translated_kwargs = {k: self.translate(v) for k, v in kwargs.items()}
        translated_message = self.translate(message)
        translated_message = translated_message.format(*translated_args, **translated_kwargs)
        for formatter in formatters:
            translated_message = formatter(translated_message)
        self._parts.append(translated_message)

        return self

    def add_line(self, message: str, *args: Any, formatters: Optional[FORMATTERS] = None, **kwargs: Any) -> Self:
        return self.add(message, *args, formatters=formatters, **kwargs).add_newline()

    def add_title(self, title: str, *args: Any, formatters: Optional[FORMATTERS] = None, **kwargs: Any) -> Self:
        return self.add_line(title, *args, formatters=[bold] + (formatters or []), **kwargs)

    def add_newline(self) -> Self:
        return self.add("\n")

    def create_inline_button(self, text: str,
                             callback_id: Optional[str] = None,
                             is_translate: bool = True) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.translate(text) if is_translate else text,
            callback_data=callback_id or text,
        )

    def add_inline_buttons(self, *buttons: List[InlineKeyboardButton]) -> Self:
        for button in buttons:
            self._reply_keyboard.append(button)
        self._reply_markup = InlineKeyboardMarkup(self._reply_keyboard)
        return self

    def add_reply_buttons(self, *buttons: List[str], is_translate: bool = True, **keyboard_kwargs) -> Self:
        for button_list in buttons:
            self._reply_keyboard.append([self.translate(button) if is_translate else button for button in button_list])
            self._reply_markup = ReplyKeyboardMarkup(self._reply_keyboard, **keyboard_kwargs)
        return self

    def reply(self) -> None:
        self._update.effective_message.reply_text(
            text="".join(self._parts),
            parse_mode=self._parse_mode,
            reply_markup=self._reply_markup,
        )

    def send_message(self, user: User) -> None:
        try:
            self._context.bot.send_message(
                chat_id=user.telegram_id,
                text="".join(self._parts),
                parse_mode=self._parse_mode,
                reply_markup=self._reply_markup,
            )
        except (telegram.error.BadRequest, telegram.error.Unauthorized):
            logger.info(f'User {user.username} {user.telegram_id} blocked')
        else:
            logger.info(f'User {user.username} {user.telegram_id} sent message')

    def edit_message_text(self) -> None:
        self._context.bot.edit_message_text(
            chat_id=self._update.callback_query.message.chat_id,
            message_id=self._update.callback_query.message.message_id,
            text="".join(self._parts),
            parse_mode=self._parse_mode,
            reply_markup=self._reply_markup,
        )

    def __repr__(self) -> str:
        return f"Message[lang={self._language}]: {''.join(self._parts)} reply_keyboard: {self._reply_keyboard}"


TO_ESCAPE = {
    "\\", "_", "*", "[", "]", "(", ")", "~", ">", "#", "+",
    "-", "=", "|", "{", "}", ".", "!"
}


def escape(s: str) -> str:
    return "".join(map(lambda c: f"\\{c}" if c in TO_ESCAPE else c, str(s)))


def italic(s):
    return f"_{s}_"


def bold(s):
    return f"*{s}*"


def underscore(s):
    return f"__{s}__"
