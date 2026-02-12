from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from enum import Enum
class role(str , Enum):
    user = "user"
    admin = "admin"
class User(Base):
    __tablename__ = "task_user"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True)
    hash_password = Column(String, nullable=False)
    student = Column(Boolean, default=False)
    role = Column(String , default=role.user.value)
    
class Task(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    owner_id = Column(Integer, ForeignKey("task_user.user_id"))
 
  
