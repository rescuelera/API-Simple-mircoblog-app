from pydantic import StrictBool, StrictInt, StrictStr

from data.response_models.common_models import StrictBaseModel


class User(StrictBaseModel):

    name: StrictStr
    email: StrictStr
    is_admin: StrictBool
    id: StrictInt
    is_active: StrictBool
