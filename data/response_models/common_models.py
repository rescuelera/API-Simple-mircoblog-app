from pydantic import BaseModel, Extra


class StrictBaseModel(BaseModel):
    """Doesn't allow keys not listed in a model."""

    class Config:
        extra = Extra.forbid