from pathlib import Path

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent / 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False