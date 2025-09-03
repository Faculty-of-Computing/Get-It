import bcrypt
from sqlalchemy import Integer, String,DateTime,Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship,validates
from core.database import db 
from datetime import datetime
from flask_login import UserMixin
from core.configs import bycrypt

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    email:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    cart: Mapped['Cart'] = relationship("Cart", back_populates="user", uselist=False,lazy='selectin') # type: ignore

    cart_items:Mapped[list['CartItem']] = relationship("CartItem", back_populates="user", cascade="all, delete-orphan",lazy='selectin') # type: ignore
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan",lazy='selectin')
    

    
    @validates('password')
    def hash_password(self, key, value:str):
        if value and not value.startswith('$2b$'):
            return bycrypt.generate_password_hash(value).decode('utf-8')
        return value


    