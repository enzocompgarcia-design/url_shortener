from fastapi import APIRouter, Depends

from app.api.dependencies import get_healthy_service
from app.services.healthy_service import HealthyService

health_router = APIRouter(tags=["health"])


@health_router.get("/health", include_in_schema=False)
async def health(service: HealthyService = Depends(get_healthy_service)):
    return service.health()


@health_router.get("/ready", include_in_schema=False)
async def ready(service: HealthyService = Depends(get_healthy_service)):
    return await service.ready()
