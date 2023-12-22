# from sqlmodel import create_engine

# from app.core.config import settings

# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/")
db = mongo.myapp
