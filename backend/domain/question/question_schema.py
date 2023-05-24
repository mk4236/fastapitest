import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


class QuestionBase(BaseModel):
    title: str
    content: str


class Question(QuestionBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    answers: List[Answer] = []
    user: User | None
    voter: list[User] = []

    class Config:
        orm_mode = True
        json_encoders = {
            datetime.datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M")
        }


class QuestionUpdate(QuestionBase):
    pass


class QuestionCreate(QuestionBase):
    pass


class QuestionList(BaseModel):
    questions: List[Question]
    total: int


class QuestionVote(BaseModel):
    question_id: int
