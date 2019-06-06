A guide walking through creating a Postgres database and examples of using Yoyo migrations to create, update, and rollback tables.

**Install dependencies:**

`$ pip install -r requirements.txt`

## Create Postgres Database
#### Install Postgres:

`$ sudo apt-get update`

`$ sudo apt-get install postgresql`

#### Create test database and set password:

`$ sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"`

`$ sudo -u postgres psql -c "CREATE DATABASE testdb;"`

#### Start postgres server and connect to it:

`$ sudo service postgresql start`

#### Setup connection config:
```
$ echo "[local]\n\ 
host=127.0.0.1\n\ 
user=postgres\n\ 
dbname=testdb\n\ 
password=postgres\n\ 
port=5432" >> ~/.pg_service.conf
```

#### Connect to Postgres local server:

`$ psql service=local`

#### Confirm database is empty:
```
$ testdb=# \d

Did not find any relations.
```


## Migration 1: Create Table
#### Make the create-table migration script with yoyo:

`$ yoyo new ./migrations -m "CREATE TABLE users (id INT, name VARCHAR(20), PRIMARY KEY (id)"`

```
# migrations/20190604_01_Vra0v-create-users-table.py

"""
Create users table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE users (id INT, name VARCHAR(20), PRIMARY KEY (id))")
]

```
```
Created file ./migrations/20190604_01_BnWl8-create-table-users-id-int-name-varchar-20-primary-key-id.py
Save migration configuration to yoyo.ini?
This is saved in plain text and contains your database password.

Answering 'y' means you do not have to specify the migration source or database connection for future runs [yn]: y
```

#### Apply migration:

`$ yoyo apply --database postgresql://postgres:postgres@localhost/testdb ./migrations`

#### Confirm table creation:

`$ psql service=local` 

`$ testdb=# \d`

```
              List of relations
 Schema |      Name       | Type  |  Owner   
--------+-----------------+-------+----------
 public | _yoyo_log       | table | postgres
 public | _yoyo_migration | table | postgres
 public | _yoyo_version   | table | postgres
 public | users           | table | postgres
 public | yoyo_lock       | table | postgres
(5 rows)

testdb=# select * from users;
 id | name 
----+------
(0 rows)
 
```

## Migration 2: Add Column to Table
#### Create migration file for new column:

`$ yoyo new ./migrations -m "Add age column to users table"`

```
# migrations/20190604_02_ORgoL-add-age-column-to-users-table.py

"""
Add age column to users table
"""

from yoyo import step

__depends__ = {'20190604_01_Vra0v-create-users-table'}

steps = [
    step("ALTER TABLE users ADD COLUMN age INT")
]
```

#### Apply migration:

`$ yoyo apply --database postgresql://postgres:postgres@localhost/testdb ./migrations`

Confirm migration worked:

```
$ testdb=# \d+ users
                                          Table "public.users"
 Column |         Type          | Collation | Nullable | Default | Storage  | Stats target | Description 
--------+-----------------------+-----------+----------+---------+----------+--------------+-------------
 id     | integer               |           | not null |         | plain    |              | 
 name   | character varying(20) |           |          |         | extended |              | 
 age    | integer               |           |          |         | plain    |              | 
```

## Migration 3: Rollback
To roll back migrations, the rollback step must be defined explicitly.

Edit the two migration scripts to add a rollback command to each step.

```
# migrations/20190604_01_Vra0v-create-users-table.py

"""
Create users table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE users (id INT, name VARCHAR(20), PRIMARY KEY (id))",
         "DROP TABLE users"),  # rollback command
]
```

```
# migrations/20190604_02_ORgoL-add-age-column-to-users-table.py 

"""
Add age column to users table
"""

from yoyo import step

__depends__ = {'20190604_01_Vra0v-create-users-table'}

steps = [
    step("ALTER TABLE users ADD COLUMN age INT",
         "ALTER TABLE users DROP COLUMN age"),  # rollback command
]       
```

#### Run rollback of the add column step:

`$ yoyo rollback --database postgresql://postgres:postgres@localhost/testdb ./migrations`

```
[20190604_02_ORgoL-add-age-column-to-users-table]
Shall I rollback this migration? [Ynvdaqjk?]: Y

[20190604_01_Vra0v-create-users-table]
Shall I rollback this migration? [Ynvdaqjk?]: n

Selected 1 migration:
  [20190604_02_ORgoL-add-age-column-to-users-table]
Rollback this migration to postgresql://postgres:postgres@localhost/testdb [Yn]: Y
```

#### Confirm that the column has been removed:
`$ testdb=# \d+ users;`

```
                                          Table "public.users"
 Column |         Type          | Collation | Nullable | Default | Storage  | Stats target | Description 
--------+-----------------------+-----------+----------+---------+----------+--------------+-------------
 id     | integer               |           | not null |         | plain    |              | 
 name   | character varying(20) |           |          |         | extended |              | 
```

You can also check the `_yoyo_migration` table to confirm which migrations have been applied to the database:

`testdb=# select * from _yoyo_migration;`

```
                          migration_hash                          |             migration_id             |       applied_at_utc       
------------------------------------------------------------------+--------------------------------------+----------------------------
 fe8fc11fadfb920b12a7f3eb691a376c7b4453321a48f409987e5b5db5eaca44 | 20190604_01_Vra0v-create-users-table | 2019-06-06 16:33:01.881926
(1 row)
```

#### Rollback a specific migation:

`yoyo rollback --database postgresql://postgres:postgres@localhost/testdb ./migrations -r 20190604_01_Vra0v-create-users-table`

If the specified migration has dependent downstream migrations yoyo is smart enough to rollback those as well:

```
Selected 2 migrations:
  [20190604_02_ORgoL-add-age-column-to-users-table]
  [20190604_01_Vra0v-create-users-table]
Rollback these 2 migrations to postgresql://postgres:postgres@localhost/testdb [Yn]: Y
```

To avoid the confirmation prompts just add the `--batch` flag to any command and it will auto-approve.

That's about it!
