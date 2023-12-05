from sqlalchemy import create_engine, Integer, String, Column, MetaData , Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import time

db_path = r"\\172.15.1.11\20_学科共有\50_国際ビジネス\db\Test.db"  # Thay 'your_database.db' bằng tên file cơ sở dữ liệu thực tế
# db_path = r""
# Tạo engine kết nối
engine = create_engine(f'sqlite:///{db_path}')
metadata = MetaData()
base = declarative_base()

# Định nghĩa lớp mô hình
class UserData(base):
    __tablename__ = 'user_data'  # Đảm bảo rằng đây là tên bảng chính xác trong cơ sở dữ liệu
    Id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    is_new= Column(Boolean)

# Tạo session
def question():
    Session = sessionmaker(bind=engine)
    session = Session()

    question = {}
    # Truy vấn dữ liệu
    data_list = session.query(UserData).all()
    if data_list:
        for data in data_list:
            # if data.is_new == True:
            question[data.Id] = data.question
    else:
        print("Không có dữ liệu")
    return question
def update_anwser(id , ans):
    Session = sessionmaker(bind=engine)
    session = Session()
    user_to_update = session.query(UserData).filter(UserData.Id == id).first()
    user_to_update.answer = ans
    session.commit()
    # for key , values in question.items():
    #     print(f"{key} + {values}")



def mess(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user_to_update = session.query(UserData).filter(UserData.Id == id).first()
    print(user_to_update.answer)

