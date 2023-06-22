from pydantic import BaseModel
from datetime import datetime


class MultimediaMetadata(BaseModel):
    id: str
    name: str
    type: str
    size_in_kb: float
    created_at: datetime
    last_changed: datetime
    username: str
    description: str
