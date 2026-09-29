from tool_metrics import tool_report

ALERT_THRESHOLD = 0.10


def alert_if_error_rate(tool: str, threshold: float = ALERT_THRESHOLD) -> bool:
    row = tool_report().get(tool) or {"error_rate": 0}
    if row["error_rate"] >= threshold:
        print("ALERT", tool, row)
        return True
    return False


def summary() -> dict:
    return tool_report()
