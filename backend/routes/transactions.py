"""
Transaction History & Budget Planner Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from datetime import datetime
import json
import logging
from pathlib import Path
from pydantic import BaseModel

from auth.dependencies import get_current_user
from user_manager_json import UserManagerJSON

router = APIRouter(tags=["Transactions"])
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_DIR = BASE_DIR / "user_data"
BUDGET_DIR = BASE_DIR / "user_budgets"
BUDGET_DIR.mkdir(exist_ok=True)


class BudgetItem(BaseModel):
    category: str
    limit: float


class BudgetUpdate(BaseModel):
    budgets: List[BudgetItem]


def _get_account_number(user_id: str) -> Optional[str]:
    """Resolve user_id to account number folder."""
    from user_manager_json import UserManagerJSON
    for acc, info in UserManagerJSON._account_to_user_map.items():
        if info["user_id"] == user_id:
            return acc
    return None


def _parse_transactions(financial_data: dict) -> List[dict]:
    """Parse raw bank transaction JSON into a clean list."""
    txns = []
    bank_data = financial_data.get("fetch_bank_transactions", {})

    raw_list = []
    if isinstance(bank_data, dict):
        raw_list = bank_data.get("bankTransactions", [])
    elif isinstance(bank_data, list):
        raw_list = bank_data

    type_map = {1: "CREDIT", 2: "DEBIT", 4: "INTEREST", 6: "INSTALLMENT"}

    for bank_entry in raw_list:
        bank_name = bank_entry.get("bank", "Bank") if isinstance(bank_entry, dict) else "Bank"
        raw_txns = bank_entry.get("txns", []) if isinstance(bank_entry, dict) else []

        for t in raw_txns:
            if not isinstance(t, list) or len(t) < 4:
                continue
            amount_raw, narration, date_str, txn_type = t[0], t[1], t[2], t[3]
            mode = t[4] if len(t) > 4 else "N/A"
            balance = t[5] if len(t) > 5 else 0

            try:
                amount = float(str(amount_raw).replace(",", ""))
            except Exception:
                amount = 0.0

            # Infer category from narration
            narration_lower = narration.lower()
            if any(k in narration_lower for k in ["salary", "credit"]):
                category = "Income"
            elif any(k in narration_lower for k in ["rent", "landlord"]):
                category = "Housing"
            elif any(k in narration_lower for k in ["sip", "mutualfund", "mf"]):
                category = "Investment"
            elif any(k in narration_lower for k in ["zomato", "swiggy", "food", "restaurant"]):
                category = "Food"
            elif any(k in narration_lower for k in ["amazon", "flipkart", "shopping"]):
                category = "Shopping"
            elif any(k in narration_lower for k in ["emi", "loan", "installment"]):
                category = "Loan EMI"
            elif any(k in narration_lower for k in ["electricity", "water", "bill", "utility"]):
                category = "Utilities"
            elif any(k in narration_lower for k in ["petrol", "fuel", "uber", "ola", "transport"]):
                category = "Transport"
            elif any(k in narration_lower for k in ["netflix", "spotify", "subscription"]):
                category = "Entertainment"
            elif any(k in narration_lower for k in ["hospital", "medical", "pharmacy", "health"]):
                category = "Healthcare"
            elif any(k in narration_lower for k in ["insurance"]):
                category = "Insurance"
            elif any(k in narration_lower for k in ["atm", "cash"]):
                category = "Cash Withdrawal"
            else:
                category = "Others"

            txns.append({
                "id": f"{date_str}_{amount}_{len(txns)}",
                "date": date_str,
                "narration": narration,
                "amount": amount,
                "type": type_map.get(txn_type, "DEBIT"),
                "mode": mode,
                "balance": float(str(balance).replace(",", "")) if balance else 0,
                "category": category,
                "bank": bank_name,
            })

    # Sort by date descending
    txns.sort(key=lambda x: x["date"], reverse=True)
    return txns


@router.get("/transactions")
async def get_transactions(
    category: Optional[str] = None,
    txn_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    current_user: Dict = Depends(get_current_user)
):
    """Get all transactions with optional filters."""
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        txns = _parse_transactions(financial_data)

        if category and category != "All":
            txns = [t for t in txns if t["category"] == category]
        if txn_type and txn_type != "All":
            txns = [t for t in txns if t["type"] == txn_type]
        if search:
            s = search.lower()
            txns = [t for t in txns if s in t["narration"].lower() or s in t["category"].lower()]

        total_credit = sum(t["amount"] for t in txns if t["type"] == "CREDIT")
        total_debit  = sum(t["amount"] for t in txns if t["type"] != "CREDIT")

        return {
            "success": True,
            "transactions": txns[:limit],
            "total": len(txns),
            "total_credit": total_credit,
            "total_debit": total_debit,
        }
    except Exception as e:
        logger.error(f"Transaction fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions/summary")
async def get_transaction_summary(current_user: Dict = Depends(get_current_user)):
    """Get category-wise spending summary."""
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        txns = _parse_transactions(financial_data)

        summary: dict = {}
        for t in txns:
            if t["type"] != "CREDIT":
                cat = t["category"]
                summary[cat] = summary.get(cat, 0) + t["amount"]

        return {
            "success": True,
            "summary": [{"category": k, "amount": round(v, 2)} for k, v in sorted(summary.items(), key=lambda x: -x[1])],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Budget Planner ────────────────────────────────────────────────────────────

def _budget_file(user_id: str) -> Path:
    return BUDGET_DIR / f"{user_id}_budget.json"


def _load_budget(user_id: str) -> dict:
    f = _budget_file(user_id)
    if f.exists():
        try:
            return json.loads(f.read_text())
        except Exception:
            pass
    # Default budget
    return {
        "Housing": 20000, "Food": 8000, "Transport": 4000,
        "Shopping": 6000, "Entertainment": 2000, "Utilities": 3000,
        "Healthcare": 2000, "Insurance": 3000, "Loan EMI": 10000, "Others": 5000,
    }


def _save_budget(user_id: str, budget: dict):
    _budget_file(user_id).write_text(json.dumps(budget, indent=2))


@router.get("/budget")
async def get_budget(current_user: Dict = Depends(get_current_user)):
    """Get user's budget limits and current spending."""
    try:
        user_id = current_user.get("sub")
        budget = _load_budget(user_id)

        # Get actual spending this month
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        txns = _parse_transactions(financial_data)
        current_month = datetime.now().strftime("%Y-%m")
        month_txns = [t for t in txns if t["date"].startswith(current_month) and t["type"] != "CREDIT"]

        spending: dict = {}
        for t in month_txns:
            spending[t["category"]] = spending.get(t["category"], 0) + t["amount"]

        result = []
        for category, limit in budget.items():
            spent = spending.get(category, 0)
            pct = min(100, round(spent / limit * 100, 1)) if limit > 0 else 0
            result.append({
                "category": category,
                "limit": limit,
                "spent": round(spent, 2),
                "remaining": max(0, round(limit - spent, 2)),
                "percentage": pct,
                "status": "danger" if pct >= 90 else "warning" if pct >= 70 else "good",
            })

        return {"success": True, "budget": result, "month": current_month}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/budget")
async def update_budget(
    body: BudgetUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update budget limits."""
    try:
        user_id = current_user.get("sub")
        budget = {item.category: item.limit for item in body.budgets}
        _save_budget(user_id, budget)
        return {"success": True, "message": "Budget updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Profile Update ────────────────────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None


@router.put("/profile")
async def update_profile(
    body: ProfileUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """Update user profile and persist to JSON file."""
    try:
        user_id = current_user.get("sub")
        acc = _get_account_number(user_id)
        if not acc:
            raise HTTPException(status_code=404, detail="User not found")

        profile_path = USER_DATA_DIR / acc / "profile.json"
        if not profile_path.exists():
            raise HTTPException(status_code=404, detail="Profile file not found")

        profile = json.loads(profile_path.read_text())
        updates = body.model_dump(exclude_none=True)

        field_map = {"location": "city", "name": "name", "occupation": "occupation", "age": "age"}
        for k, v in updates.items():
            mapped = field_map.get(k, k)
            profile[mapped] = v

        profile_path.write_text(json.dumps(profile, indent=2))
        return {"success": True, "message": "Profile updated", "profile": profile}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Smart Notifications ───────────────────────────────────────────────────────

@router.get("/smart-notifications")
async def get_smart_notifications(current_user: Dict = Depends(get_current_user)):
    """Generate smart notifications from user's actual financial data."""
    try:
        user_id = current_user.get("sub")
        financial_data = UserManagerJSON.get_all_user_data(user_id)
        txns = _parse_transactions(financial_data)
        budget = _load_budget(user_id)

        current_month = datetime.now().strftime("%Y-%m")
        month_txns = [t for t in txns if t["date"].startswith(current_month)]

        notifications = []
        nid = 1

        # Budget alerts
        spending: dict = {}
        for t in month_txns:
            if t["type"] != "CREDIT":
                spending[t["category"]] = spending.get(t["category"], 0) + t["amount"]

        for cat, limit in budget.items():
            spent = spending.get(cat, 0)
            pct = spent / limit * 100 if limit > 0 else 0
            if pct >= 100:
                notifications.append({
                    "id": nid, "type": "danger", "category": "Budget",
                    "title": f"{cat} Budget Exceeded",
                    "message": f"You've spent ₹{spent:,.0f} on {cat} this month, exceeding your ₹{limit:,.0f} limit by ₹{spent-limit:,.0f}.",
                    "time": "This month", "read": False,
                })
                nid += 1
            elif pct >= 80:
                notifications.append({
                    "id": nid, "type": "warning", "category": "Budget",
                    "title": f"{cat} Budget at {pct:.0f}%",
                    "message": f"You've used ₹{spent:,.0f} of your ₹{limit:,.0f} {cat} budget. Only ₹{limit-spent:,.0f} remaining.",
                    "time": "This month", "read": False,
                })
                nid += 1

        # Large transaction alerts
        for t in month_txns[:20]:
            if t["type"] != "CREDIT" and t["amount"] >= 10000:
                notifications.append({
                    "id": nid, "type": "info", "category": "Transaction",
                    "title": f"Large Transaction: ₹{t['amount']:,.0f}",
                    "message": f"{t['narration']} — ₹{t['amount']:,.0f} via {t['mode']} on {t['date']}.",
                    "time": t["date"], "read": False,
                })
                nid += 1
                if nid > 10:
                    break

        # Net worth from data
        nw_data = financial_data.get("fetch_net_worth", {})
        net_worth = nw_data.get("net_worth", nw_data.get("netWorth", 0)) if isinstance(nw_data, dict) else 0
        if net_worth:
            notifications.append({
                "id": nid, "type": "success", "category": "Wealth",
                "title": "Net Worth Update",
                "message": f"Your current net worth is ₹{float(net_worth):,.0f}. Keep up the great financial discipline!",
                "time": "Today", "read": False,
            })
            nid += 1

        # SIP reminder
        sip_txns = [t for t in month_txns if "sip" in t["narration"].lower() or "mutualfund" in t["narration"].lower()]
        if sip_txns:
            total_sip = sum(t["amount"] for t in sip_txns)
            notifications.append({
                "id": nid, "type": "success", "category": "Investment",
                "title": "SIP Processed Successfully",
                "message": f"₹{total_sip:,.0f} invested via SIP this month. Compounding is working for you!",
                "time": "This month", "read": False,
            })
            nid += 1

        return {"success": True, "notifications": notifications, "unread": len([n for n in notifications if not n["read"]])}
    except Exception as e:
        logger.error(f"Smart notifications error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
