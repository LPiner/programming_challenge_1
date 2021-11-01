from typing import List

from db.classes import CreateUser, CreateQuestion, CreateQuestionAnswer
from validation.util import contains_html


def validate_create_answer(create: CreateQuestionAnswer) -> List[str]:

    errors = []

    if not create.body or len(create.body) > 2000 or len(create.body) < 10:
        errors.append("Body must be between 10-2000 characters long.")

    if create.body and contains_html(create.body):
        errors.append("Body cannot contain HTML.")

    return errors
