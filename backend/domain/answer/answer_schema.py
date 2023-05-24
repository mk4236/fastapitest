from datetime import datetime
from pydantic import BaseModel, Field, validator
from domain.user.user_schema import User


class AnswerBase(BaseModel):
    content: str = Field(..., min_length=1)

    @validator('content')
    def validate_content(cls, content):
        if not content.strip():
            raise ValueError('Content cannot be empty')
        return content


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: User | None
    question_id: int
    voter: list[User] = []

    class Config:
        orm_mode = True


class AnswerVote(BaseModel):
    answer_id: int
