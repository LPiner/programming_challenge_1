from db.classes import User, CreateUser, CreateQuestion, Question
from typing import Any, Optional, Tuple, Sequence, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_question(session: Session, create: CreateQuestion) -> Question:
    query = "INSERT INTO questions (owner_id, title, body) VALUES (:owner_id, :title, :body) RETURNING *"
    result = session.execute(text(query).bindparams(owner_id=create.owner_id, title=create.title, body=create.body)).fetchone()
    return _model_to_question(result)

def get_question_by_id(session: Session, id: int) -> Optional[Question]:
    query = "SELECT * from questions WHERE id = :id"
    result = session.execute(text(query).bindparams(id=id)).fetchone()
    return _model_to_question(result) if result else None

def get_all_questions(session: Session) -> Sequence[Question]:
    query = "SELECT * from questions"
    results = session.execute(text(query)).fetchall()
    return [_model_to_question(x) for x in results]

def get_questions_by_owner_id(session: Session, owner_id: int) -> Sequence[Question]:
    query = "SELECT * from questions where owner_id = :owner_id"
    results = session.execute(text(query).bindparams(owner_id=owner_id)).fetchall()
    return [_model_to_question(x) for x in results]

def get_question_counts_grouped_by_owner_id(session: Session) -> List[Tuple[int, int]]:
    query = "SELECT owner_id, COUNT(*) from questions JOIN users u on u.id = questions.owner_id GROUP BY owner_id HAVING COUNT(*) > 0"
    results = session.execute(text(query)).fetchall()
    return results

def _model_to_question(data: Tuple[Any, ...]) -> Question:
    return Question(
        id=data[0],
        owner_id=data[1],
        title=data[2],
        body=data[3],
    )
