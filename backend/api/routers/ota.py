import hashlib
import os
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from core.config import settings
from core.db import get_db
from core.security import get_current_user_id
from core.mqtt import mqtt_service
from services.storage import storage

router = APIRouter(prefix="/ota", tags=["ota"])

OTA_DIR = Path("./ota_files")
OTA_DIR.mkdir(exist_ok=True)


@router.post("/upload")
def upload_firmware(
    device_id: str,
    version: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    # Save file via pluggable storage (local or S3)
    filename = f"{device_id}_{version}_{int(datetime.utcnow().timestamp())}.bin"
    content = file.file.read()
    checksum = hashlib.sha256(content).hexdigest()
    download_url = storage.save_firmware_and_get_url(filename, content)

    # Notify device via MQTT
    mqtt_service.publish_json(
        topic=f"infinitek/ota/{device_id}",
        payload={"version": version, "url": download_url, "checksum": checksum},
        qos=1,
    )

    return {"filename": filename, "checksum": checksum, "url": download_url}
