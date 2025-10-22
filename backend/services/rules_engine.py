import json
import logging
from typing import Any, Dict, List, Union

from core.db import SessionLocal
from core.mqtt import mqtt_service
from models.rule import Rule


logger = logging.getLogger(__name__)


Condition = Dict[str, Any]


def _compare(op: str, left: float, right: float) -> bool:
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    return False


def _match_conditions(telemetry: Dict[str, Any], cond: Union[Condition, List[Condition]]) -> bool:
    conditions: List[Condition] = cond if isinstance(cond, list) else [cond]
    for c in conditions:
        sensor_ok = True
        if "sensor" in c:
            sensor_ok = telemetry.get("sensor") == c.get("sensor")
        value_ok = True
        if "op" in c and "value" in c:
            try:
                tval = float(telemetry.get("value"))
                rval = float(c.get("value"))
                value_ok = _compare(str(c.get("op")), tval, rval)
            except Exception:
                value_ok = False
        if not (sensor_ok and value_ok):
            return False
    return True


class RulesEngine:
    def evaluate_and_act(self, owner_id: str, telemetry: Dict[str, Any]) -> None:
        db = SessionLocal()
        try:
            rules: List[Rule] = (
                db.query(Rule)
                .filter(Rule.owner_id == owner_id, Rule.enabled == True)  # noqa: E712
                .all()
            )
            for r in rules:
                try:
                    conditions = json.loads(r.conditions)
                except Exception:
                    logger.warning("Invalid rule conditions JSON for rule_id=%s", r.id)
                    continue
                if not _match_conditions(telemetry, conditions):
                    continue
                # Execute action
                try:
                    actions = json.loads(r.actions)
                except Exception:
                    logger.warning("Invalid rule actions JSON for rule_id=%s", r.id)
                    continue
                topic = actions.get("topic")
                payload = actions.get("payload", {})
                if isinstance(topic, str):
                    topic_formatted = topic.format(**telemetry)
                    mqtt_service.publish_json(topic_formatted, payload, qos=1)
        finally:
            db.close()


rules_engine = RulesEngine()
