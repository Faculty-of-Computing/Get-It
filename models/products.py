from sqlalchemy import Integer, String,Float,DateTime,Boolean,Enum,JSON,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from core.database import db
from datetime import datetime 
from typing import List
from utils.enums import ProductCategory  # Assuming enums.py is in the utils directory

class Products(db.Model):
    __tablename__ = 'Products'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True,nullable=False,autoincrement=True)
    name:Mapped[str] = mapped_column(String(255), nullable= False)
    price:Mapped[float] = mapped_column(Float,nullable=False)
    images:Mapped[List[str]] = mapped_column(JSON, nullable=False)  #NOTE- Assuming images are stored as a comma-separated string
    category:Mapped[ProductCategory] = mapped_column(Enum(ProductCategory), nullable=False)  # Using Enum for category
    description:Mapped[str] = mapped_column(String(500), nullable=True)
    stock:Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sold:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_featured:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at:Mapped[datetime]= mapped_column(DateTime,nullable=False,default=datetime.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime,nullable=False,default=datetime.now(),onupdate=datetime.now)
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    product = relationship('Products', back_populates='reviews')
    
    def __repr__(self):
        return f"<Product {self.name} - {self.category}>"

class Review(db.Model):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('Products.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[str] = mapped_column(db.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user = relationship('User')
    