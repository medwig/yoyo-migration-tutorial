from yoyo import read_migrations, get_backend

backend = get_backend('postgres://postgres:postgres@localhost/testdb')
migrations = read_migrations('./migrations')
sorted_migrations = sorted(migrations, key=lambda x: x.id, reverse=True)
print(sorted_migrations)
backend.rollback_migrations(sorted_migrations)

