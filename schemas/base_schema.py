from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel, serialization_alias=to_snake
        ),
        validate_by_name=True,
        from_attributes=True,
    )
