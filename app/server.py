from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.core.settings import settings
from app.core.exception_handlers import add_exception_handlers
from app.db.database import init_db, Base
import app.db.database as db_module
import app.db.seeds.seeder as seeder
from app.models.profile import Profile  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.TESTING:
        init_db()
        if settings.ENV == "production":
            Base.metadata.create_all(bind=db_module.engine)
            seeder.seed_profiles()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_exception_handlers(app)
app.include_router(api_router)

reload = False
if settings.ENV == "development":
    reload = True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app.server:app", reload=reload)
