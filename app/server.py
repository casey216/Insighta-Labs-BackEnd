from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.core.settings import settings
from app.core.exception_handlers import add_exception_handlers
from app.db.database import init_db, Base
import app.db.database as db_module
import app.db.seeds.seeder as seeder
from app.models.profile import Profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.TESTING:
        init_db()
        Base.metadata.create_all(bind=db_module.engine)
        seeder.seed_profiles()

    yield


app = FastAPI(lifespan=lifespan)
add_exception_handlers(app)
app.include_router(api_router)

reload = False
if settings.ENV == "development":
    reload = True

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app="app.server:app", reload=reload)