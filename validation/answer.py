from typing import List

from db.classes import CreateUser, CreateQuestion, CreateQuestionAnswer


def validate_create_answer(create: CreateQuestionAnswer) -> List[str]:

    errors = []

    if not create.body or len(create.body) > 2000 or len(create.body) < 10:
        errors.append("Body must be between 10-2000 characters long.")

    return errors
