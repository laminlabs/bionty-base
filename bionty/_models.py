from pydantic import BaseModel


class Entity(BaseModel):
    name: str  # this is the value of the standardized id
    std_id: str  # which field contains the standardized ids
