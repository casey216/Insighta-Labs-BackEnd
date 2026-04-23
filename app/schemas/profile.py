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
    name: str
    gender: Gender
    gender_probability: float
    age: int
    age_group: AgeGroup
    country_id: str
    country_name: str
    country_probability: float