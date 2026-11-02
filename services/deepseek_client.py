import os
from typing import Annotated

from fastapi import Depends
from openai import AsyncOpenAI

from env_config import get_config
from schemas import Product, ProductAIDescription


class DeepSeekClientService:
    from env_config import Config

    def __init__(self, config: Annotated[Config, Depends(get_config)]) -> None:
        self.client = AsyncOpenAI(
            api_key=config.deepseek_api_key,
            base_url="https://api.deepseek.com",
        )

        self.SYSTEM_PROMT = """Ты — SEO-копирайтер интернет-магазина бытовой техники и приборов.
        Твоя задача — по данным о товаре генерировать SEO-контент для карточки.

        ПРАВИЛА:
        1. Отвечай строго в формате JSON, без markdown-обёрток и без пояснений вне JSON.
        2. Не выдумывай характеристики, которых нет во входных данных.
        3. Пиши на русском языке, естественно, без «воды» и переспама ключей.
        4. Соблюдай лимиты:
           - seo_title: до 70 символов включительно.
           - seo_description: от 800 до 1200 символов.
           - keywords: ровно 3–5 штук.
        5. seo_title должен содержать название товара и главный коммерческий маркер (например, «купить», модель, тип), но без кликбейта.
        6. seo_description — связный текст: что это за прибор, для кого, ключевые преимущества, сценарии использования. Без списков и без повторения заголовка дословно.
        7. characteristics — массив объектов {"name": "...", "value": "..."} только по фактам из входных данных, если написано, что данных нет, так и пиши - выводить характеристики из поля description не нужно.
        8. commercial_block — 2–4 предложения для менеджера: кому подходит прибор и какие задачи решает. Деловой, без маркетинговых штампов.

        СТРУКТУРА ОТВЕТА (строго):
        {
          "seo_title": "string",
          "seo_description": "string",
          "characteristics": {"name": "string", "value": "string"},
          "keywords": ["string"],
          "commercial_block": "string"
        }"""

        self.USER_PROMT_TEMPLATE = """Сгенерируй SEO-контент для товара на основе данных
        в JSON ниже.

        Данные товара:
        {product_json}"""

    async def generate_description(
        self, product: Product
    ) -> ProductAIDescription | None:
        response = await self.client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {
                    "role": "system",
                    "content": self.SYSTEM_PROMT,
                },
                {
                    "role": "user",
                    "content": self.USER_PROMT_TEMPLATE.format(
                        product_json=product.model_dump_json()
                    ),
                },
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )

        json_response = response.choices[0].message.content
        if json_response:
            return ProductAIDescription.model_validate_json(json_response)
        else:
            return None
