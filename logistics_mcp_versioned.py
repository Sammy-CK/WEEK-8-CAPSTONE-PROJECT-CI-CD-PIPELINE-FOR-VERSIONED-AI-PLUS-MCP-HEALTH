"""AfyaPlus logistics MCP — semver in version://current resource."""
import json
import logging

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    filename="mcp_server.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MCP_VERSION = "1.1.0"
mcp = FastMCP("afyaplus-logistics")

with open("clinics.json", encoding="utf-8") as f:
    CLINICS = {c["id"]: c for c in json.load(f)}


@mcp.resource("version://current")
def version_current() -> str:
    """Semver of this MCP server. Agents and CI should read this."""
    return MCP_VERSION


@mcp.tool()
def check_stock(clinic_id: str, item: str) -> dict:
    """Check stock of a medical item at one clinic."""
    logging.info("tool=check_stock clinic=%s item=%s", clinic_id, item)
    clinic = CLINICS.get(clinic_id)
    if clinic is None:
        return {"error": f"Unknown clinic_id {clinic_id!r}"}
    qty = clinic["stock"].get(item.lower().strip())
    if qty is None:
        return {"error": f"Item {item!r} not tracked"}
    return {
        "clinic": clinic["name"],
        "item": item,
        "quantity": qty,
        "reorder_needed": qty < clinic["reorder_level"],
    }


@mcp.tool()
def list_low_stock(clinic_id: str) -> dict:
    """List items at or below reorder_level (additive in 1.1.0)."""
    logging.info("tool=list_low_stock clinic=%s", clinic_id)
    clinic = CLINICS.get(clinic_id)
    if clinic is None:
        return {"error": f"Unknown clinic_id {clinic_id!r}"}
    low = [
        {"item": k, "quantity": v}
        for k, v in clinic["stock"].items()
        if v < clinic["reorder_level"]
    ]
    return {"clinic": clinic["name"], "low_stock": low, "mcp_version": MCP_VERSION}


if __name__ == "__main__":
    mcp.run()
