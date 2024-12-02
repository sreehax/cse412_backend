import os

class Config:
    user = os.getenv('USER')
    user = 'postgres' if user == 'root' else user
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://{user}@localhost:5432/cse412')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
