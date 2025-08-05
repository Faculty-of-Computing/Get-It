from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Float, Text, DateTime, func,Enum
from core.database import db
from utils.enums import OrderStatus

class Order(db.Model):
    __tablename__ = "Orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)

    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    shipping_address: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    phone: Mapped[str] = mapped_column(String(20), nullable=False)


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("Orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("Products.id"), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)  # price at time of order

    order = relationship("Order", back_populates="items")
    product = relationship("Products")
