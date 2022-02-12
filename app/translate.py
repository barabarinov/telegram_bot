import logging

logger = logging.getLogger(__name__)


RU = 'ru'
EN = 'en'
DEFAULT = EN

REGISTERED = 'register'
INCOGNITO = 'incognito'
ALREADY_REGISTERED = 'already registered'
STOP_IT = 'stop it'
GROCERIES = 'groseries'
TRANSPORT = 'transport'
BILLS = 'bills'
MISCELLANEOUS = 'miscellaneous'
SALARY = 'salary'
DELETE = 'delete'
CANCEL = 'cancel'
INCOME_TITLE = 'income title'
HOW_MUCH_EARN = 'how much earn'
SELECT_GROUP = 'select group'
THATS_YOUR_INCOME = 'That\'s your income'
INCOME_ADDED = 'income added'
SEEYA = 'See ya'


TRANSLATES = {
    REGISTERED: {
        RU: '✅ Вы зарегестрированы, {}!',
        EN: '✅ You are registered, {}!',
    },
    INCOGNITO: {
        RU: 'Инкогнито',
        EN: 'Incognito',
    },
    ALREADY_REGISTERED: {
        RU: '❗Вы уже зарегестрированы️',
        EN: '❗️You are already registered',
    },
    STOP_IT: {
        RU: ' Остановись, я устал уже...😩',
        EN: ' Stop it, I\'m tired...😩'
    },
    GROCERIES: {
        RU: '🏠 Продукты и все для дома',
        EN: '🏠 Groceries and home appliances',
    },
    TRANSPORT: {
        RU: '🚙 Транспорт',
        EN: '🚙 Transport',
    },
    BILLS: {
        RU: '💵 Коммунальные',
        EN: '💵 Bills',
    },
    MISCELLANEOUS: {
        RU: '🛍 Разное',
        EN: '🛍 Miscellaneous',
    },
    SALARY: {
        RU: '🤑 Зарплата',
        EN: '🤑 Salary',
    },
    DELETE: {
        RU: '🗑 You are deleted, {}!',
        EN: '🗑 Ваша учетная запись удалена, {}!',
    },
    CANCEL: {
        RU: '/cancel',
        EN: '/отмена',
    },
    HOW_MUCH_EARN: {
        RU: '❔How much did you earn?:',
        EN: '❔Сколько вы заработали?:',
    },
    SELECT_GROUP: {
        RU: 'Select group',
        EN: 'Выберите группу',
    },
    THATS_YOUR_INCOME: {
        RU: 'Это ваш доход!',
        EN: 'That\'s your income!',
    },
    INCOME_ADDED: {
        RU: '✅ Ваш доход добавлен!',
        EN: '✅ Your income has been added!',
    },
    SEEYA: {
        RU: '👋🏼 Пока пока!',
        EN: '👋🏼 See ya!',
    },


}


def gettext(msg_key, lang, *args, **kwargs):
    logger.info(f'USERLANG GET_TEXT *****{lang}*****###{args}###{kwargs}')
    if msg_key not in TRANSLATES:
        raise ValueError(f"Not found translate for {msg_key}!")
    message = TRANSLATES[msg_key].get(lang)
    if message is None:
        logger.info(f'IF MESSAGE NONE *****{message}*****###{args}###{kwargs}')
        message = TRANSLATES[msg_key].get(DEFAULT)
    if message is None:
        raise ValueError(f"Not found translate for default {msg_key}!")

    return message.format(*args, **kwargs)
