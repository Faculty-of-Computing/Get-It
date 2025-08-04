from enums import Enum 

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