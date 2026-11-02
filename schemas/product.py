from .base_schema import BaseSchema
from .product_spec import ProductSpec


class Product(BaseSchema):
    name: str
    manufacturer: str
    specs: ProductSpec
    description: str
