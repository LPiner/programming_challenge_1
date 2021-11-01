from typing import List

from db.classes import CreateUser, CreateQuestion
from validation.util import contains_html


def validate_create_question(create: CreateQuestion) -> List[str]:
    errors = []
    if not create.title or len(create.title) > 50 or len(create.title) < 4:
        errors.append("Title must be between 4-50 characters long.")

    if not create.body or len(create.body) > 2000 or len(create.body) < 10:
        errors.append("Body must be between 10-2000 characters long.")

    if create.body and contains_html(create.body):
        errors.append("Body cannot contain HTML.")

    if create.title and contains_html(create.title):
        errors.append("Title cannot contain HTML.")

    return errors
