from sqlalchemy import create_engine, Integer, String, Column, MetaData, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import time

db_server = "localhost"
db_user = "root"
db_name = "phptest"
db_pass = ""
db_uri = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_server}/{db_name}"
Base = declarative_base()
class UserData(Base):
    __tablename__ = 'advice'  # Đảm bảo rằng đây là tên bảng chính xác trong cơ sở dữ liệu
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

try:
    engine = create_engine(db_uri)
    print("conected")
except:
    print("erro")




def insert(question  , answer):
    session = sessionmaker(bind = engine)
    session = session()
    newdata = UserData(question = question , answer = answer)
    session.add(newdata)
    session.commit()



    