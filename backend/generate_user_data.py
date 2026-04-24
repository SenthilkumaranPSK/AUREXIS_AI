"""
AUREXIS AI — User Data Generator
Generates rich, realistic financial data for all 12 users.
Run once: python generate_user_data.py
"""

import json
import random
import os
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent / "user_data"

# ── User profiles ──────────────────────────────────────────────────────────────
USERS = [
    {"id": "1010101010", "name": "Senthilkumaran", "age": 24, "occupation": "Software Engineer",   "income": 78000,  "city": "Salem",      "credit_score": 788, "risk": "Moderate"},
    {"id": "1111111111", "name": "Imayavarman",    "age": 32, "occupation": "Doctor",              "income": 150000, "city": "Erode",      "credit_score": 810, "risk": "Low"},
    {"id": "1212121212", "name": "Srivarshan",     "age": 40, "occupation": "Business Owner",      "income": 250000, "city": "Theni",      "credit_score": 742, "risk": "High"},
    {"id": "1313131313", "name": "Rahulprasath",   "age": 30, "occupation": "Teacher",             "income": 45000,  "city": "Omalur",     "credit_score": 720, "risk": "Low"},
    {"id": "1414141414", "name": "Magudesh",       "age": 28, "occupation": "Freelancer",          "income": 55000,  "city": "Bangalore",  "credit_score": 695, "risk": "Moderate"},
    {"id": "2020202020", "name": "Deepak",         "age": 29, "occupation": "CA",                  "income": 90000,  "city": "Chennai",    "credit_score": 801, "risk": "Low"},
    {"id": "2121212121", "name": "Mani",           "age": 38, "occupation": "Government Employee", "income": 60000,  "city": "Edapadi",    "credit_score": 755, "risk": "Low"},
    {"id": "2222222222", "name": "Dineshkumar",    "age": 52, "occupation": "Lawyer",              "income": 120000, "city": "Sangagari",  "credit_score": 768, "risk": "Moderate"},
    {"id": "2525252525", "name": "Avinash",        "age": 28, "occupation": "IPS",                 "income": 70000,  "city": "Ambur",      "credit_score": 780, "risk": "Low"},
    {"id": "3333333333", "name": "Kumar",          "age": 23, "occupation": "Content Creator",     "income": 35000,  "city": "Coimbatore", "credit_score": 660, "risk": "High"},
    {"id": "4444444444", "name": "Hari",           "age": 44, "occupation": "Startup Founder",     "income": 200000, "city": "Karur",      "credit_score": 730, "risk": "High"},
    {"id": "5555555555", "name": "Janakrishnan",   "age": 22, "occupation": "Government Employee", "income": 38000,  "city": "Rasipuram",  "credit_score": 710, "risk": "Low"},
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def rand(base, pct=0.15):
    """Random variation around base value."""
    return int(base * (1 + random.uniform(-pct, pct)))

def date_range(months_back=12):
    """Generate list of (year, month) tuples going back N months."""
    today = datetime.now()
    result = []
    for i in range(months_back, 0, -1):
        d = today - timedelta(days=30 * i)
        result.append((d.year, d.month))
    return result

def fmt_date(year, month, day):
    return f"{year}-{month:02d}-{day:02d}"

def month_name(month):
    return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][month-1]

# ── Bank Transactions ──────────────────────────────────────────────────────────

def make_bank_transactions(user):
    income = user["income"]
    city   = user["city"]
    name   = user["name"]
    occ    = user["occupation"]

    # Expense ratios based on occupation
    expense_ratio = {
        "Software Engineer": 0.55, "Doctor": 0.45, "Business Owner": 0.60,
        "Teacher": 0.65, "Freelancer": 0.60, "CA": 0.50,
        "Government Employee": 0.55, "Lawyer": 0.50, "IPS": 0.50,
        "Content Creator": 0.70, "Startup Founder": 0.65,
    }.get(occ, 0.55)

    txns = []
    months = date_range(12)

    for year, month in months:
        base_expense = income * expense_ratio
        salary_day   = 1
        rent_day     = 2
        sip_day      = 5
        cc_day       = 10
        misc_days    = [15, 20, 25, 28]

        # Salary credit
        txns.append([str(rand(income, 0.02)), f"SALARY CREDIT - {name.upper()} - {month_name(month)} {year}", fmt_date(year, month, salary_day), 1, "NEFT", str(rand(income * 3))])

        # Rent
        rent = int(income * 0.22)
        txns.append([str(rent), f"IMPS-LANDLORD-{month_name(month)} RENT-{city.upper()}", fmt_date(year, month, rent_day), 2, "FT", str(rand(income * 2.5))])

        # SIP
        sip_amt = int(income * 0.08)
        txns.append([str(sip_amt), f"ACH D-MUTUALFUND-SIP/{year}{month:02d}{sip_day:02d}/MF{random.randint(10000,99999)}", fmt_date(year, month, sip_day), 6, "ACH", str(rand(income * 2))])

        # RD / Insurance
        rd_amt = int(income * 0.05)
        txns.append([str(rd_amt), f"AUTO DEBIT - RD INSTALLMENT A/C XXXXXX{random.randint(1000,9999)}", fmt_date(year, month, sip_day), 6, "ACH", str(rand(income * 1.8))])

        # Credit card bill
        cc_amt = int(base_expense * 0.20)
        txns.append([str(cc_amt), f"CREDIT CARD BILL PAYMENT-XXXXXXXX{random.randint(1000,9999)}", fmt_date(year, month, cc_day), 2, "CARD_PAYMENT", str(rand(income * 1.5))])

        # Groceries
        txns.append([str(rand(2500, 0.3)), f"UPI-GROCER-GROCERIES@UPI-{city.upper()}", fmt_date(year, month, 15), 2, "UPI", str(rand(income * 1.3))])

        # Utilities
        txns.append([str(rand(1800, 0.2)), f"BESCOM/TNEB ELECTRICITY BILL-{month_name(month)}{year}", fmt_date(year, month, 18), 2, "BILLPAY", str(rand(income * 1.2))])

        # Mobile/Internet
        txns.append([str(rand(800, 0.1)), f"AIRTEL/JIO RECHARGE-{name.upper()}", fmt_date(year, month, 20), 2, "UPI", str(rand(income * 1.1))])

        # Fuel / Transport
        txns.append([str(rand(2200, 0.25)), f"UPI-PETROL BUNK-FUEL@UPI-{city.upper()}", fmt_date(year, month, 22), 2, "UPI", str(rand(income * 1.0))])

        # Dining / Entertainment
        txns.append([str(rand(1500, 0.4)), f"SWIGGY/ZOMATO-FOOD ORDER-{name.upper()}", fmt_date(year, month, 25), 2, "UPI", str(rand(income * 0.9))])

        # FD interest (quarterly)
        if month in [3, 6, 9, 12]:
            fd_interest = int(income * 0.5 * 0.07 / 4)
            txns.append([str(fd_interest), f"QTRLY INTEREST CREDIT ON FD A/C XXXXXX{random.randint(1000,9999)}", fmt_date(year, month, 15), 4, "INTEREST", str(rand(income * 3.5))])

        # Occasional large expense (medical, travel etc.)
        if random.random() < 0.3:
            large_amt = rand(int(income * 0.15), 0.3)
            categories = ["MEDICAL EXPENSE", "TRAVEL BOOKING", "ONLINE SHOPPING", "HOME MAINTENANCE", "INSURANCE PREMIUM"]
            txns.append([str(large_amt), f"UPI-{random.choice(categories)}-{name.upper()}", fmt_date(year, month, 28), 2, "UPI", str(rand(income * 0.8))])

    return {
        "schemaDescription": "Bank transactions. txns schema: [amount, narration, date, type(1=CREDIT,2=DEBIT,4=INTEREST,6=INSTALLMENT), mode, balance]",
        "bankTransactions": [{"bank": "State Bank of India", "txns": txns}]
    }

# ── Net Worth ──────────────────────────────────────────────────────────────────

def make_net_worth(user):
    income = user["income"]
    age    = user["age"]

    # Wealth accumulation based on age and income
    years_working = max(1, age - 22)
    savings_factor = years_working * income * 0.15

    mf_value      = int(savings_factor * 0.30)
    epf_value     = int(savings_factor * 0.25)
    fd_value      = int(savings_factor * 0.20)
    savings_value = int(income * 3)
    etf_value     = int(savings_factor * 0.10)
    rd_value      = int(savings_factor * 0.05)
    total         = mf_value + epf_value + fd_value + savings_value + etf_value + rd_value

    return {
        "netWorthResponse": {
            "assetValues": [
                {"netWorthAttribute": "ASSET_TYPE_MUTUAL_FUND",      "value": {"currencyCode": "INR", "units": str(mf_value)}},
                {"netWorthAttribute": "ASSET_TYPE_EPF",              "value": {"currencyCode": "INR", "units": str(epf_value)}},
                {"netWorthAttribute": "ASSET_TYPE_DEPOSITS",         "value": {"currencyCode": "INR", "units": str(fd_value)}},
                {"netWorthAttribute": "ASSET_TYPE_ETF",              "value": {"currencyCode": "INR", "units": str(etf_value)}},
                {"netWorthAttribute": "ASSET_TYPE_SAVINGS_ACCOUNTS", "value": {"currencyCode": "INR", "units": str(savings_value)}},
                {"netWorthAttribute": "ASSET_TYPE_RECURRING_DEPOSIT","value": {"currencyCode": "INR", "units": str(rd_value)}},
            ],
            "totalNetWorthValue": {"currencyCode": "INR", "units": str(total)}
        }
    }

# ── Credit Report ──────────────────────────────────────────────────────────────

def make_credit_report(user):
    score = user["credit_score"]
    income = user["income"]

    cc_limit1 = int(income * 1.5)
    cc_limit2 = int(income * 1.0)
    cc_bal1   = int(cc_limit1 * 0.15)
    cc_bal2   = int(cc_limit2 * 0.12)

    return {
        "creditReports": [{
            "creditReportData": {
                "creditProfileHeader": {
                    "reportDate": datetime.now().strftime("%Y%m%d"),
                    "reportTime": datetime.now().strftime("%H%M%S"),
                },
                "creditAccount": {
                    "creditAccountSummary": {
                        "account": {
                            "creditAccountTotal": "3",
                            "creditAccountActive": "2",
                            "creditAccountDefault": "0",
                            "creditAccountClosed": "1",
                        },
                        "totalOutstandingBalance": {
                            "outstandingBalanceUnSecured": str(cc_bal1 + cc_bal2),
                            "outstandingBalanceAll": str(cc_bal1 + cc_bal2),
                        }
                    },
                    "creditAccountDetails": [
                        {
                            "subscriberName": "SBI Card",
                            "portfolioType": "R",
                            "accountType": "10",
                            "openDate": f"{user['age'] - 4}0101".replace(str(user['age'] - 4), str(datetime.now().year - 4)),
                            "creditLimitAmount": str(cc_limit1),
                            "currentBalance": str(cc_bal1),
                            "amountPastDue": "0",
                            "paymentHistoryProfile": "0" * 36,
                            "rateOfInterest": "20.0",
                            "accountStatus": "11",
                        },
                        {
                            "subscriberName": "HDFC Bank",
                            "portfolioType": "R",
                            "accountType": "10",
                            "openDate": f"{datetime.now().year - 2}0601",
                            "creditLimitAmount": str(cc_limit2),
                            "currentBalance": str(cc_bal2),
                            "amountPastDue": "0",
                            "paymentHistoryProfile": "0" * 24,
                            "rateOfInterest": "21.5",
                            "accountStatus": "11",
                        }
                    ]
                },
                "score": {
                    "bureauScore": str(score),
                    "bureauScoreConfidenceLevel": "H" if score >= 750 else "M",
                },
                "totalCapsSummary": {
                    "totalCapsLast7Days": "0", "totalCapsLast30Days": "1",
                    "totalCapsLast90Days": "2", "totalCapsLast180Days": "3",
                }
            },
            "vendor": "EXPERIAN"
        }]
    }

# ── EPF Details ────────────────────────────────────────────────────────────────

def make_epf_details(user):
    income = user["income"]
    age    = user["age"]
    years  = max(1, age - 22)

    employee_contrib = int(income * 0.12 * 12 * years)
    employer_contrib = int(income * 0.12 * 12 * years * 0.9)
    interest         = int((employee_contrib + employer_contrib) * 0.08 * years / 2)
    total            = employee_contrib + employer_contrib + interest

    return {
        "epfDetails": {
            "uanNumber": f"10{user['id'][:8]}",
            "memberName": user["name"],
            "dateOfJoining": f"{datetime.now().year - years}-04-01",
            "establishmentName": f"{user['occupation']} Organization",
            "employeeContribution": employee_contrib,
            "employerContribution": employer_contrib,
            "interestEarned": interest,
            "totalBalance": total,
            "lastContributionMonth": datetime.now().strftime("%Y-%m"),
            "monthlyContribution": int(income * 0.12),
        }
    }

# ── MF Transactions ────────────────────────────────────────────────────────────

MF_SCHEMES = [
    {"isin": "INF179KB1HS3", "name": "Nippon India Corporate Bond Fund - Direct Growth",    "nav_base": 21.5,  "asset": "DEBT",     "risk": "MODERATE_RISK"},
    {"isin": "INF174V01BL6", "name": "Axis Treasury Advantage Fund - Direct Growth",        "nav_base": 128.0, "asset": "DEBT",     "risk": "LOW_TO_MODERATE_RISK"},
    {"isin": "INF209K01YY1", "name": "UTI Money Market Fund - Direct Growth",               "nav_base": 3300,  "asset": "DEBT",     "risk": "LOW_TO_MODERATE_RISK"},
    {"isin": "INF204KB17I9", "name": "HDFC Gold ETF",                                       "nav_base": 58.0,  "asset": "COMMODITY","risk": "HIGH_RISK"},
    {"isin": "INF179K01844", "name": "HDFC Gold Fund - Direct Plan - Growth",               "nav_base": 20.5,  "asset": "COMMODITY","risk": "HIGH_RISK"},
    {"isin": "INF109K01XO3", "name": "ICICI Prudential Short Term Debt Fund - Direct Growth","nav_base": 54.5, "asset": "DEBT",     "risk": "LOW_TO_MODERATE_RISK"},
    {"isin": "INF174K01BU9", "name": "Kotak Equity Arbitrage Fund - Direct Growth",         "nav_base": 32.9,  "asset": "HYBRID",   "risk": "LOW_TO_MODERATE_RISK"},
    {"isin": "INF846K01EW2", "name": "Axis Bluechip Fund - Direct Growth",                  "nav_base": 55.0,  "asset": "EQUITY",   "risk": "HIGH_RISK"},
    {"isin": "INF200K01RO2", "name": "SBI Nifty Index Fund - Direct Growth",                "nav_base": 180.0, "asset": "EQUITY",   "risk": "HIGH_RISK"},
]

def make_mf_transactions(user):
    income = user["income"]
    sip_amt = int(income * 0.08)

    # Pick 2-4 schemes based on income
    num_schemes = 2 if income < 50000 else 3 if income < 100000 else 4
    schemes = random.sample(MF_SCHEMES, num_schemes)

    mf_txns = []
    months = date_range(18)  # 18 months of SIP history

    for scheme in schemes:
        txns = []
        nav = scheme["nav_base"]
        per_scheme_sip = sip_amt // num_schemes

        for year, month in months:
            nav = nav * (1 + random.uniform(0.003, 0.012))  # slight NAV growth
            units = round(per_scheme_sip / nav, 2)
            txns.append([1, fmt_date(year, month, 5), round(nav, 2), units, per_scheme_sip])

        mf_txns.append({
            "isin": scheme["isin"],
            "schemeName": scheme["name"],
            "folioId": f"AU-{random.randint(100000, 999999)}",
            "txns": txns
        })

    return {
        "mfTransactions": mf_txns,
        "schemaDescription": "MF transactions. txns: [orderType(1=BUY,2=SELL), date, nav, units, amount]"
    }

# ── Stock Transactions ─────────────────────────────────────────────────────────

STOCKS = [
    {"symbol": "RELIANCE",  "name": "Reliance Industries Ltd",  "price_base": 2800},
    {"symbol": "TCS",       "name": "Tata Consultancy Services", "price_base": 3900},
    {"symbol": "INFY",      "name": "Infosys Ltd",               "price_base": 1700},
    {"symbol": "HDFCBANK",  "name": "HDFC Bank Ltd",             "price_base": 1650},
    {"symbol": "WIPRO",     "name": "Wipro Ltd",                 "price_base": 480},
    {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd",            "price_base": 1100},
    {"symbol": "SBIN",      "name": "State Bank of India",       "price_base": 820},
    {"symbol": "TATAMOTORS","name": "Tata Motors Ltd",           "price_base": 950},
]

def make_stock_transactions(user):
    income = user["income"]

    # Only higher income users have stocks
    if income < 50000:
        return {"stockTransactions": [], "schemaDescription": "Stock transactions"}

    num_stocks = 2 if income < 80000 else 3 if income < 150000 else 5
    selected = random.sample(STOCKS, min(num_stocks, len(STOCKS)))

    stock_txns = []
    months = date_range(12)

    for stock in selected:
        price = stock["price_base"]
        qty   = max(1, int(income * 0.05 / price))
        txns  = []

        # Buy transactions over time
        for i, (year, month) in enumerate(months):
            if random.random() < 0.4:  # buy in ~40% of months
                price = price * (1 + random.uniform(-0.03, 0.05))
                txns.append({
                    "type": "BUY",
                    "date": fmt_date(year, month, random.randint(5, 25)),
                    "symbol": stock["symbol"],
                    "quantity": qty,
                    "price": round(price, 2),
                    "amount": round(price * qty, 2),
                })

        if txns:
            current_price = price * (1 + random.uniform(0.05, 0.20))
            total_qty = sum(t["quantity"] for t in txns if t["type"] == "BUY")
            stock_txns.append({
                "symbol":       stock["symbol"],
                "companyName":  stock["name"],
                "exchange":     "NSE",
                "currentPrice": round(current_price, 2),
                "totalQuantity": total_qty,
                "currentValue": round(current_price * total_qty, 2),
                "transactions": txns,
            })

    return {
        "stockTransactions": stock_txns,
        "schemaDescription": "Stock transactions with buy/sell history"
    }

# ── Profile ────────────────────────────────────────────────────────────────────

def make_profile(user):
    return {
        "user_id":              user["id"],
        "name":                 user["name"],
        "occupation":           user["occupation"],
        "age":                  user["age"],
        "monthly_income":       user["income"],
        "city":                 user["city"],
        "risk_profile":         user["risk"],
        "financial_goals":      ["Emergency Fund", "Retirement Planning", "Investment Growth"],
        "dependents":           random.randint(0, 3),
        "marital_status":       "Married" if user["age"] > 28 else "Single",
        "investment_preference": "Equity and Mutual Funds" if user["risk"] == "High" else "Debt and FD",
    }

# ── Main Generator ─────────────────────────────────────────────────────────────

def generate_all():
    random.seed(42)  # reproducible data
    generated = 0

    for user in USERS:
        user_dir = BASE_DIR / user["id"]
        user_dir.mkdir(parents=True, exist_ok=True)

        files = {
            "fetch_bank_transactions.json": make_bank_transactions(user),
            "fetch_net_worth.json":         make_net_worth(user),
            "fetch_credit_report.json":     make_credit_report(user),
            "fetch_epf_details.json":       make_epf_details(user),
            "fetch_mf_transactions.json":   make_mf_transactions(user),
            "fetch_stock_transactions.json":make_stock_transactions(user),
            "profile.json":                 make_profile(user),
        }

        for filename, data in files.items():
            path = user_dir / filename
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

        txn_count = len(data.get("bankTransactions", [{}])[0].get("txns", [])) if "bankTransactions" in files["fetch_bank_transactions.json"] else 0
        print(f"✅ {user['name']:20s} ({user['id']}) — {len(files)} files, ~{len(files['fetch_bank_transactions.json']['bankTransactions'][0]['txns'])} transactions")
        generated += 1

    print(f"\n🎉 Generated data for {generated} users in backend/user_data/")


if __name__ == "__main__":
    generate_all()
