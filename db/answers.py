from db.classes import User, CreateUser, CreateQuestionAnswer, QuestionAnswer
from typing import Any, Optional, Tuple, Sequence, List
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_question_answer(session: Session, create: CreateQuestionAnswer) -> QuestionAnswer:
    query = "INSERT INTO question_answers (question_id, owner_id, body) VALUES (:question_id, :owner_id, :body) RETURNING *"
    result = session.execute(text(query).bindparams(question_id=create.question_id, owner_id=create.owner_id, body=create.body)).fetchone()
    return _model_to_answer(result)

def get_answers_by_question_id(session: Session, question_id: int) -> Sequence[QuestionAnswer]:
    query = "SELECT * from question_answers WHERE question_id= :question_id"
    results = session.execute(text(query).bindparams(question_id=question_id)).fetchall()
    return [_model_to_answer(x) for x in results]

def get_answers_by_question_ids(session: Session, question_ids: List[int]) -> Sequence[QuestionAnswer]:
    query = "SELECT * from question_answers WHERE question_id = ANY(:question_ids)"
    results = session.execute(text(query).bindparams(question_ids=question_ids)).fetchall()
    return [_model_to_answer(x) for x in results]

def get_answer_counts_grouped_by_owner_id(session: Session) -> List[Tuple[int, int]]:
    query = "SELECT owner_id, COUNT(*) from question_answers JOIN users u on u.id = question_answers.owner_id GROUP BY owner_id HAVING COUNT(*) > 0"
    results = session.execute(text(query)).fetchall()
    return results

def _model_to_answer(data: Tuple[Any, ...]) -> QuestionAnswer:
    return QuestionAnswer(
        id=data[0],
        question_id=data[1],
        owner_id=data[2],
        body=data[3],
    )

