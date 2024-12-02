import os

class Config:
    user = os.getenv('USER')
    host = os.getenv('HOSTNAME')
    user = 'postgres' if (user == 'root' or host == 'lux') else user
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://{user}@localhost:5432/cse412')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
