import secrets

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.services.github import build_github_auth_url, pkce_challange


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/github")
async def github_login(request: Request):
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = pkce_challange(code_verifier)

    url = build_github_auth_url(
        state=state,
        code_challenge=code_challenge
    )
    return RedirectResponse(url)
