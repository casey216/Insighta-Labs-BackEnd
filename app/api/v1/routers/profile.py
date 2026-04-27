from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.nlp_parser import parse_natural_language_query
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
        db,
        filter_prams,
        p,
        sort_params
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


@router.get("/search")
def nlq_search(
    q: Annotated[str, Query(default=None)],
    p: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Missing or empty query parameter")

    filters = parse_natural_language_query(q)
    if filters is None:
        raise HTTPException(
            status_code=422,
            detail="Unable to interpret query"
        )
    
    result = ProfileService.get_all_profiles(
        db,
        filters,
        p
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
    