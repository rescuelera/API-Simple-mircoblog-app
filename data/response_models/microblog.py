from datetime import datetime

from pydantic import StrictInt, StrictStr

from data.response_models.common_models import StrictBaseModel


class Microblog(StrictBaseModel):

    title: StrictStr
    text: StrictStr
    owner: StrictInt
    id: StrictInt
    date: datetime
