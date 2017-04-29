from api.database import DAL
from api.database.db import db

def init():
    DAL.open(db)