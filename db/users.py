from db.classes import User, CreateUser
from typing import Any, Optional, Tuple, Sequence, List
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_user(session: Session, create: CreateUser) -> User:
    """
    There is a few way to format this with SQLAlchemy but I suspect anything other than this styling was not allowed
    since they used various shortcuts to generate raw sql.
    """

    """
    Commented code here is unsafe since it is directly inserting values in to the statement. This could allow arbitrary 
    sql commands to be run.
    """
    #statement = f"INSERT INTO users (first_name, last_name) VALUES ({create.first_name}, {create.last_name})"
    #result = session.execute(statement)

    """
    Code here allows the sqlalchemy library to sanitize inputs before executing the command.
    """
    query = "INSERT INTO users (username) VALUES (:username) RETURNING *"
    result = session.execute(text(query).bindparams(username=create.username)).fetchone()
    return _model_to_user(result)

def get_user_by_id(session: Session, id: int) -> Optional[User]:
    query = "SELECT * from users WHERE id = :id"
    result = session.execute(text(query).bindparams(id=id)).fetchone()
    return _model_to_user(result) if result else None

def get_user_by_username(session: Session, name: str) -> Optional[User]:
    query = "SELECT * from users WHERE username = :name"
    result = session.execute(text(query).bindparams(name=name)).fetchone()
    return _model_to_user(result) if result else None

def get_all_users(session: Session) -> Sequence[User]:
    query = "SELECT * from users"
    results = session.execute(text(query)).fetchall()
    return [_model_to_user(x) for x in results]

def get_users_by_ids(session: Session, ids: Sequence[int]) -> Sequence[User]:
    query = "SELECT * from users WHERE id = ANY(:ids)"
    results = session.execute(text(query).bindparams(ids=ids)).fetchall()
    return [_model_to_user(x) for x in results]

def _model_to_user(data: Tuple[Any, ...]) -> User:
    """
    Converts a single row of DB data into a python object. While this function is a little cleaner when using ORM objects; it
    works the same with raw sql data. Using this method I get nice clean objects out of the database layer without dealing with
    hashes/dicts or ORM objects outside of the database layer.
    """
    return User(
        id=data[0],
        username=data[1],
    )
