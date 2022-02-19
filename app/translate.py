import logging
from telegram import ParseMode

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

INCOME_TITLE = 'income title'
HOW_MUCH_EARN = 'how much did you earn'
SELECT_GROUP = 'select group'
THATS_YOUR_INCOME = 'That\'s your income'
DISPLAY_INCOME = 'display income'
INCOME_ADDED = 'income added'
SEEYA = 'See ya'

EXPENSE_TITLE = 'expence title'
HOW_MUCH_SPEND = 'how much did you spend'
THATS_YOUR_EXPENSE = 'that\'s your expence'
DISPLAY_EXPENSE = 'display income'
EXPENSE_ADDED = 'expence added'

SAVE = 'save'
DONT_SAVE = 'don\'t save'

DAILY_MESSAGE = 'Don’t forget to fill in your expenses and incomes for today!'

MONTHLY_INCOME = 'monthly income'
MONTHLY_EXPENSE = 'monthly expense'

REPORT_INCOME_CATEGORIES = 'Sum of incomes in categories'
REPORT_EXPENSE_CATEGORIES = 'Sum of expense in categories'
TOTAL = 'total'
OVER_ALL = 'overall'
SIGN = '$ ₴'

YES_CAPS = 'YES'
NO_CAPS = 'NO'
YES_NO = 'Yes/No'
NAME_INCOME_CATEGORY = 'Enter name of the new income category!'
IS_CORRECT = 'The name for new category is correct?'
CATEGORY_CREATED = 'The category was created!'

NAME_EXPENSE_CATEGORY = 'Enter name of the new expense group!'

TRANSLATES = {
    REGISTERED: {
        RU: '✅ Вы зарегестрированы, {}!',
        EN: '✅ You are registered, {}!',
    },
    INCOGNITO: {
        RU: 'безымянный пользователь',
        EN: 'nameless user',
    },
    ALREADY_REGISTERED: {
        RU: '❗Вы уже зарегестрированы️ {}',
        EN: '❗️You are already registered',
    },
    STOP_IT: {
        RU: ' Остановитесь, я устал уже...😩',
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
        RU: '🗑 Ваша учетная запись удалена, {}!',
        EN: '🗑 You are deleted, {}!',
    },
    INCOME_TITLE: {
        RU: 'Введите название дохода:',
        EN: 'Enter your income title:',
    },
    HOW_MUCH_EARN: {
        RU: 'Введите сумму дохода:',
        EN: 'How much did you earn?:',
    },
    SELECT_GROUP: {
        RU: 'Select group:',
        EN: 'Выберите категорию:',
    },
    DISPLAY_INCOME: {
        RU: (
            '_Название: {}\n_'
            '_Доход: {}\n_'
            '_Категория: {}\n_'
            '_Дата добавления: {}_'
        ),
        EN: (
            '_Title: {}_\n'
            '_Earned Money: {}_\n'
            '_Category: {}_\n'
            '_Creation Date: {}_'
        )
    },
    THATS_YOUR_INCOME: {
        RU: '*Это ваш доход!*\n{}',
        EN: '*That\'s your income!*\n{}',
    },
    INCOME_ADDED: {
        RU: '✅ Ваш доход добавлен!',
        EN: '✅ Your income has been added!',
    },
    SEEYA: {
        RU: '👋🏼 Пока пока!',
        EN: '👋🏼 See ya!',
    },
    EXPENSE_TITLE: {
        RU: 'Введите название расхода:',
        EN: 'Enter your expense title:',
    },
    HOW_MUCH_SPEND: {
        RU: 'Введите расходную сумму:',
        EN: 'How much did you spend?:',
    },
    THATS_YOUR_EXPENSE: {
        RU: '*Ваш расход!*\n{}',
        EN: '*That\'s your expense!*\n{}',
    },
    DISPLAY_EXPENSE: {
        RU: (
            '_Название: {}_\n'
            '_Расход: {}_\n'
            '_Категория: {}_\n'
            '_Дата добавления: {}_'
        ),
        EN: (
            '_Title: {}_\n'
            '_Spent Money: {}_\n'
            '_Category: {}_\n'
            '_Creation Date: {}_'
        )
    },
    EXPENSE_ADDED: {
        RU: '✅ Ваш расход добавлен!',
        EN: '✅ Your expense has been added!',
    },
    SAVE: {
        RU: 'Сохранить',
        EN: 'Save',
    },
    DONT_SAVE: {
        RU: 'Отмена',
        EN: 'Don\'t save',
    },
    DAILY_MESSAGE: {
        RU: 'Не забудьте внести свои доходы и растраты за сегодня!',
        EN: 'Don’t forget to enter your incomes and expenses for today!',
    },
    MONTHLY_INCOME: {
        RU: '*Ваш месячный доход:* _₴ {}_',
        EN: '*Your monthly income:* _$ {}_',
    },
    MONTHLY_EXPENSE: {
        RU: '*Ваш месячный расход:* _₴ {}_',
        EN: '*Your monthly expense:* _$ {}_',
    },
    REPORT_INCOME_CATEGORIES: {
        RU: '*Сумма доходов по категориям:*',
        EN: '*Sum of incomes in categories:*',
    },
    REPORT_EXPENSE_CATEGORIES: {
        RU: '*Сумма расходов по категориям:*',
        EN: '*Sum of expenses in categories:*',
    },
    TOTAL: {
        RU: '*Итого: ₴ {}*',
        EN: '*Total: $ {}*',
    },
    OVER_ALL: {
        RU: '*Общая сумма доходов: ₴ {}*',
        EN: '*Total of all incomes: $ {}*',  # ПРОВЕРИТЬ
    },
    SIGN: {
        RU: '₴',
        EN: '$',
    },
    YES_CAPS: {
        RU: 'ДА',
        EN: 'YES',
    },
    NO_CAPS: {
        RU: 'НЕТ',
        EN: 'NO',
    },
    YES_NO: {
        RU: 'Да/Нет?',
        EN: 'Yes/No?',
    },
    NAME_INCOME_CATEGORY: {
        RU: 'Введите имя новой категории дохода!',
        EN: 'Enter name of the new income category!',
    },
    IS_CORRECT: {
        RU: 'Имя новой \'{}\' категории верно?',
        EN: 'The name \'{}\' for new category is correct?',
    },
    CATEGORY_CREATED: {
        RU: '✅ Новая категория \'{}\' создана!',
        EN: '✅ The new category \'{}\' was created!',
    },
    NAME_EXPENSE_CATEGORY: {
        RU: 'Введите имя новой категории дохода!',
        EN: 'Enter name of the new expense category!',
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
