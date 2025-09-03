from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import db
from datetime import datetime

class Wishlist(db.Model):
    __tablename__ = 'Wishlist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('Products.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    user = relationship('User', back_populates='wishlist_items')
    product = relationship('Products', back_populates='wishlist_entries')

from models.products import Products
Products.wishlist_entries = relationship('Wishlist', back_populates='product', cascade="all, delete-orphan")