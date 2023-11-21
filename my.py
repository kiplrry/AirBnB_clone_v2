#!/usr/bin/python3
from os import environ

pas = environ.get('PASS', 'lol')
db = environ.get('DB', 'no db')

print(pas)
print(db)
