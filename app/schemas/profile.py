from enum import StrEnum

from pydantic import BaseModel, Field


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

class ProfileOut(BaseModel):
    id: str
    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: str
    country_id: str
    country_name: str
    country_probability: float
    created_at: str

class AllProfiles(BaseModel):
    status: str
    page: int
    limit: int
    total: int
    data: list[ProfileOut]

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    gender: Gender | None = None
    age_group: AgeGroup | None = None
    country_id: str | None = None
    min_age: int | None = Field(default=None, ge=0)
    max_age: int | None = Field(default=None, ge=0)
    min_gender_probability: float | None = Field(default=None, ge=0.0, le=1.0)
    min_country_probability: float | None = Field(default=None, ge=0.0, le=1.0)

class SortParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    sort_by: SortEnum | None = None
    order: OrderByEnum = OrderByEnum.ASCENDING

class PaginationParams:
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = max(page, 1)
        self.limit = min(limit, 50)

    @property
    def offset(self):
        return (self.page - 1) * self.limit