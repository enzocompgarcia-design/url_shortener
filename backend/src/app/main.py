from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.links import shorten_link_router
from app.core.id_generator import IDGenerator
from app.database.cache.connections import get_id_generator
from app.database.cassandra.connections import create_tables
from app.errors.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    app.state.id_generator = IDGenerator(cache=get_id_generator())

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(shorten_link_router)
