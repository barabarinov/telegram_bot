from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, FLOAT
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    enable_monthly_report = Column(Boolean, default=True)

    incomes = relationship(
        "Income", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    purchases = relationship(
        "Purchase", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    groups_purchases = relationship(
        "GroupPurchase", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    groups_incomes = relationship(
        "GroupIncome", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f'User with telegram id: {self.telegram_id}'


class GroupPurchase(Base):
    __tablename__ = 'groups_purchases'

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    name = Column(String(32))

    user = relationship("User", back_populates="groups_purchases")
    purchases = relationship("Purchase", back_populates="group")

    def __repr__(self):
        return f'Group of Purchases: {self.name}'


class GroupIncome(Base):
    __tablename__ = 'groups_incomes'

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    name = Column(String(32))

    user = relationship("User", back_populates="groups_incomes")
    incomes = relationship("Income", back_populates="group")

    def __repr__(self):
        return f'Group of Incomes: {self.name}'


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="purchases")

    group_id = Column(Integer, ForeignKey('groups_purchases.id', ondelete='SET NULL'), nullable=False)
    group = relationship('GroupPurchase', back_populates="purchases")

    title = Column(String(64), nullable=False)
    spent_money = Column(FLOAT, nullable=False)
    creation_date = Column(
        DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'Purchase #{self.id}: {self.title[:20]}'

    def display_purchase(self):
        return (
            f'Title: {self.title}\n'
            f'Spent Money: {self.spent_money}\n'
            f'Group: {self.group.name if self.group else None}\n'
            f'Creation Date: {self.creation_date.strftime("%H:%M %d/%m/%Y")}'
        )


class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="incomes")

    group_id = Column(Integer, ForeignKey('groups_incomes.id', ondelete='SET NULL'), nullable=False)
    group = relationship('GroupIncome', back_populates="incomes")

    title = Column(String(64), nullable=False)
    earned_money = Column(FLOAT, nullable=False)
    creation_date = Column(
        DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'Income #{self.id}: {self.title[:20]}'

    def display_income(self):
        return (
            f'Title: {self.title}\n'
            f'Earned Money: {self.earned_money}\n'
            f'Group: {self.group.name if self.group else None}\n'
            f'Creation Date: {self.creation_date.strftime("%H:%M %d/%m/%Y")}'
        )
