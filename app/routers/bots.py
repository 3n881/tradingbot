

# from fastapi import APIRouter, Depends, HTTPException, status
# from app.routers.auth import get_current_user
# from typing import List
# from app.services.bot_execution_service import BotExecutionService

# router = APIRouter()
# execution_service = BotExecutionService()

# class Bot:
#     id_counter = 1
#     db = []

#     @classmethod
#     def create(cls, user_id, name, strategy, configuration):
#         bot = {"id": cls.id_counter, "user_id": user_id, "name": name, "strategy": strategy, "configuration": configuration}
#         cls.db.append(bot)
#         cls.id_counter += 1
#         return bot

#     @classmethod
#     def list(cls, user_id):
#         return [bot for bot in cls.db if bot["user_id"] == user_id]

#     @classmethod
#     def update(cls, bot_id, user_id, name, strategy, configuration):
#         for bot in cls.db:
#             if bot["id"] == bot_id and bot["user_id"] == user_id:
#                 bot.update({"name": name, "strategy": strategy, "configuration": configuration})
#                 return bot
#         return None

#     @classmethod
#     def delete(cls, bot_id, user_id):
#         for bot in cls.db:
#             if bot["id"] == bot_id and bot["user_id"] == user_id:
#                 cls.db.remove(bot)
#                 return True
#         return False

# @router.post("/", response_model=dict)
# def create_bot(name: str, strategy: str, configuration: dict, user=Depends(get_current_user)):
#     new_bot = Bot.create(user["username"], name, strategy, configuration)
#     return new_bot

# @router.get("/", response_model=List[dict])
# def list_bots(user=Depends(get_current_user)):
#     return Bot.list(user["username"])

# @router.put("/{bot_id}", response_model=dict)
# def update_bot(bot_id: int, name: str, strategy: str, configuration: dict, user=Depends(get_current_user)):
#     updated_bot = Bot.update(bot_id, user["username"], name, strategy, configuration)
#     if not updated_bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     return updated_bot

# @router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_bot(bot_id: int, user=Depends(get_current_user)):
#     success = Bot.delete(bot_id, user["username"])
#     if not success:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     return None

# @router.post("/{bot_id}/activate")
# def activate_bot(bot_id: int, user=Depends(get_current_user)):
#     bot = Bot.update_status(bot_id, user["username"], "active")
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     return {"message": "Bot activated successfully", "bot": bot}

# @router.post("/{bot_id}/execute")
# def execute_bot(bot_id: int, user=Depends(get_current_user)):
#     bot = next((b for b in Bot.db if b["id"] == bot_id and b["user_id"] == user["username"]), None)
#     if not bot:
#         raise HTTPException(status_code=404, detail="Bot not found")
#     if bot["status"] != "active":
#         raise HTTPException(status_code=400, detail="Bot is not active")
#     decision = execution_service.execute_bot(bot)
#     return {"bot_id": bot_id, "decision": decision}

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.models.bot import Bot  # Assuming Bot is defined in app/models/bot.py
from app.utils.logger import log_bot_action


router = APIRouter()

# Simulating authentication for now
def get_current_user():
    return {"username": "user1"}  # Replace with real user extraction logic (e.g., JWT)

# Pydantic models
class BotBase(BaseModel):
    name: str
    strategy: str
    configuration: dict

class BotCreate(BotBase):
    pass

class BotResponse(BotBase):
    id: int
    status: str

# Endpoints
@router.post("/", response_model=BotResponse)
def create_bot(bot: BotCreate, user=Depends(get_current_user)):
    new_bot = Bot.create(user["username"], bot.name, bot.strategy, bot.configuration)
    return new_bot

@router.get("/", response_model=List[BotResponse])
def list_bots(user=Depends(get_current_user)):
    return Bot.list(user["username"])

@router.put("/{bot_id}", response_model=BotResponse)
def update_bot(bot_id: int, bot: BotCreate, user=Depends(get_current_user)):
    updated_bot = Bot.update(bot_id, user["username"], bot.name, bot.strategy, bot.configuration)
    if not updated_bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return updated_bot

@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bot(bot_id: int, user=Depends(get_current_user)):
    success = Bot.delete(bot_id, user["username"])
    if not success:
        raise HTTPException(status_code=404, detail="Bot not found")
    return None

@router.post("/{bot_id}/activate", response_model=dict)
def activate_bot(bot_id: int, user=Depends(get_current_user)):
    bot = Bot.update_status(bot_id, user["username"], "active")
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"message": "Bot activated successfully", "bot": bot}

@router.post("/{bot_id}/execute", response_model=dict)
def execute_bot(bot_id: int, user=Depends(get_current_user)):
    bot = next((b for b in Bot.db if b["id"] == bot_id and b["user_id"] == user["username"]), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot["status"] != "active":
        raise HTTPException(status_code=400, detail="Bot is not active")
    decision = f"Executed bot {bot['name']} with strategy {bot['strategy']}"  # Mock execution logic
    return {"bot_id": bot_id, "decision": decision}

@router.post("/{bot_id}/activate")
def activate_bot(bot_id: int, user=Depends(get_current_user)):
    bot = Bot.update_status(bot_id, user["username"], "active")
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    log_bot_action(bot_id, "activate", "Bot activated successfully")
    return {"message": "Bot activated successfully", "bot": bot}

@router.post("/{bot_id}/execute")
def execute_bot(bot_id: int, user=Depends(get_current_user)):
    bot = next((b for b in Bot.db if b["id"] == bot_id and b["user_id"] == user["username"]), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot["status"] != "active":
        raise HTTPException(status_code=400, detail="Bot is not active")
    decision = execution_service.execute_bot(bot)
    log_bot_action(bot_id, "execute", f"Bot decision: {decision}")
    return {"bot_id": bot_id, "decision": decision}