from sqlalchemy import Integer, String,DateTime,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.database import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(Integer,primary_key=True,unique=True,nullable=False,autoincrement=True,index=True)
    first_name:Mapped[str]= mapped_column(String(100),nullable=True)
    last_name:Mapped[str]= mapped_column(String(100),nullable=True,)
    username:Mapped[str] = mapped_column(String(100),nullable=False,unique=True,index=True)
    created_at:Mapped[datetime]= mapped_column(DateTime,nullable=False,default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime,nullable=False,default=datetime.now(),onupdate=datetime.now())
    is_active:Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)
    deleted:Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)
    password:Mapped[str] = mapped_column(String(255), nullable=False)
    
    