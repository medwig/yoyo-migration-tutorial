from yoyo import read_migrations, get_backend, descendants

backend = get_backend('postgres://postgres:postgres@localhost/testdb')
migrations = read_migrations('./migrations')

revision = '20190604_01_Vra0v-create-users-table'
revision = '20190604_02_ORgoL-add-age-column-to-users-table'

targets = [m for m in migrations if revision in m.id]
if len(targets) == 0:
    raise InvalidArgument("'{}' doesn't match any revisions."
                          .format(args.revision))
if len(targets) > 1:
    raise InvalidArgument("'{}' matches multiple revisions. "
                          "Please specify one of {}.".format(
                              args.revision,
                              ', '.join(m.id for m in targets)))
target = targets[0]

deps = descendants(target, migrations)
target_plus_deps = deps | {target}
migrations = migrations.filter(lambda m: m in target_plus_deps)
sorted_migrations = sorted(migrations, key=lambda x: x.id, reverse=True)

print(sorted_migrations)

backend.rollback_migrations(sorted_migrations)

