from sqlalchemy import Integer, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from core.database import db
from datetime import datetime 
from typing import List

class Cart(db.Model):
    __tablename__= 'Cart'
    id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,unique=True,index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    user = relationship('User', back_populates='cart',lazy='selectin')
    items:Mapped[List['CartItem']] = relationship('CartItem', backref='Cart', cascade="all, delete-orphan",lazy='selectin')

class CartItem(db.Model):
    __tablename__ = "CartItem"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id:Mapped[int] = mapped_column(Integer, ForeignKey('Cart.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'), nullable=False)
    product_id:Mapped[int] = mapped_column(Integer, ForeignKey('Products.id'), nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=1)

    product: Mapped['Products'] = relationship("Products", back_populates="cart_items", lazy='selectin') # type: ignore

    user:Mapped['User'] = relationship(back_populates='cart_items') # type: ignore
