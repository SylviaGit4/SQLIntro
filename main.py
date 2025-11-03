import sqlite3
from faker import Faker
fake = Faker()

Faker.seed(0)

# Connect to the database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create tables
#c.execute('''CREATE TABLE Authors (
#                id INTEGER PRIMARY KEY,
#                name TEXT
#             )''')

#c.execute('''CREATE TABLE Books (
#                id INTEGER PRIMARY KEY,
#                title TEXT,
#                author_id INTEGER,
#                FOREIGN KEY(author_id) REFERENCES Authors(id)
#             )''')

# Insert FAKE data
#for i in range (101):
#    name = fake.name()
#    title = fake.bs()
#    c.execute(f"INSERT INTO Authors (name) VALUES ('{name}')")
#    c.execute(f"INSERT INTO Books (title, author_id) VALUES ('{title}', {i})")


# Insert data
#c.execute("INSERT INTO Authors (name) VALUES ('George Orwell')")
#c.execute("INSERT INTO Books (title, author_id) VALUES ('1984', 1)")
#c.execute("INSERT INTO Books (title, author_id) VALUES ('Animal Farm', 1)")



conn.commit()
conn.close()
