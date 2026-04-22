from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import init_db
from app.models.profile import Profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield


app = FastAPI(lifespan=lifespan)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app=app)