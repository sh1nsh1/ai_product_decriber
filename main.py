from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from schemas import Product, ProductAIDescription
from services.deepseek_client import DeepSeekClientService

app = FastAPI()


@app.post(
    "/generate_description",
    response_model=ProductAIDescription,
    description="Сгенерировать описание товара по характеристикам",
)
async def generate_description(
    product: Product,
    llm_service: Annotated[DeepSeekClientService, Depends()],
):
    product_description = await llm_service.generate_description(product)
    if product_description:
        return product_description


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "missing_fields": [
                err.get("loc")[1] for err in exc.errors()
            ],  # детали ошибки
            "body": exc.body,
            "message": "Не достаточно данных",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
