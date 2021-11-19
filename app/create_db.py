# У пользователя должна быть возможность внести потраченную сумму и какой-то комментарий,
# затем добаввить эту потраченную сумму в определенную группу/категорию

# Должна быть возможность:
# - удалять покупки если ошибся
# - исправлять внесунную суму или комментарий

# У пользователя должна быть возможность добавлять заработанную сумму и комментарий к ней
# - удалять и исправлять

# Есть дефолтные таблицы/категории ПРОДУКТЫ, КОФЕ, ПРОЕЗД, ПЛАТЕЖИ, РАЗНОЕ, ДОХОД
# Дать пользователю возможность создавать новую категорию
# Должен быть хендлер, который подсчитает сколько потрачено денег в какой-то определенной группе или во всех вместе
# Этот подсчет это некий временный чек что происходит с твоими доходами и расходами

# Должен быть хендлер, который подсчитает общий ДОХОД/РАСХОД
# Общий подсчет ДОХОДОВ/РАСХОДОВ должен происходить первого числа нового месяца

# Таблицы:
# Users, Groups, Purchase, Income


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Group, Purchase

if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    User.metadata.drop_all(engine)
    Group.metadata.drop_all(engine)
    Purchase.metadata.drop_all(engine)

    User.metadata.create_all(engine)
    Group.metadata.create_all(engine)
    Purchase.metadata.create_all(engine)

    Session = sessionmaker(engine)
