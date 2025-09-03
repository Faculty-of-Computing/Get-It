import bcrypt
from sqlalchemy import Integer, String,DateTime,Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship,validates
from core.database import db 
from datetime import datetime
from flask_login import UserMixin
from core.configs import bycrypt
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

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
    is_seller: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    seller_application_status: Mapped[str] = mapped_column(String(20), default='none', nullable=False)  # none, pending, approved, denied
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_image: Mapped[str] = mapped_column(String(255), nullable=True)
    cart: Mapped['Cart'] = relationship("Cart", back_populates="user", uselist=False,lazy='selectin') # type: ignore

    cart_items:Mapped[list['CartItem']] = relationship("CartItem", back_populates="user", cascade="all, delete-orphan",lazy='selectin') # type: ignore
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan",lazy='selectin')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @validates('password')
    def hash_password(self, key, value:str):
        if value and not value.startswith('$2b$'):
            return bycrypt.generate_password_hash(value).decode('utf-8')
        return value


