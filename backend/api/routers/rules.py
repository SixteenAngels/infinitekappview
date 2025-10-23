from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from core.security import get_current_user_id
from models.rule import Rule
from schemas.rules import RuleCreate, RulePublic, RuleUpdate

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("/", response_model=List[RulePublic])
def list_rules(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    rules = db.query(Rule).filter(Rule.owner_id == user_id).order_by(Rule.id.desc()).all()
    return [RulePublic.model_validate(r, from_attributes=True) for r in rules]


@router.post("/", response_model=RulePublic)
def create_rule(rule_in: RuleCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    rule = Rule(name=rule_in.name, conditions=rule_in.conditions, actions=rule_in.actions, enabled=True, owner_id=user_id)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return RulePublic.model_validate(rule, from_attributes=True)


@router.patch("/{id}", response_model=RulePublic)
def update_rule(id: int, rule_in: RuleUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    rule: Optional[Rule] = db.query(Rule).filter(Rule.id == id, Rule.owner_id == user_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    if rule_in.name is not None:
        rule.name = rule_in.name
    if rule_in.conditions is not None:
        rule.conditions = rule_in.conditions
    if rule_in.actions is not None:
        rule.actions = rule_in.actions
    if rule_in.enabled is not None:
        rule.enabled = rule_in.enabled
    db.commit()
    db.refresh(rule)
    return RulePublic.model_validate(rule, from_attributes=True)


@router.delete("/{id}")
def delete_rule(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    rule: Optional[Rule] = db.query(Rule).filter(Rule.id == id, Rule.owner_id == user_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return {"ok": True}
