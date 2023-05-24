from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from .answer_exec import get_answers_exec, get_answer_exec, create_answer_exec, update_answer_exec, delete_answer_exec, vote_answer_exec
from .answer_schema import Answer, AnswerCreate, AnswerUpdate, AnswerVote
from databases import get_db

from domain.user.user_router import get_current_user
from models import User

router = APIRouter(prefix="/api/answer")


@router.get("/{question_id}/", response_model=List[Answer])
def read_answers_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    답변 목록
    """
    answers = get_answers_exec(db, skip=skip, limit=limit)
    return answers


@router.get("/detail/{answer_id}/", response_model=Answer)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    """
    답변 상세
    """
    answer = get_answer_exec(db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.post("/{question_id}/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def create_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    답변 생성
    """
    return create_answer_exec(db=db, question_id=question_id, answer=answer, user=current_user)


@router.put("/{answer_id}/", response_model=Answer)
def update_answer(
    answer_id: int,
    answer_update: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    답변 수정
    """
    answer = get_answer_exec(db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    if answer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return update_answer_exec(db, answer=answer, answer_update=answer_update)


@router.delete("/{answer_id}/")
def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    답변 삭제
    """
    answer = get_answer_exec(db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    if answer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    delete_answer_exec(db, answer=answer)
    return {"message": "Answer deleted"}


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(_answer_vote: AnswerVote,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_answer = get_answer_exec(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    vote_answer_exec(
        db, db_answer=db_answer, db_user=current_user)
