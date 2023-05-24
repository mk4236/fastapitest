from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from databases import get_db
from domain.user.user_router import get_current_user
from starlette import status

from .question_exec import (
    get_questions_exec,
    get_question_exec,
    create_question_exec,
    update_question_exec,
    delete_question_exec,
    vote_question_exec,
)
from .question_schema import Question, QuestionCreate, QuestionUpdate, QuestionList, QuestionVote

router = APIRouter(prefix="/api/question")


@router.get("/", response_model=QuestionList)
def read_questions_list(
    search_str: str = "",
    page: int = 0,
    size: int = 20,
    order_by: str = "created_at",
    ascending: bool = False,
    db: Session = Depends(get_db)
):
    """
    문제 목록
    """
    total, questions = get_questions_exec(
        db,
        search_str=search_str,
        skip=page * size,
        limit=size,
        order_by=order_by,
        ascending=ascending
    )

    result = {
        'total': total,
        'questions': questions
    }
    return result


@router.get("/{question_id}", response_model=Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    """
    문제 상세
    """
    question = get_question_exec(db, question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/", response_model=Question)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    문제 생성
    """
    return create_question_exec(db=db, question=question, user=current_user)


@router.put("/{question_id}", response_model=Question)
def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    문제수정
    """
    question = get_question_exec(db, question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # 현재 사용자가 글의 작성자인지 확인
    if question.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return update_question_exec(db, question=question, question_update=question_update)


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    문제 삭제
    """
    question = get_question_exec(db, question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # 현재 사용자가 글의 작성자인지 확인
    if question.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    delete_question_exec(db, question=question)
    return {"message": "Question deleted"}


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = get_question_exec(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    vote_question_exec(
        db, db_question=db_question, db_user=current_user)
