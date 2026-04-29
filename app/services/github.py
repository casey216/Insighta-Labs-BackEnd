import base64
import hashlib

from app.core.settings import settings


GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"


def build_github_auth_url(state: str, code_challenge: str) -> str:
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "scope": "read:user user:email",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{GITHUB_AUTH_URL}?{query}"


def pkce_challange(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
