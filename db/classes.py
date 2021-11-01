from attr import attrs

"""
The @attrs decorator provides a shortcut for python class creation by allowing us to bypass the need to use __init__.
auto_attribs=True saves us from using the long hand version of typing decoration.
frozen=True prevents the class from being modified after creation.

Each class in this file defines a single row of data from its related table. This saves us from passing around hashes/dicts
and allows us to define field types.

"""

@attrs(auto_attribs=True, frozen=True)
class User:
    id: int
    username: str

@attrs(auto_attribs=True, frozen=True)
class CreateUser:
    username: str


@attrs(auto_attribs=True, frozen=True)
class Question:
    id: int
    owner_id: int
    title: str
    body: str

@attrs(auto_attribs=True, frozen=True)
class CreateQuestion:
    owner_id: int
    title: str
    body: str


@attrs(auto_attribs=True, frozen=True)
class QuestionAnswer:
    id: int
    owner_id: int
    question_id: int
    body: str

@attrs(auto_attribs=True, frozen=True)
class CreateQuestionAnswer:
    question_id: int
    owner_id: int
    body: str


