from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


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
    def get_all_profiles(db: Session) -> list[Profile]:
        return db.query(Profile).all()
    
    @staticmethod
    def update_profile(db: Session, profile_id: UUID, profile: ProfileUpdate) -> Profile | None:

        existing_profile = db.query(Profile).filter(Profile.id == profile_id).first()

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