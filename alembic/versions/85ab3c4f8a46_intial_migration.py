"""intial_migration

Revision ID: 85ab3c4f8a46
Revises: 5715bfb693ca
Create Date: 2021-10-30 10:24:09.739463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

"""
Note:
Alembic migrations are normally used in conjunction with the sqlachemy ORM functions. However, there is nothing
stopping us from using them with raw SQL commands instead since we're not using sqlachemys ORM functions. Using alembic gives us
the benefit a real migration system which might be overkill for this project.
- L
"""

# revision identifiers, used by Alembic.
revision = '85ab3c4f8a46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    bind = op.get_bind()
    session = Session(bind=bind)

    # Initial tables
    ## Serial is a macro for `INT NOT NULL DEFAULT nextval('some_table_name_seq')`
    session.execute("CREATE TABLE users ( id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE )")
    session.execute("CREATE TABLE questions (id SERIAL PRIMARY KEY, owner_id INT, title VARCHAR(255), body TEXT)")
    session.execute("CREATE TABLE question_answers (id SERIAL PRIMARY KEY, question_id INT, owner_id INT, body TEXT)")

    # Initial views

    # Add constraints
    ## I think it's cleaner to do this after table creation, also then you don't need to worry about table creation order.
    session.execute("ALTER TABLE questions ADD CONSTRAINT fk_questions_owner FOREIGN KEY (owner_id) REFERENCES users (id)")

    session.execute("ALTER TABLE question_answers ADD CONSTRAINT fk_question_answers_owner FOREIGN KEY (owner_id) REFERENCES users (id)")
    session.execute("ALTER TABLE question_answers ADD CONSTRAINT fk_question_answers_question FOREIGN KEY (question_id) REFERENCES questions (id)")

    #session.execute("ALTER TABLE projects ADD CONSTRAINT fk_projects_people FOREIGN KEY (owner_id) REFERENCES users (id)")

    # Indexes
    ## On a more permanent project you would want to come back and add some indexes.





def downgrade():
    # No downgrade on initial migration, just delete the db.
    pass
