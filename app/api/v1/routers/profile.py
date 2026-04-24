from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.profile import Profile
from app.schemas.profile import FilterParams, SortParams, PaginationParams, AllProfiles, Gender
from app.services.profile_service import ProfileService


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", status_code=200, response_model=AllProfiles)
def read_all_profiles(
    filter_prams: Annotated[FilterParams, Depends()],
    sort_params: Annotated[SortParams, Depends()],
    p: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    result = ProfileService.get_all_profiles(
        filter_prams,
        sort_params,
        p,
        db
    )

    data = result.get("data")

    return {
        "status": "success",
        "page": p.page,
        "limit": p.limit,
        "total": result.get("total"),
        "data": [
            profile.to_dict() for profile in (data or [])
        ]
    }