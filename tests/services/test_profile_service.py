from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.profile import Profile
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, Gender, AgeGroup,
    FilterParams, PaginationParams
)
from app.services.profile_service import ProfileService


def create_sample_profile(n: int = 0) -> ProfileCreate:
    return ProfileCreate(
        name=f"kenechi {n}",
        gender=Gender.MALE,
        gender_probability=0.99,
        age=33,
        age_group=AgeGroup.ADULT,
        country_id="NG",
        country_name="nigeria",
        country_probability=0.99
    )


class TestProfileService:
    """Test class for profile service."""

    def test_create_profile(self, db_session):
        data = create_sample_profile()

        new_profile = ProfileService.create_profile(db_session, data)

        assert new_profile.id is not None
        assert new_profile.name == "kenechi 0"
        assert new_profile.gender == "male"

    def test_fail_to_create_duplicate_profile(self, db_session):
        data = create_sample_profile()

        ProfileService.create_profile(db_session, data)

        with pytest.raises(IntegrityError):
            ProfileService.create_profile(db_session, data)

    def test_get_profile_by_id(self, db_session):
        data = create_sample_profile()
        created = ProfileService.create_profile(db_session, data)

        found = ProfileService.get_profile_by_id(db_session, created.id)

        assert found is not None
        assert found.id == created.id

    def test_get_profile_by_name(self, db_session):
        data = create_sample_profile()
        ProfileService.create_profile(db_session, data)

        found = ProfileService.get_profile_by_name(db_session, "kenechi 0")

        assert found is not None
        assert found.name == "kenechi 0"

    def test_get_all_profiles(self, db_session):
        ProfileService.create_profile(db_session, create_sample_profile())
        ProfileService.create_profile(db_session, create_sample_profile(1))
        filter_params = FilterParams()
        p = PaginationParams()

        result = ProfileService.get_all_profiles(db_session, filter_params, p)

        assert isinstance(result, dict)
        assert "data" in result
        assert "total" in result
        assert isinstance(result.get("data"), list)
        assert result.get("total") == 2

    def test_profile_not_found(self, db_session):
        profile_id = uuid4()

        profile = ProfileService.get_profile_by_id(db_session, profile_id)

        assert profile is None

        profile = ProfileService.get_profile_by_name(db_session, "fake name")
        assert profile is None

    def test_update_profile(self, db_session):
        created = ProfileService.create_profile(
            db_session, create_sample_profile())

        update_data = ProfileUpdate(
            name="updated name",
            age=34,
            gender_probability=0.88
        )

        updated = ProfileService.update_profile(
            db_session, created.id, update_data)

        assert updated is not None
        assert updated.name == "updated name"
        assert updated.age == 34
        assert updated.gender_probability == 0.88

    def test_update_with_unset_values_changes_nothing(self, db_session):
        created = ProfileService.create_profile(
            db_session, create_sample_profile())

        update_data = ProfileUpdate()

        updated = ProfileService.update_profile(
            db_session, created.id, update_data)

        assert updated is not None
        assert updated.name == created.name
        assert updated.age == created.age
        assert updated.gender_probability == created.gender_probability

    def test_delete_profile(self, db_session):
        data = create_sample_profile()
        created = ProfileService.create_profile(db_session, data)

        result = ProfileService.delete_profile(db_session, created.id)

        assert result is True

        deleted = ProfileService.get_profile_by_id(db_session, created.id)
        assert deleted is None

    def test_persistence_after_commit(self, db_session):
        data = create_sample_profile()

        created = ProfileService.create_profile(db_session, data)

        fetched = db_session.query(Profile).filter_by(id=created.id).first()

        assert fetched is not None
