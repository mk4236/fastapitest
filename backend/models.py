import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

"""
문제 좋아요 N:N
"""
question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey(
        'questions.id'), primary_key=True)
)

"""
답변 좋아요 N:N
"""
answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answers.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)
    answers = relationship("Answer", back_populates="question",
                           cascade="all, delete-orphan")  # Answer와의 관계 설정
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="questions")
    voter = relationship('User', secondary=question_voter,
                         backref='question_voters')

    class Config:
        orm_mode = True


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)
    question_id = Column(Integer, ForeignKey(
        "questions.id"))  # Question과의 관계 설정
    question = relationship(
        "Question", back_populates="answers")  # Question과의 관계 설정
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    voter = relationship('User', secondary=answer_voter,
                         backref='answer_voters')

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
