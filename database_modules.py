from datetime import date, time
from sqlalchemy import Integer, Date, Time, String, ForeignKey, create_engine
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'Users'

    userLogin:Mapped[str] = mapped_column(String, primary_key=True)
    userPassword:Mapped[str] = mapped_column(String, nullable=False)

class Notes(Base):
    __tablename__ = 'Notes'

    noteID:Mapped[int] = mapped_column(Integer, primary_key = True)
    noteDate:Mapped[date] = mapped_column(Date, nullable=True)
    noteTime:Mapped[time] = mapped_column(Time, nullable=True)
    noteText:Mapped[str] = mapped_column(String, nullable=False)
    noteUser:Mapped[str] = mapped_column(String, ForeignKey("Users.userLogin"))

def createDatabase():
    engine = create_engine(f'sqlite:///NotepadDatabase.db')
    Base.metadata.create_all(engine)

if __name__=='__main__':
    createDatabase()