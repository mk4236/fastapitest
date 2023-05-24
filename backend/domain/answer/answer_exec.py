from typing import List
from sqlalchemy.orm import Session
from models import Answer, User
from domain.answer.answer_schema import AnswerCreate, AnswerUpdate


def get_answer_exec(db: Session, answer_id: int) -> Answer:
    """
    답변 상세
    """
    result = db.query(Answer).filter(Answer.id == answer_id).first()
    return result


def get_answers_exec(db: Session, question_id: int, skip: int = 0, limit: int = 100) -> List[Answer]:
    """
    답변 목록
    """
    result = db.query(Answer).filter(Answer.question_id ==
                                     question_id).offset(skip).limit(limit).all()
    return result


def create_answer_exec(db: Session, answer: AnswerCreate, question_id: int, user: User) -> Answer:
    """
    답변 생성
    """
    answer_data = Answer(question_id=question_id, user=user, **answer.dict())
    db.add(answer_data)
    db.commit()
    db.refresh(answer_data)
    return answer_data


def update_answer_exec(db: Session, answer: Answer, answer_update: AnswerUpdate) -> Answer:
    """
    답변 수정
    """
    for field, value in answer_update.dict(exclude_unset=True).items():
        setattr(answer, field, value)
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer_exec(db: Session, answer: Answer) -> None:
    """
    답변 삭제
    """
    db.delete(answer)
    db.commit()


def vote_answer_exec(db: Session, db_answer: Answer, db_user: User):
    """
    질문 좋아요
    """
    db_answer.voter.append(db_user)
    db.commit()
