import os

class Config:
    #user = os.getenv('USER')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://postgres@localhost:5432/cse412')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
