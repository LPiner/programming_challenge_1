from typing import List

from db.classes import CreateUser


def validate_create_user(create: CreateUser) -> List[str]:
    errors = []
    if not create.username or len(create.username) > 20 or len(create.username) < 4:
        errors.append("Username must be between 4-20 characters long.")

    if create.username:
        if not create.username.isalnum():
            errors.append("Username can only contain characters a-z, numbers 0-9.")
    return errors
