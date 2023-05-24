from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Answer, Question, User
from domain.question.question_schema import QuestionCreate, QuestionUpdate


def get_question_exec(db: Session, question_id: int) -> Question:
    """
    질문 상세
    """
    result = db.query(Question).filter(Question.id == question_id).first()
    return result


def get_questions_exec(
    db: Session,
    search_str: str = "",
    skip: int = 0,
    limit: int = 100,
    order_by: str = "created_at",
    ascending: bool = False
) -> List[Question]:
    """
    질문 목록
    """
    order_field = getattr(Question, order_by)

    if ascending:
        _questions = db.query(Question).order_by(order_field)
    else:
        _questions = db.query(Question).order_by(order_field.desc())

    if search_str:
        search_pattern = f"%{search_str}%"
        _questions = _questions.filter(
            or_(
                Question.title.like(search_pattern),
                Question.user.has(User.username.like(search_pattern)),
                Question.content.like(search_pattern),
                Question.answers.any(Answer.content.like(search_pattern))
            )
        )

    total = _questions.count()
    questions = _questions.offset(skip).limit(limit).all()

    return total, questions


def create_question_exec(db: Session, question: QuestionCreate, user: User) -> Question:
    """
    질문 생성
    """
    question_data = Question(**question.dict(), user=user)
    db.add(question_data)
    db.commit()
    db.refresh(question_data)
    return question_data


def update_question_exec(db: Session, question: Question, question_update: QuestionUpdate) -> Question:
    """
    질문 수정
    """
    for field, value in question_update.dict(exclude_unset=True).items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question


def delete_question_exec(db: Session, question: Question) -> None:
    """
    질문 삭제
    """
    db.delete(question)
    db.commit()


def vote_question_exec(db: Session, db_question: Question, db_user: User):
    """
    질문 좋아요
    """
    db_question.voter.append(db_user)
    db.commit()
