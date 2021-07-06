from datetime import datetime

from pydantic import UUID4, BaseModel


class ProgressFilmModel(BaseModel):
    user_id: UUID4
    movie_id: UUID4
    viewing_progress: int
    viewing_date: datetime
