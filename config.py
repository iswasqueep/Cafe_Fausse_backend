import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:admin@localhost/cafe_fausse_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
