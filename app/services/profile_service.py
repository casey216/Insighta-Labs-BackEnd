from typing import Any
from uuid import UUID

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError

from app.models.profile import Profile
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, 
    Gender, AgeGroup, SortParams,
    FilterParams, PaginationParams
)


class ProfileService:
    """Service layer for Profile business logic"""

    @staticmethod
    def create_profile(db: Session, profile: ProfileCreate) -> Profile:
        new_profile = Profile(**profile.model_dump())

        try:
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return new_profile
        except IntegrityError:
            db.rollback()
            raise

    @staticmethod
    def get_profile_by_id(db: Session, profile_id: UUID) -> Profile | None:
        return db.query(Profile).filter(Profile.id == profile_id).first()
    
    @staticmethod
    def get_profile_by_name(db: Session, name: str) -> Profile | None:
        return db.query(Profile).filter(Profile.name == name).first()
    
    @staticmethod
    def get_all_profiles(
        filter_params: FilterParams,
        sort_params: SortParams,
        p: PaginationParams,
        db: Session
        ) -> dict[str, Any]:
        q = db.query(Profile)
        q = ProfileQueryBuilder(q)
        q = q.filter_age(filter_params.min_age, filter_params.max_age)
        q = q.filter_age_group(filter_params.age_group)
        q = q.filter_country_id(filter_params.country_id)
        q = q.filter_country_probability(filter_params.min_country_probability)
        q = q.filter_gender(filter_params.gender)
        q = q.filter_gender_probability(filter_params.min_gender_probability)
        q = q.sort_by(sort_params)
        q = q.build()

        total = q.count()
        profiles = q.offset(p.offset).limit(p.limit).all()

        return {
            "total": total,
            "data": profiles
        }
        
    
    @staticmethod
    def update_profile(db: Session, profile_id: UUID, profile: ProfileUpdate) -> Profile | None:

        existing_profile = ProfileService.get_profile_by_id(db, profile_id)

        if not existing_profile:
            return None
        
        new_profile = profile.model_dump(exclude_unset=True)

        for key, value in new_profile.items():
            setattr(existing_profile, key, value)

        db.commit()
        db.refresh(existing_profile)

        return existing_profile
    
    @staticmethod
    def delete_profile(db: Session, profile_id: UUID) -> bool:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()

        if not profile:
            return False

        db.delete(profile)
        db.commit()

        return True
    

class ProfileQueryBuilder:
    """Query buider for Profile service"""
    def __init__(self, query: Query[Profile]):
        self.query = query
        self.sort_column = None

    def filter_gender(self, genders: list[Gender] | None):
        if genders:
            self.query = self.query.filter(Profile.gender.in_(genders))
        return self

    def filter_age(self, min_age: int | None, max_age: int | None):
        if min_age:
            self.query = self.query.filter(Profile.age >= min_age)
        if max_age:
            self.query = self.query.filter(Profile.age <= max_age)
        return self
    
    def filter_age_group(self, age_groups: list[AgeGroup] | None):
        if age_groups:
            self.query = self.query.filter(Profile.age_group.in_(age_groups))
        return self

    def filter_country_id(self, country_id: str | None):
        if country_id:
            self.query = self.query.filter(Profile.country_id == country_id.upper())
        return self

    def filter_country_probability(self, min_country_p: float | None):
        if min_country_p:
            self.query = self.query.filter(Profile.country_probability == min_country_p)
        return self
    
    def filter_gender_probability(self, min_gender_p: float | None):
        if min_gender_p:
            self.query = self.query.filter(Profile.country_probability == min_gender_p)
        return self
    
    def sort_by(self, sort_params: SortParams):
        if sort_params.sort_by:
            value = sort_params.sort_by.value
            if value == "age":
                self.sort_column = Profile.age
            if value == "created_at":
                self.sort_column = Profile.created_at
            if value == "gender_probability":
                self.sort_column = Profile.gender_probability

        if self.sort_column:
            if sort_params.order_by == "asc":
                self.query = self.query.order_by(asc(self.sort_column))
            else:
                self.query = self.query.order_by(desc(self.sort_column))
        return self

    def build(self):
        return self.query