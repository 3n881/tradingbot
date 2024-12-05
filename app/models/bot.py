
class Bot:
    id_counter = 1
    db = []

    @classmethod
    def create(cls, user_id, name, strategy, configuration):
        bot = {
            "id": cls.id_counter,
            "user_id": user_id,
            "name": name,
            "strategy": strategy,
            "configuration": configuration,
            "status": "inactive",  # Default bot status
        }
        cls.db.append(bot)
        cls.id_counter += 1
        return bot

    @classmethod
    def list(cls, user_id):
        return [bot for bot in cls.db if bot["user_id"] == user_id]

    @classmethod
    def update(cls, bot_id, user_id, name, strategy, configuration):
        for bot in cls.db:
            if bot["id"] == bot_id and bot["user_id"] == user_id:
                bot.update({"name": name, "strategy": strategy, "configuration": configuration})
                return bot
        return None

    @classmethod
    def delete(cls, bot_id, user_id):
        for bot in cls.db:
            if bot["id"] == bot_id and bot["user_id"] == user_id:
                cls.db.remove(bot)
                return True
        return False

    @classmethod
    def update_status(cls, bot_id, user_id, status):
        for bot in cls.db:
            if bot["id"] == bot_id and bot["user_id"] == user_id:
                bot["status"] = status
                return bot
        return None
