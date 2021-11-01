# DEV Steps

- docker-compose up db
- poetry install
- Migrate DB to the latest `alembic upgrade head`

### To Create A New Migration
- ``alembic revision -m "create account table"`` 

## Trouble Shooting
- Delete the db `docker-compose rm`
