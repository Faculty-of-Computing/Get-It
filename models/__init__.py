from .order import Order
from .products import Products,Review
from .users import User
from .wishlist import Wishlist
from sqlalchemy.orm import relationship

User.wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan", lazy='selectin') # type: ignore
Products.wishlist_entries = relationship('Wishlist', back_populates='product', cascade="all, delete-orphan") # type: ignore


__all__ = [
	"Order",
	"Products",
	"Review",
	"User",
	"Wishlist",
]
