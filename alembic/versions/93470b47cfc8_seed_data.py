"""empty message

Revision ID: 93470b47cfc8
Revises: 85ab3c4f8a46
Create Date: 2021-11-01 14:50:10.671401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = '93470b47cfc8'
down_revision = '85ab3c4f8a46'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Seed data
    session.execute("INSERT INTO users (username) VALUES ('admin')")
    session.execute("INSERT INTO users (username) VALUES ('notaspambot')")
    session.execute("INSERT INTO users (username) VALUES ('johnm')")
    session.execute("INSERT INTO users (username) VALUES ('mattq')")

    session.execute("INSERT INTO questions (owner_id, title, body) VALUES (1, 'Anyone here?', 'Guys common I spent like 4 hours on this.')")
    session.execute("INSERT INTO questions (owner_id, title, body) VALUES (2, 'Free money!', 'Visit my website www.notascam.com ')")
    session.execute("INSERT INTO questions (owner_id, title, body) VALUES (3, 'Lost Cat!@#', 'Last my cat while walking her last night, has anyone seen her?')")
    session.execute("INSERT INTO questions (owner_id, title, body) VALUES (3, 'Soccer Anyone?', 'After you guys find my cat does anyone want to play some soccer at the part?')")
    session.execute("INSERT INTO questions (owner_id, title, body) VALUES (4, 'Wheres the coffee maker gone?', 'Has anyone seen the coffee maker? Its missing from the break room')")

    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (1, 5, 'HR took it out to clean it, should be back next week.')")

    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (2, 5, 'Free money @ www.notascam.com ')")
    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (2, 5, 'Free money @ www.notascam.com ')")
    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (2, 5, 'Free money @ www.notascam.com ')")
    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (2, 5, 'Free money @ www.notascam.com ')")

    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (1, 4, 'Sure Im down!')")
    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (2, 4, 'Free money @ www.notascam.com ')")
    session.execute("INSERT INTO question_answers (owner_id, question_id, body) VALUES (4, 4, 'Only if theres beer!')")



def downgrade():
    pass
