from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Haetaan tietokanta-URI ympäristömuuttujasta
database_url = getenv("DATABASE_URL")

# Luodaan SQLAlchemy-yhteys
engine = create_engine(database_url)

# Määritellään tietokantamalli (malli)
Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)
    owner_name = Column(String(255), nullable=False)
    notes = Column(Text)
    start_date = Column(Date)
    start_stage = Column(Integer)
    end_stage = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

# Luo taulut tietokantaan
Base.metadata.create_all(engine)
