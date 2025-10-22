import json
from typing import Callable, Optional

import paho.mqtt.client as mqtt

from core.config import settings


class MQTTService:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self._on_message_handler: Optional[Callable[[str, str], None]] = None

    def connect(self) -> None:
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        # Credentials
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        # TLS
        if settings.MQTT_TLS:
            if settings.MQTT_TLS_CA_FILE:
                self.client.tls_set(ca_certs=settings.MQTT_TLS_CA_FILE)
            else:
                self.client.tls_set()  # use default certs
            if settings.MQTT_TLS_INSECURE:
                self.client.tls_insecure_set(True)
        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)

    def loop_start(self) -> None:
        self.client.loop_start()

    def loop_stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def publish_json(self, topic: str, payload: dict, qos: int = 0, retain: bool = False) -> None:
        self.client.publish(topic, json.dumps(payload), qos=qos, retain=retain)

    def subscribe(self, topic: str, qos: int = 0) -> None:
        self.client.subscribe(topic, qos=qos)

    def set_on_message(self, handler: Callable[[str, str], None]) -> None:
        self._on_message_handler = handler

    def _on_connect(self, client, userdata, flags, rc):
        # Subscribe to telemetry topics
        self.subscribe("infinitek/tele/#")

    def _on_message(self, client, userdata, msg):
        if self._on_message_handler:
            try:
                self._on_message_handler(msg.topic, msg.payload.decode())
            except Exception as e:
                print(f"on_message handler error: {e}")


mqtt_service = MQTTService()
