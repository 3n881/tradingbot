from fastapi import APIRouter
from collections import Counter

router = APIRouter()

@router.get("/bot/{bot_id}")
def get_bot_analytics(bot_id: int):
    """Analyze bot actions from the log file."""
    analytics = {"activations": 0, "executions": 0, "buy": 0, "sell": 0, "hold": 0}
    try:
        with open("bot_actions.log", "r") as f:
            logs = f.readlines()
        bot_logs = [log for log in logs if f"Bot ID: {bot_id}" in log]

        # Count activations and executions
        activations = [log for log in bot_logs if "activate" in log]
        executions = [log for log in bot_logs if "execute" in log]
        analytics["activations"] = len(activations)
        analytics["executions"] = len(executions)

        # Count decisions
        decisions = [log.split("Details: ")[1].strip() for log in executions if "Bot decision" in log]
        decision_counts = Counter(decisions)
        analytics.update(decision_counts)

    except Exception as e:
        return {"error": f"Failed to read log file: {str(e)}"}
    return analytics
