from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

load_dotenv()

# Retrieve the database URI from the environment variable
database_url = getenv("DATABASE_URL")

# Create an SQLAlchemy connection
engine = create_engine(database_url)

# Define the database model
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)
    owner_name = Column(String(50), nullable=False)
    notes = Column(Text)
    start_date = Column(Date)
    start_stage = Column(Integer)
    end_stage = Column(Integer)
    inventory_id = Column(Integer, ForeignKey("inventories.inventory_id"))

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

class Permission(Base):
    __tablename__ = "permissions"
    permission_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    username = Column(String(50), nullable=False)
    project_name = Column(String(255), nullable=False)
    project_owner_name = Column(String(50), nullable=False)
    can_modify = Column(Boolean)

    project = relationship("Project", back_populates="permissions")

class Inventory(Base):
    __tablename__ = "inventories"
    owner_name = Column(String(50), nullable=False, unique=True)
    inventory_id = Column(Integer, primary_key=True)
    inventory_name = Column(String(255), nullable=False)
    notes = Column(Text)

class InventoryUsage(Base):
    __tablename__ = "inventory_usage"
    inventory_usage_id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventories.inventory_id", ondelete="CASCADE"))
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    
    inventory = relationship("Inventory", back_populates="inventory_usage")
    project = relationship("Project", back_populates="inventory_usage")

# Create tables
Base.metadata.create_all(engine)
