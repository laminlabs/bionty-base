from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import create_model as pydantic_create_model
from pydantic.fields import ModelField


class BaseModel(PydanticBaseModel):
    @classmethod
    def add_fields(cls, **field_definitions: Any):
        """Dynamically adding fields inplace.

        From: https://github.com/samuelcolvin/pydantic/issues/1937
        """
        new_fields: Dict[str, ModelField] = {}
        new_annotations: Dict[str, Optional[type]] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        "field definitions should either be a tuple of (<type>,"
                        " <default>) or just a default value, unfortunately this means"
                        " tuples as default values are not allowed"
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            if f_annotation:
                new_annotations[f_name] = f_annotation

            new_fields[f_name] = ModelField.infer(
                name=f_name,
                value=f_value,
                annotation=f_annotation,
                class_validators=None,
                config=cls.__config__,
            )

        cls.__fields__.update(new_fields)
        cls.__annotations__.update(new_annotations)


class Entity(BaseModel):
    name: str  # this is the value of the standardized id
    std_id: str  # which field contains the standardized ids


def create_model(__model_name: str, *, __base__=BaseModel, **kwargs):
    return pydantic_create_model(
        __model_name=__model_name, __base__=BaseModel, **kwargs
    )
