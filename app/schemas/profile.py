from enum import StrEnum

from pydantic import BaseModel


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class AgeGroup(StrEnum):
    CHILD = "child"
    TEENAGER = "teenager"
    ADULT = "adult"
    SENIOR = "senior"

class SortEnum(StrEnum):
    AGE = "age"
    CREATED_AT = "created_at"
    GENDER_PROBABILITY = "gender_probability"

class OrderByEnum(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"

class ProfileCreate(BaseModel):
    name: str
    gender: Gender
    gender_probability: float
    age: int
    age_group: AgeGroup
    country_id: str
    country_name: str
    country_probability: float

class ProfileUpdate(BaseModel):
    name: str | None = None
    gender: Gender | None = None
    gender_probability: float | None = None
    age: int | None = None
    age_group: AgeGroup | None = None
    country_id: str | None = None
    country_name: str | None = None
    country_probability: float | None = None

class FilterParams(BaseModel):
    gender: list[Gender] | None = None
    age_group: list[AgeGroup] | None = None
    country_id: str | None = None
    min_age: int | None = None
    max_age: int | None = None
    min_gender_probability: float | None = None
    min_country_probability: float | None = None

class SortParams(BaseModel):
    sort_by: SortEnum | None = None
    order_by: OrderByEnum = OrderByEnum.ASCENDING

class PaginationParams:
    def __init__(self, page: int = 1, limit: int = 100):
        self.page = max(page, 1)
        self.limit = min(limit, 100)

    @property
    def offset(self):
        return (self.page - 1) * self.limit