import logging

logger = logging.getLogger(__name__)

RU = 'ru'
EN = 'en'
UK = 'uk'
DEFAULT = EN

# main menu
CREATE_NEW_EXPENSE = 'create new expense'
CREATE_EXPENSE_CATEGORY = 'create new expense category'
ALL_EXPENSES = 'see all expenses'
CREATE_NEW_INCOME = 'create new income'
CREATE_INCOME_CATEGORY = 'create new income category'
ALL_INCOMES = 'see all incomes'
LAST_MONTH = "see statistic of last month"
LANGUAGE_NAME = 'language name'

# Registration
REGISTERED = 'register'
INCOGNITO = 'incognito'
ALREADY_REGISTERED = 'already registered'
STOP_IT = 'stop it'

# Default names of categories
GROCERIES = 'groseries'
TRANSPORT = 'transport'
BILLS = 'bills'
MISCELLANEOUS = 'miscellaneous'
SALARY = 'salary'
DELETE = 'delete'

WRONG_VALUE = 'Enter the only digits'

# Create income
INCOME_TITLE = 'income title'
HOW_MUCH_EARN = 'how much did you earn'
SELECT_CATEGORY = 'select group'
THATS_YOUR_INCOME = 'That\'s your income'
DISPLAY_INCOME = 'display income'
INCOME_ADDED = 'income added'
SEEYA = 'See ya'

# Create expense
EXPENSE_TITLE = 'expence title'
HOW_MUCH_SPEND = 'how much did you spend'
THATS_YOUR_EXPENSE = 'that\'s your expence'
DISPLAY_EXPENSE = 'display expense'
EXPENSE_ADDED = 'expence added'

SAVE = 'savesave'
DONT_SAVE = 'don\'t savesave'

ONCE_MESSAGE = 'Special message for all users'
DAILY_MESSAGE = 'Don’t forget to fill in your expenses and incomes for today!'

# Monthly expense/income report
YOUR_MONTHLY_EXPENSES = 'your monthly expenses'
YOUR_MONTHLY_INCOME = 'your monthly income'

# Months
JANUARY = 'January'
FABRUARY = 'Fabruary'
MARCH = 'March'
APRIL = 'April'
MAY = 'May'
JUNE = 'June'
JULY = 'July'
AUGUST = 'August'
SEPTEMBER = 'September'
OCTOBER = 'October'
NOVEMBER = 'November'
DECEMBER = 'December'

# Current expense/income report
REPORT_INCOME_CATEGORIES = 'Sum of incomes in categories'
REPORT_EXPENSE_CATEGORIES = 'Sum of expense in categories'
TOTAL = 'total'
OVER_ALL_INCOMES = 'overall incomes'
OVER_ALL_EXPENSES = 'overall expenses'
SIGN = '$ ₴'

# Create expense/income category
NAME_INCOME_CATEGORY = 'Enter name of the new income category!'
NAME_EXPENSE_CATEGORY = 'Enter name of the new expense category!'
IS_CORRECT = 'The name for new category is correct?'
YES = 'YES'
NO = 'NO'
CATEGORY_CREATED = 'The category was created!'

# Translation
CHANGE_LANG = 'Change language'
YOUR_LANG_CHANGED = 'Language change to...'

CANCEL_THIS = 'cancel translation'

TRANSLATES = {
    REGISTERED: {
        UK: '✅ Ви зареєстровані, {}!',
        RU: '✅ Вы зарегестрированы, {}!',
        EN: '✅ You are registered, {}!',
    },
    INCOGNITO: {
        UK: 'безіменний користувач',
        RU: 'безымянный пользователь',
        EN: 'nameless user',
    },
    ALREADY_REGISTERED: {
        UK: '🟢 Ви вже зареєстровані {}. ',
        RU: '🟢 Вы уже зарегестрированы️ {}. ',
        EN: '🟢 You are already registered {}. ',
    },
    STOP_IT: {
        UK: 'Досить вже тицяти на start, я замахався вже...😩',
        RU: 'Хватит нажимать на start, я устал уже...😩',
        EN: 'Stop it, I\'m tired...😩'
    },
    DELETE: {
        UK: '🗑 Ваш обліковий запис видалено, {}!',
        RU: '🗑 Ваша учетная запись удалена, {}!',
        EN: '🗑 You are deleted, {}!',
    },
    GROCERIES: {
        UK: '🏠 Продукти та все для дому',
        RU: '🏠 Продукты и все для дома',
        EN: '🏠 Groceries and home appliances',
    },
    TRANSPORT: {
        UK: '🚘 Транспорт',
        RU: '🚘 Транспорт',
        EN: '🚘 Transport',
    },
    BILLS: {
        UK: '💵 Комунальні послуги',
        RU: '💵 Коммунальные',
        EN: '💵 Bills',
    },
    MISCELLANEOUS: {
        UK: '🛍 Різне',
        RU: '🛍 Разное',
        EN: '🛍 Miscellaneous',
    },
    SALARY: {
        UK: '🤑 Заробітна плата',
        RU: '🤑 Зарплата',
        EN: '🤑 Salary',
    },
    CREATE_NEW_INCOME: {
        UK: '🟩 Додати дохід',
        RU: '🟩 Внести доход',
        EN: '🟩 Create new income',
    },
    CREATE_INCOME_CATEGORY: {
        UK: '📥 Створити категорію доходу',
        RU: '📥 Создать категорию дохода',
        EN: '📥 Create new income category',
    },
    ALL_INCOMES: {
        UK: '📉 Статистика доходів',
        RU: '📉 Статистика доходов',
        EN: '📉 Income statistics',
    },
    CREATE_NEW_EXPENSE: {
        UK: '🟥 Додати витрату',
        RU: '🟥 Внести расход',
        EN: '🟥 Create new expense',
    },
    CREATE_EXPENSE_CATEGORY: {
        UK: '📤 Створити категорію витрат',
        RU: '📤 Создать категорию расходов',
        EN: '📤 Create new expense category',
    },
    ALL_EXPENSES: {
        UK: '📈 Статистика витрат',
        RU: '📈 Статистика расходов',
        EN: '📈 Expenses statistics',
    },
    LAST_MONTH: {
        UK: '📊 Статистика за минулий місяць',
        RU: '📊 Статистика за прошлый месяц',
        EN: '📊 Statistic for the last month',
    },
    LANGUAGE_NAME: {
        UK: '🇺🇦 Мова',
        RU: '🏳️ Язык',
        EN: '🇬🇧 Language',
    },
    WRONG_VALUE: {
        UK: '🤥 Упс! Потрібні цифри! Спробуйте ще раз!',
        RU: '🤥 Упс! Нужны цифры! Попробуйте еще раз!',
        EN: '🤥 Oops! Use the digits! Try again!',
    },
    INCOME_TITLE: {
        UK: 'Введіть назву доходу:',
        RU: 'Введите название дохода:',
        EN: 'Enter your income title:',
    },
    HOW_MUCH_EARN: {
        UK: 'Введіть суму доходу:',
        RU: 'Введите сумму дохода:',
        EN: 'How much did you earn?',
    },
    SELECT_CATEGORY: {
        UK: 'Оберіть категорію:',
        RU: 'Выберите категорию:',
        EN: 'Select category:',
    },
    DISPLAY_INCOME: {
        UK: (
            '_Назва: {}\n_'
            '_Дохід: {}\n_'
            '_Категорія: {}\n_'
            '_Дата створення: {}_'
        ),
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
        UK: '*Це ваш дохід!*\n{}',
        RU: '*Это ваш доход!*\n{}',
        EN: '*That\'s your income!*\n{}',
    },
    INCOME_ADDED: {
        UK: '✅ Ваш дохід додано!',
        RU: '✅ Ваш доход добавлен!',
        EN: '✅ Your income has been added!',
    },
    SEEYA: {
        UK: '👋🏼 Бувай!',
        RU: '👋🏼 Пока пока!',
        EN: '👋🏼 See ya!',
    },
    EXPENSE_TITLE: {
        UK: 'Введіть назву витрати:',
        RU: 'Введите название расхода:',
        EN: 'Enter your expense title:',
    },
    HOW_MUCH_SPEND: {
        UK: 'Введіть витрачену суму:',
        RU: 'Введите расходную сумму:',
        EN: 'How much did you spend?',
    },
    THATS_YOUR_EXPENSE: {
        UK: '*Ваша витрата!*\n{}',
        RU: '*Ваш расход!*\n{}',
        EN: '*That\'s your expense!*\n{}',
    },
    DISPLAY_EXPENSE: {
        UK: (
            '_Назва: {}\n_'
            '_Витрата: {}\n_'
            '_Категорія: {}\n_'
            '_Дата створення: {}_'
        ),
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
        UK: '✅ Вашу витрату додано!',
        RU: '✅ Ваш расход добавлен!',
        EN: '✅ Your expense has been added!',
    },
    SAVE: {
        UK: '🟢 Зберегти',
        RU: '🟢 Сохрнанить',
        EN: '🟢 Save',
    },
    DONT_SAVE: {
        UK: '🔴 Скасувати',
        RU: '🔴 Отмена',
        EN: '🔴 Don\'t save',
    },
    ONCE_MESSAGE:{
        UK: ('🙏🏼🫶🏼🇺🇦 Слава Україні! Дякую, що використовуєте Wallet-Tracker для підрахунку своїх доходів та витрат! '
             'Кожного для ми робимо усе можливе, аби бот ставав дедалі краще. '
             'Якщо ви бажаєте підтримати молодого розробника, '
             'ви можете це зробити за допомогою переказу на картку по Україні 💳:'),
        RU: ('🙏🏼🫶🏼🇺🇦 Спасибо, что используете Wallet-Tracker для подсчета своих доходов и расходов! '
             'Каждый день мы делаем все возможное, чтобы бот становился все лучше. '
             'Если вы желает поддержать молодого разработчика, '
             'вы можете это сделать с помощью перевода на карту по Украине 💳:'),
        EN: ('🙏🏼🫶🏼🇺🇦 Glory to Ukraine! Thank you for using Wallet-Tracker to keep track of your income and expenses!'
             'Every day we do our best to make the bot better and better. '
             'If you want to support a young developer, '
             'you can do this via transfer to Ukrainian bank card 💳:'),
    },
    DAILY_MESSAGE: {
        UK: '💭 Не забудьте внести свої доходи та витрати за сьогодні! Слава Україні! 🇺🇦',
        RU: '💭 Не забудьте внести свои доходы и расходы за сегодня!',
        EN: '💭 Don’t forget to enter your incomes and expenses for today!',
    },
    YOUR_MONTHLY_INCOME: {
        UK: '🟩 *Звіт по доходах за {}:*',
        RU: '🟩 *Отчет по доходам за {}:*',
        EN: '🟩 *Report on income for {}:*',
    },
    YOUR_MONTHLY_EXPENSES: {
        UK: '🟥 *Звіт по витратах за {}:*',
        RU: '🟥 *Отчет по расходам за {}:*',
        EN: '🟥 *Report on expenses for {}:*',
    },
    JANUARY: {
        UK: 'Січень',
        RU: 'Январь',
        EN: 'January',
    },
    FABRUARY: {
        UK: 'Лютий',
        RU: 'Февраль',
        EN: 'February',
    },
    MARCH: {
        UK: 'Березень',
        RU: 'Март',
        EN: 'March',
    },
    APRIL: {
        UK: 'Квітень',
        RU: 'Апрель',
        EN: 'April',
    },
    MAY: {
        UK: 'Травень',
        RU: 'Май',
        EN: 'May',
    },
    JUNE: {
        UK: 'Червень',
        RU: 'Июнь',
        EN: 'June',
    },
    JULY: {
        UK: 'Липень',
        RU: 'Июль',
        EN: 'July',
    },
    AUGUST: {
        UK: 'Серпень',
        RU: 'Август',
        EN: 'August',
    },
    SEPTEMBER: {
        UK: 'Вересень',
        RU: 'Сентябрь',
        EN: 'September',
    },
    OCTOBER: {
        UK: 'Жовтень',
        RU: 'Октябрь',
        EN: 'October',
    },
    NOVEMBER: {
        UK: 'Листопад',
        RU: 'Ноябрь',
        EN: 'November',
    },
    DECEMBER: {
        UK: 'Грудень',
        RU: 'Декабрь',
        EN: 'December',
    },
    REPORT_INCOME_CATEGORIES: {
        UK: '*Сума доходів по категоріям:*',
        RU: '*Сумма доходов по категориям:*',
        EN: '*Sum of incomes in categories:*',
    },
    REPORT_EXPENSE_CATEGORIES: {
        UK: '*Сума витрат по категоріям:*',
        RU: '*Сумма расходов по категориям:*',
        EN: '*Sum of expenses in categories:*',
    },
    TOTAL: {
        UK: '__Разом: ₴ {}__',
        RU: '__Итого: ₴ {}__',
        EN: '__Total: $ {}__',
    },
    OVER_ALL_INCOMES: {
        UK: '*РАЗОМ: ₴ {}*',
        RU: '*ОБЩАЯ СУММА: ₴ {}*',
        EN: '*TOTAL: $ {}*',
    },
    OVER_ALL_EXPENSES: {
        UK: '*РАЗОМ: ₴ {}*',
        RU: '*ОБЩАЯ СУММА: ₴ {}*',
        EN: '*TOTAL: $ {}*',
    },
    SIGN: {
        UK: '₴',
        RU: '₴',
        EN: '$',
    },
    YES: {
        UK: '🟢 Так',
        RU: '🟢 Да',
        EN: '🟢 Yes',
    },
    NO: {
        UK: '🔴 Ні',
        RU: '🔴 Нет',
        EN: '🔴 No',
    },
    NAME_INCOME_CATEGORY: {
        UK: 'Введіть ім\'я нової категорії доходу:',
        RU: 'Введите имя новой категории дохода:',
        EN: 'Enter name of the new income category:',
    },
    NAME_EXPENSE_CATEGORY: {
        UK: 'Введіть ім\'я нової категорії витрат:',
        RU: 'Введите имя новой категории расхода:',
        EN: 'Enter name of the new expense category:',
    },
    IS_CORRECT: {
        UK: 'Ім\'я нової \'{}\' категорії вірне?',
        RU: 'Имя новой \'{}\' категории верное?',
        EN: 'The name \'{}\' for new category is correct?',
    },
    CATEGORY_CREATED: {
        UK: '✅ Нова категорія \'{}\' створена!',
        RU: '✅ Новая категория \'{}\' создана!',
        EN: '✅ The new category \'{}\' was created!',
    },
    CHANGE_LANG: {
        UK: 'Виберіть мову:',
        RU: 'Выберите язык:',
        EN: 'Select the language:',
    },
    YOUR_LANG_CHANGED: {
        UK: '✅ Мову змінено на {} Слава Україні!',
        RU: '✅ Язык изменен на {}',
        EN: '✅ Language changed to {}',
    },
    CANCEL_THIS: {
        UK: 'Скасувати',
        RU: 'Отмена',
        EN: 'Cancel',
    },

}


def gettext(msg_key, lang, *args, **kwargs):
    logger.info(f'FUNC GET_TEXT USERLANG *****{lang}*****###{args}###{kwargs}')
    if msg_key not in TRANSLATES:
        raise ValueError(f"Not found translate for {msg_key}!")
    message = TRANSLATES[msg_key].get(lang)
    if message is None:
        logger.info(f'IF MESSAGE NONE *****{message}*****###{args}###{kwargs}')
        message = TRANSLATES[msg_key].get(DEFAULT)
    if message is None:
        raise ValueError(f"Not found translate for default {msg_key}!")

    return message.format(*args, **kwargs)
