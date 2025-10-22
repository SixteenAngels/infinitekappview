from fastapi import APIRouter, Depends

from core.security import get_current_user_id

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.get("/lgwebos/status")
def lgwebos_status(user_id: str = Depends(get_current_user_id)):
    # Stub endpoint to show connector readiness
    return {"connector": "LG WebOS", "status": "ready"}
