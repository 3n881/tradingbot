
from fastapi import APIRouter, Depends, HTTPException, status
from app.routers.auth import get_current_user
from typing import List

router = APIRouter()

class Strategy:
    id_counter = 1
    db = []

    @classmethod
    def create(cls, user_id, name, description, parameters, price):
        strategy = {"id": cls.id_counter, "user_id": user_id, "name": name, "description": description, "parameters": parameters, "price": price}
        cls.db.append(strategy)
        cls.id_counter += 1
        return strategy

    @classmethod
    def list(cls):
        return cls.db

    @classmethod
    def update(cls, strategy_id, user_id, name, description, parameters, price):
        for strategy in cls.db:
            if strategy["id"] == strategy_id and strategy["user_id"] == user_id:
                strategy.update({"name": name, "description": description, "parameters": parameters, "price": price})
                return strategy
        return None

    @classmethod
    def delete(cls, strategy_id, user_id):
        for strategy in cls.db:
            if strategy["id"] == strategy_id and strategy["user_id"] == user_id:
                cls.db.remove(strategy)
                return True
        return False

@router.post("/", response_model=dict)
def create_strategy(name: str, description: str, parameters: dict, price: float, user=Depends(get_current_user)):
    new_strategy = Strategy.create(user["username"], name, description, parameters, price)
    return new_strategy

@router.get("/", response_model=List[dict])
def list_strategies():
    return Strategy.list()

@router.put("/{strategy_id}", response_model=dict)
def update_strategy(strategy_id: int, name: str, description: str, parameters: dict, price: float, user=Depends(get_current_user)):
    updated_strategy = Strategy.update(strategy_id, user["username"], name, description, parameters, price)
    if not updated_strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return updated_strategy

@router.delete("/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(strategy_id: int, user=Depends(get_current_user)):
    success = Strategy.delete(strategy_id, user["username"])
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return None
