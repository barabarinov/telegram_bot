from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, FLOAT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    monthly_report = Column(Boolean, default=True)

    purchases = relationship(
        "Purchase", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    groups = relationship(
        "Group", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    incomes = relationship(
        "Income", back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f'User {self.id} with telegram id: {self.telegram_id}'


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    name = Column(String(32))

    user = relationship("User", back_populates="groups")
    purchases = relationship("Purchase", back_populates="group")
    incomes = relationship("Income", back_populates="group")

    def __repr__(self):
        return f'Group {self.name}'


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="purchases")

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)
    group = relationship('Group', back_populates="purchases")

    description = Column(String(64), nullable=False)
    spent_money = Column(FLOAT, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=DateTime.datetime.now)

    def __repr__(self):
        return f'Purchase #{self.id}: {self.description[:20]}'


class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    user = relationship('User', back_populates="incomes")

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)
    group = relationship('Group', back_populates="incomes")

    description = Column(String(64), nullable=False)
    earned_money = Column(FLOAT, nullable=False)
    # заработанные деньги

    def __repr__(self):
        return f'Income #{self.id}: {self.description[:20]}'
