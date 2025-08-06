from typing import Any, Sequence
from core.database import db
from models.cart import Cart,CartItem

def get_cart() -> Sequence[Cart]:
    return db.session.execute(db.select(Cart)).scalars().all()