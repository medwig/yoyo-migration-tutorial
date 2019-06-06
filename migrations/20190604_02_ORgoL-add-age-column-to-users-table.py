"""
Add age column to users table
"""

from yoyo import step

__depends__ = {'20190604_01_Vra0v-create-users-table'}

steps = [
    step("ALTER TABLE users ADD COLUMN age INT",
         "ALTER TABLE users DROP COLUMN age"),
]
