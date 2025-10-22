from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from core.config import settings


class Storage(Protocol):
    def save_firmware_and_get_url(self, filename: str, content: bytes) -> str: ...


class LocalStorage:
    def __init__(self) -> None:
        self.ota_dir = Path("./ota_files")
        self.ota_dir.mkdir(exist_ok=True)

    def save_firmware_and_get_url(self, filename: str, content: bytes) -> str:
        dest = self.ota_dir / filename
        with open(dest, "wb") as f:
            f.write(content)
        return f"/static/ota/{filename}"


try:
    import boto3  # type: ignore
    from botocore.client import Config as BotoConfig  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    boto3 = None  # type: ignore


class S3Storage:
    def __init__(self) -> None:
        assert boto3 is not None, "boto3 is required for S3 storage"
        self.bucket = os.environ.get("S3_BUCKET", "")
        self.region = os.environ.get("S3_REGION", None)
        self.client = boto3.client("s3", region_name=self.region, config=BotoConfig(signature_version="s3v4"))

    def save_firmware_and_get_url(self, filename: str, content: bytes) -> str:
        key = f"ota/{filename}"
        self.client.put_object(Bucket=self.bucket, Key=key, Body=content, ContentType="application/octet-stream")
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=int(os.environ.get("S3_URL_EXPIRES", "900")),
        )
        return url


def _select_storage() -> Storage:
    if os.environ.get("USE_S3_OTA", "false").lower() in {"1", "true", "yes"}:
        return S3Storage()
    return LocalStorage()


storage: Storage = _select_storage()
