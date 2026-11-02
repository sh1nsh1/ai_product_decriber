from .base_schema import BaseSchema


class ProductAIDescription(BaseSchema):
    seo_title: str
    seo_description: str
    characteristics: list[dict[str, str]]
    keywords: list[str]
    commercial_block: str
