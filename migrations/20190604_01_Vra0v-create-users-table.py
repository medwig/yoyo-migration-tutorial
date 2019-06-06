"""
Create users table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE users (id INT, name VARCHAR(20), PRIMARY KEY (id))",
         "DROP TABLE users"),
]
