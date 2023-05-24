from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
회원가입
"""
def create_user_exec(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()


"""
중복확인
"""
def get_existing_user_exec(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()


"""
사용자명으로 사용자 모델객체를 리턴
"""
def get_user_exec(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()