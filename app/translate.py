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

TRANSLATES = {
    REGISTERED: {
        RU: '✅ Вы зарегестрированы, {}!"',
        EN: '✅ You are registered, {}!',
    },
    INCOGNITO: {
        RU: '❔Неизвестный',
        EN: '❔Incognito',
    },
    ALREADY_REGISTERED: {
        RU: '❗️ You are already registered',
        EN: '❗️ Вы уже зарегестрированы',
    },
    STOP_IT: {
        RU: ' Stop it, I\'m tired...😩',
        EN: ' Остановись, я так устал уже...😩'
    }
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
    }


}


def gettext(msg_key, user, *args, **kwargs):
    if msg_key not in TRANSLATES:
        raise ValueError(f"Not found translate for {msg_key}!")
    message = TRANSLATES[msg_key].get(user.lang)
    if message is None:
        message = TRANSLATES[msg_key].get(DEFAULT)
    if message is None:
        raise ValueError(f"Not found translate for default {msg_key}!")

    return message.format(*args, **kwargs)
