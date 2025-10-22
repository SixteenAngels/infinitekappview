from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.db import Base, engine
from core.mqtt import mqtt_service
from api.routers import auth, devices, measurements, rules, ota, connectors, config_sync
from api.routers import ws as ws_router
import services.mqtt_ingestion  # noqa: F401  # ensure MQTT handler registration
from core.logging import configure_logging
from core.metrics import MetricsMiddleware, router as metrics_router

configure_logging()
app = FastAPI(title="Infinitek Smart Control", version="0.1.0")
app.add_middleware(MetricsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list if settings.cors_origin_list != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers under prefix
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(devices.router, prefix=settings.API_PREFIX)
app.include_router(measurements.router, prefix=settings.API_PREFIX)
app.include_router(rules.router, prefix=settings.API_PREFIX)
app.include_router(ota.router, prefix=settings.API_PREFIX)
app.include_router(connectors.router, prefix=settings.API_PREFIX)
app.include_router(config_sync.router, prefix=settings.API_PREFIX)
app.include_router(ws_router.router)
app.include_router(metrics_router)

# Mount static files for OTA downloads
ota_dir = Path("./ota_files")
ota_dir.mkdir(exist_ok=True)
app.mount("/static/ota", StaticFiles(directory=str(ota_dir)), name="ota")


@app.get("/")
def root():
    return {"name": "Infinitek Smart Control", "api_prefix": settings.API_PREFIX}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    try:
        mqtt_service.connect()
        mqtt_service.loop_start()
    except Exception as e:
        # Log but don't crash during dev
        print(f"MQTT start failed: {e}")


@app.on_event("shutdown")
def on_shutdown():
    try:
        mqtt_service.loop_stop()
    except Exception:
        pass
