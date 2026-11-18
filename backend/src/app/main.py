from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.health import health_router
from app.api.routers.links import shorten_link_router
from app.config import config
from app.core.id_generator import IDGenerator
from app.database.cache.connections import close_redis, get_id_generator, init_redis
from app.database.cassandra.connections import create_tables
from app.errors.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    await init_redis()

    app.state.id_generator = IDGenerator(cache=get_id_generator())

    yield

    await close_redis()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

register_exception_handlers(app)

app.include_router(shorten_link_router)
app.include_router(health_router)
