"""
AUREXIS AI — Portfolio Analytics
Processes stocks and mutual fund data from user JSON files.
"""

from typing import Dict, Any, List
from datetime import datetime


def compute_stocks(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process stock transaction data into portfolio summary."""
    stock_data = financial_data.get("fetch_stock_transactions", {})
    stocks     = stock_data.get("stockTransactions", [])

    if not stocks:
        return {"holdings": [], "totalValue": 0, "totalInvested": 0, "totalPnL": 0, "totalPnLPct": 0}

    holdings = []
    total_value    = 0
    total_invested = 0

    for stock in stocks:
        txns = stock.get("transactions", [])
        buy_txns  = [t for t in txns if t.get("type") == "BUY"]
        sell_txns = [t for t in txns if t.get("type") == "SELL"]

        total_qty      = sum(t.get("quantity", 0) for t in buy_txns)
        sold_qty       = sum(t.get("quantity", 0) for t in sell_txns)
        holding_qty    = total_qty - sold_qty
        avg_buy_price  = (sum(t.get("price", 0) * t.get("quantity", 0) for t in buy_txns) / total_qty) if total_qty > 0 else 0
        invested       = avg_buy_price * holding_qty
        current_price  = stock.get("currentPrice", avg_buy_price * 1.10)
        current_value  = current_price * holding_qty
        pnl            = current_value - invested
        pnl_pct        = round(pnl / invested * 100, 2) if invested > 0 else 0

        # Day change simulation
        day_change_pct = round((current_price - avg_buy_price * 1.08) / (avg_buy_price * 1.08) * 100, 2)

        holdings.append({
            "symbol":       stock.get("symbol", ""),
            "companyName":  stock.get("companyName", ""),
            "exchange":     stock.get("exchange", "NSE"),
            "quantity":     holding_qty,
            "avgBuyPrice":  round(avg_buy_price, 2),
            "currentPrice": round(current_price, 2),
            "currentValue": round(current_value, 2),
            "invested":     round(invested, 2),
            "pnl":          round(pnl, 2),
            "pnlPct":       pnl_pct,
            "dayChangePct": day_change_pct,
            "trend":        "up" if pnl_pct > 0 else "down",
            "transactions": len(txns),
        })

        total_value    += current_value
        total_invested += invested

    total_pnl     = total_value - total_invested
    total_pnl_pct = round(total_pnl / total_invested * 100, 2) if total_invested > 0 else 0

    # Sector allocation (simplified)
    sector_map = {
        "RELIANCE": "Energy", "TCS": "IT", "INFY": "IT", "WIPRO": "IT",
        "HDFCBANK": "Banking", "ICICIBANK": "Banking", "SBIN": "Banking",
        "TATAMOTORS": "Auto",
    }
    sector_alloc: Dict[str, float] = {}
    for h in holdings:
        sector = sector_map.get(h["symbol"], "Others")
        sector_alloc[sector] = sector_alloc.get(sector, 0) + h["currentValue"]

    sector_breakdown = [
        {"sector": k, "value": round(v), "pct": round(v / total_value * 100, 1) if total_value > 0 else 0}
        for k, v in sorted(sector_alloc.items(), key=lambda x: -x[1])
    ]

    return {
        "holdings":        sorted(holdings, key=lambda x: -x["currentValue"]),
        "totalValue":      round(total_value, 2),
        "totalInvested":   round(total_invested, 2),
        "totalPnL":        round(total_pnl, 2),
        "totalPnLPct":     total_pnl_pct,
        "sectorBreakdown": sector_breakdown,
        "holdingsCount":   len(holdings),
    }


def compute_mutual_funds(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process mutual fund transaction data into portfolio summary."""
    mf_data = financial_data.get("fetch_mf_transactions", {})
    schemes = mf_data.get("mfTransactions", [])

    # Also get current values from net worth data
    nw_data    = financial_data.get("fetch_net_worth", {})
    mf_schemes = nw_data.get("mfSchemeAnalytics", {}).get("schemeAnalytics", [])

    # Build a lookup from net worth data
    nw_lookup: Dict[str, Dict] = {}
    for s in mf_schemes:
        isin = s.get("schemeDetail", {}).get("isinNumber", "")
        if isin:
            analytics = s.get("enrichedAnalytics", {}).get("analytics", {}).get("schemeDetails", {})
            nw_lookup[isin] = {
                "currentValue":  float(analytics.get("currentValue", {}).get("units", 0)),
                "investedValue": float(analytics.get("investedValue", {}).get("units", 0)),
                "xirr":          analytics.get("XIRR", 0),
                "longName":      s.get("schemeDetail", {}).get("nameData", {}).get("longName", ""),
                "assetClass":    s.get("schemeDetail", {}).get("assetClass", ""),
                "riskLevel":     s.get("schemeDetail", {}).get("fundhouseDefinedRiskLevel", ""),
            }

    holdings = []
    total_current  = 0
    total_invested = 0

    for scheme in schemes:
        isin       = scheme.get("isin", "")
        name       = scheme.get("schemeName", "Unknown Fund")
        txns       = scheme.get("txns", [])
        folio      = scheme.get("folioId", "")

        buy_txns  = [t for t in txns if t[0] == 1]
        sell_txns = [t for t in txns if t[0] == 2]

        total_units    = sum(t[3] for t in buy_txns) - sum(t[3] for t in sell_txns)
        total_invested_scheme = sum(t[4] for t in buy_txns) - sum(t[4] for t in sell_txns)

        # Use net worth data if available, else estimate
        if isin in nw_lookup:
            nw = nw_lookup[isin]
            current_value  = nw["currentValue"]
            invested_value = nw["investedValue"]
            xirr           = nw["xirr"]
            asset_class    = nw["assetClass"]
            risk_level     = nw["riskLevel"].replace("_RISK", "").replace("_TO_", "-").replace("_", " ").title()
        else:
            # Estimate from transactions
            last_nav       = buy_txns[-1][2] if buy_txns else 0
            current_nav    = last_nav * 1.08  # assume 8% growth
            current_value  = total_units * current_nav
            invested_value = total_invested_scheme
            xirr           = 8.0
            asset_class    = "DEBT"
            risk_level     = "Moderate"

        pnl     = current_value - invested_value
        pnl_pct = round(pnl / invested_value * 100, 2) if invested_value > 0 else 0

        # SIP details
        sip_months = len(buy_txns)
        monthly_sip = round(total_invested_scheme / sip_months) if sip_months > 0 else 0

        holdings.append({
            "isin":          isin,
            "schemeName":    name,
            "folioId":       folio,
            "assetClass":    asset_class,
            "riskLevel":     risk_level,
            "totalUnits":    round(total_units, 2),
            "currentValue":  round(current_value, 2),
            "investedValue": round(invested_value, 2),
            "pnl":           round(pnl, 2),
            "pnlPct":        pnl_pct,
            "xirr":          xirr,
            "monthlySIP":    monthly_sip,
            "sipMonths":     sip_months,
            "trend":         "up" if pnl_pct > 0 else "down",
        })

        total_current  += current_value
        total_invested += invested_value

    total_pnl     = total_current - total_invested
    total_pnl_pct = round(total_pnl / total_invested * 100, 2) if total_invested > 0 else 0
    avg_xirr      = round(sum(h["xirr"] for h in holdings) / len(holdings), 2) if holdings else 0

    # Asset class breakdown
    asset_alloc: Dict[str, float] = {}
    for h in holdings:
        ac = h["assetClass"] or "OTHER"
        asset_alloc[ac] = asset_alloc.get(ac, 0) + h["currentValue"]

    asset_breakdown = [
        {"assetClass": k, "value": round(v), "pct": round(v / total_current * 100, 1) if total_current > 0 else 0}
        for k, v in sorted(asset_alloc.items(), key=lambda x: -x[1])
    ]

    return {
        "holdings":       sorted(holdings, key=lambda x: -x["currentValue"]),
        "totalValue":     round(total_current, 2),
        "totalInvested":  round(total_invested, 2),
        "totalPnL":       round(total_pnl, 2),
        "totalPnLPct":    total_pnl_pct,
        "avgXIRR":        avg_xirr,
        "assetBreakdown": asset_breakdown,
        "schemesCount":   len(holdings),
    }
