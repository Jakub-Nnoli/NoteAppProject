from datetime import date, time
from sqlalchemy import Integer, Date, Time, String, ForeignKey, create_engine, select
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'Users'

    userLogin:Mapped[str] = mapped_column(String, primary_key=True)
    userPassword:Mapped[str] = mapped_column(String, nullable=False)
    userEmail:Mapped[str] = mapped_column(String, nullable=False, info={'check_constraint': "userEmail ~ '^[\w\.-]+@[\w\.-]+\.\w+$'"})

class Notes(Base):
    __tablename__ = 'Notes'

    noteID:Mapped[int] = mapped_column(Integer, primary_key = True)
    noteDate:Mapped[date] = mapped_column(Date, nullable=True)
    noteTime:Mapped[time] = mapped_column(Time, nullable=True)
    noteText:Mapped[str] = mapped_column(String, nullable=False)
    noteUser:Mapped[str] = mapped_column(String, ForeignKey("Users.userLogin"))