from pydantic import BaseModel, Field


class ProductSpec(BaseModel):
    range: str = Field(
        default="нет данных",
        alias="диапазон измерений",
        description="Диапазон измерений, МПа",
    )
    accuracy_class: str = Field(
        default="нет данных", alias="класс точности", description="Класс точности"
    )
    connection_type: str = Field(
        default="нет данных", alias="присоединение", description="Тип присоединения"
    )
    body_diameter: str = Field(
        default="нет данных", alias="диаметр корпуса", description="Диаметр корпуса, мм"
    )
