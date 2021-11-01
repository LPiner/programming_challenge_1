from itertools import chain
from typing import List

from flask import Flask, request, flash, render_template, redirect, session, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_app_config
from db.answers import get_answers_by_question_id, create_question_answer, get_answers_by_question_ids, \
    get_answer_counts_grouped_by_owner_id
from db.classes import CreateUser, CreateQuestion, CreateQuestionAnswer
from db.questions import create_question, get_question_by_id, get_all_questions, get_question_counts_grouped_by_owner_id
from db.users import create_user, get_all_users, get_users_by_ids, get_user_by_username
from validation.answer import validate_create_answer
from validation.question import validate_create_question
from validation.user import validate_create_user

app = Flask(__name__)
app.secret_key = "=)"
config = get_app_config("development")

engine = create_engine(f'postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@localhost/{config.DB}')
db_session = sessionmaker(bind=engine, autocommit=True)


def flash_multiple(messages: List[str], level: str) -> None:
    for m in messages:
        flash(m, level)


@app.route("/submit_question", methods=('GET', 'POST'))
def submit_question():
    if not session.get("current_user"):
        flash(f"You must sign in or register to ask questions.", "info")
        return redirect(url_for("index"))

    if request.method == 'POST':
        # This is where validation would go.
        # username = request.form['username']
        create = CreateQuestion(
            owner_id=session["current_user"]["id"],
            title=request.form["title"],
            body=request.form["body"],
        )
        errors = validate_create_question(create)
        if errors:
            flash_multiple(errors, "warning")
            return render_template('submit_question.html')

            # The line below starts a transaction with the DB that ends when the block ends.
        with db_session.begin() as db:
            question = create_question(db, create)
        return redirect(url_for("question", id=question.id))

        flash(error)
    return render_template('submit_question.html')


@app.route("/question/<id>/answer", methods=('GET', 'POST'))
def submit_answer(id: int):
    if not session.get("current_user"):
        flash(f"You must sign in or register to answer questions.", "info")
        return redirect(url_for("index"))

    with db_session.begin() as db:
        question = get_question_by_id(db, id)

    if not question:
        flash(f"Question with id {id} was not found.")
        return redirect(url_for("index"))

    if request.method == 'POST':
        create = CreateQuestionAnswer(
            owner_id=session["current_user"]["id"],
            question_id=question.id,
            body=request.form["body"], )
        errors = validate_create_answer(create)
        if errors:
            flash_multiple(errors, "warning")
            return render_template('submit_answer.html')

        # This is where validation would go.
        # username = request.form['username']
        error = None

        if error is None:
            # The line below starts a transaction with the DB that ends when the block ends.
            with db_session.begin() as db:
                create_question_answer(db, create)
            flash("Answer Submitted!")
            return redirect(url_for("question", id=question.id))

        flash(error)
    return render_template('submit_answer.html')


@app.route("/question/<id>")
def question(id: int):
    if not session.get("current_user"):
        flash(f"You must sign in or register to view questions.", "info")
        return redirect(url_for("index"))
    with db_session.begin() as db:
        question = get_question_by_id(db, id)
        answers = get_answers_by_question_id(db, question_id=id)
        users = {x.id: x for x in get_users_by_ids(db, list({x.owner_id for x in answers}))}
    if not question:
        flash(f"Question with id {id} was not found.")
        return redirect(url_for("index"))

    return render_template('question.html', question=question, answers=answers, users=users)


@app.route("/create_user", methods=('GET', 'POST'))
def user():
    if session.get("current_user"):
        flash(f"You are already signed in.", "info")
        return redirect(url_for("index"))
    if request.method == 'POST':
        create = CreateUser(username=request.form["username"])
        errors = validate_create_user(create)
        with db_session.begin() as db:
            existing_user = get_user_by_username(db, create.username)
        if existing_user:
            errors.append("This username is already in use.")
        if errors:
            flash_multiple(errors, "warning")
            return render_template('create_user.html')

        with db_session.begin() as db:
            user = create_user(db, create)

        session["current_user"] = {"username": user.username, "id": user.id}

        return redirect(url_for("index"))

    return render_template('create_user.html')


@app.route("/login", methods=('GET', 'POST'))
def login():
    if session.get("current_user"):
        flash(f"You are already signed in!", "info")
        return redirect(url_for("index"))

    if request.method == 'POST':
        # This is where validation would go.
        # username = request.form['username']
        error = None

        if error is None:
            # The line below starts a transaction with the DB that ends when the block ends.
            with db_session.begin() as db:
                user = get_user_by_username(db, request.form['username'])
            if not user:
                flash(f"User with name {request.form['username']} was not found.", "warning")
                return redirect(url_for("login"))
            session["current_user"] = {"username": user.username, "id": user.id}
            flash(f"Thank you for signing in!", "info")
            return redirect(url_for("index"))

        flash(error)

    return render_template('login.html')


@app.route("/logout", methods=('GET',))
def logout():
    if session.get('current_user'):
        del session["current_user"]
        flash("You have been signed out.", "info")
    return redirect(url_for("index"))


@app.route("/users", methods=('GET',))
def users():
    with db_session.begin() as session:
        users = get_all_users(session)

    return render_template('users.html', users=users)


@app.route("/", methods=('GET',))
def index():
    if not session.get("current_user"):
        return redirect(url_for("stats"))

    with db_session.begin() as db:
        questions = get_all_questions(db)
        answers = get_answers_by_question_ids(db, [x.id for x in questions])
        counts = {x.id: len([y for y in answers if y.question_id == x.id]) for x in questions}
    questions = sorted(questions, key=lambda x: counts[x.id], reverse=True)

    return render_template('questions.html', questions=questions, counts=counts)


@app.route("/stats", methods=('GET',))
def stats():
    with db_session.begin() as session:
        question_counts_by_user = get_question_counts_grouped_by_owner_id(session)
        answer_counts_by_user = get_answer_counts_grouped_by_owner_id(session)
        users = get_users_by_ids(session,
                                 list(set(chain(
                                     [x[0] for x in question_counts_by_user],
                                     [x[0] for x in answer_counts_by_user],
                                 )))

                                 )
        users = {x.id: x for x in users}

    return render_template('stats.html',
                           users=users,
                           answer_counts_by_user=sorted(answer_counts_by_user, key=lambda x: x[1], reverse=True),
                           question_counts_by_user=sorted(question_counts_by_user, key=lambda x: x[1], reverse=True),
                           )
