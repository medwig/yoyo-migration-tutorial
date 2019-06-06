from yoyo import read_migrations, get_backend

backend = get_backend('postgres://postgres:postgres@localhost/testdb')
migrations = read_migrations('./migrations')
backend.rollback_one(migrations[-1])

