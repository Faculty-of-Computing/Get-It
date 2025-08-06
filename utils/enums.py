from enum import Enum 

class ProductCategory(str,Enum): # type: ignore
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME_APPLIANCES = "home_appliances"
    BOOKS = "books"
    TOYS = "toys"
    SPORTS = "sports"
    BEAUTY = "beauty"
    AUTOMOTIVE = "automotive"
    GROCERY = "grocery"

class OrderStatus(str,Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class OrderePaymentStatus(str,Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
