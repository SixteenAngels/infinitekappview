import json
from typing import Dict, List

from core.mqtt import mqtt_service


class RulesEngine:
    def evaluate_and_act(self, telemetry: Dict) -> None:
        # Placeholder: In a real implementation, load user rules, match, and publish actions
        # Example: if temperature > threshold then publish command
        try:
            sensor = telemetry.get("sensor")
            value = float(telemetry.get("value"))
            device_id = telemetry.get("device_id")
        except Exception:
            return

        # Simple demo rule (not persisted): if temperature > 28 -> publish fan on
        if sensor == "temperature" and value > 28:
            mqtt_service.publish_json(f"infinitek/cmnd/{device_id}", {"state": "ON"}, qos=1)


rules_engine = RulesEngine()
