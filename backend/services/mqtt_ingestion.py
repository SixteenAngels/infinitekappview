import json
from datetime import datetime

from core.mqtt import mqtt_service
from core.db import SessionLocal
from models.measurement import Measurement
from models.device import Device
from services.rules_engine import rules_engine


def handle_mqtt_message(topic: str, payload: str) -> None:
    # Expected topics: infinitek/tele/<device_id>/<sensor>
    try:
        parts = topic.split("/")
        _, _, device_id, sensor = parts
        data = json.loads(payload)
        telemetry = {"device_id": device_id, "sensor": sensor, **data}

        # Persist to DB if device exists to resolve owner
        db = SessionLocal()
        try:
            device = db.query(Device).filter(Device.device_id == device_id).first()
            if device is not None:
                m = Measurement(
                    device_id=device_id,
                    sensor=sensor,
                    value=float(data.get("value")),
                    unit=data.get("unit"),
                    created_at=datetime.utcnow(),
                    owner_id=device.owner_id,
                )
                db.add(m)
                db.commit()
            # Evaluate rules (stateless stub for now)
            rules_engine.evaluate_and_act(telemetry)
        finally:
            db.close()
    except Exception as e:
        print(f"Failed to process MQTT message: {e}")


mqtt_service.set_on_message(handle_mqtt_message)
