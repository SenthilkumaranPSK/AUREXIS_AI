"""
Test script for all new features:
- Credit Score Prediction
- Tax Planning
- Fraud Detection
- Real-time Alerts
"""

import json
from user_manager import get_all_user_data
from credit_score_predictor import credit_score_predictor
from tax_planner import tax_planner
from fraud_detector import fraud_detector
from realtime_alerts import realtime_alert_system

print("=" * 80)
print("🚀 AUREXIS AI - New Features Demo")
print("=" * 80)
print()

# Load sample user data
user_id = "1010101010"
financial_data = get_all_user_data(user_id)

# TEST 1: Credit Score Prediction
print("📊 TEST 1: Credit Score Prediction")
print("-" * 80)
credit_prediction = credit_score_predictor.predict_credit_score(financial_data)
print(f"Current Score: {credit_prediction['current_score']}")
print(f"Predicted Score: {credit_prediction['predicted_score']}")
print(f"Trend: {credit_prediction['trend']}")
print(f"Score Range: {credit_prediction['score_range']}")
print(f"\nTop Recommendations:")
for rec in credit_prediction['recommendations'][:3]:
    print(f"  • [{rec['priority'].upper()}] {rec['action']}")
    print(f"    Impact: {rec['impact']} in {rec['timeline']}")
print()

# TEST 2: Tax Planning
print("💰 TEST 2: Tax Planning & Optimization")
print("-" * 80)

# Calculate tax for different incomes
annual_income = 1200000  # 12 LPA

# New regime
new_regime = tax_planner.calculate_tax_liability(annual_income, regime="new")
print(f"Annual Income: ₹{annual_income:,.0f}")
print(f"\nNEW REGIME:")
print(f"  Tax: ₹{new_regime['total_tax']:,.0f}")
print(f"  Effective Rate: {new_regime['effective_tax_rate']}%")
print(f"  Take Home: ₹{new_regime['take_home_annual']:,.0f}/year")

# Old regime with deductions
deductions = {
    "80C": 150000,
    "80D": 25000,
    "NPS": 50000
}
old_regime = tax_planner.calculate_tax_liability(annual_income, regime="old", deductions=deductions)
print(f"\nOLD REGIME (with deductions):")
print(f"  Tax: ₹{old_regime['total_tax']:,.0f}")
print(f"  Effective Rate: {old_regime['effective_tax_rate']}%")
print(f"  Take Home: ₹{old_regime['take_home_annual']:,.0f}/year")

savings = old_regime['total_tax'] - new_regime['total_tax']
print(f"\n💡 Savings: ₹{abs(savings):,.0f} with {'NEW' if savings > 0 else 'OLD'} regime")

# Tax-saving investment suggestions
print(f"\n📈 Tax-Saving Investment Suggestions:")
suggestions = tax_planner.suggest_tax_saving_investments(
    annual_income=annual_income,
    current_investments={"80C": 50000, "80D": 0, "NPS": 0},
    risk_profile="moderate"
)
for rec in suggestions['recommendations']:
    print(f"  • {rec['instrument']} ({rec['section']})")
    print(f"    Invest: ₹{rec['amount']:,.0f} → Save Tax: ₹{rec['tax_saved']:,.0f}")
print()

# TEST 3: Fraud Detection
print("🔒 TEST 3: Fraud Detection")
print("-" * 80)

# Analyze a suspicious transaction
suspicious_txn = {
    "id": "txn_12345",
    "amount": -95000,
    "type": "debit",
    "category": "Shopping",
    "description": "Crypto Exchange",
    "location": "International",
    "date": "2026-04-20T03:30:00"
}

transactions = financial_data.get("fetch_bank_transactions", {}).get("transactions", [])
fraud_analysis = fraud_detector.analyze_transaction(
    transaction=suspicious_txn,
    user_history=transactions,
    user_profile={"name": "Test User"}
)

print(f"Transaction: ₹{abs(suspicious_txn['amount']):,.0f} - {suspicious_txn['description']}")
print(f"Risk Score: {fraud_analysis['risk_score']} ({fraud_analysis['risk_level'].upper()})")
print(f"Recommended Action: {fraud_analysis['recommended_action'].upper()}")
print(f"Is Fraudulent: {'YES ⚠️' if fraud_analysis['is_fraudulent'] else 'NO ✓'}")
print(f"\nRisk Factors:")
for factor in fraud_analysis['risk_factors'][:5]:
    print(f"  • [{factor['severity'].upper()}] {factor['factor']}")
    print(f"    {factor['description']}")

# Generate fraud report
print(f"\n📋 Fraud Report Summary:")
fraud_report = fraud_detector.generate_fraud_report(transactions, {"name": "Test User"})
print(f"  Total Transactions: {fraud_report['summary']['total_transactions']}")
print(f"  Flagged: {fraud_report['summary']['flagged_transactions']}")
print(f"  Overall Risk: {fraud_report['summary']['overall_risk_score']}")
print(f"  Risk Distribution: {fraud_report['summary']['risk_distribution']}")
print()

# TEST 4: Real-time Alerts
print("🔔 TEST 4: Real-time Alerts")
print("-" * 80)

alerts = realtime_alert_system.generate_realtime_alerts(
    financial_data=financial_data,
    user_profile={"name": "Test User"}
)

print(f"Total Alerts: {len(alerts)}")
print(f"\nTop Alerts:")
for alert in alerts[:5]:
    icon = alert.get('icon', '📌')
    priority = alert['priority'].upper()
    print(f"\n{icon} [{priority}] {alert['title']}")
    print(f"   {alert['message']}")
    if alert.get('action_required'):
        print(f"   ⚠️ Action Required!")

# Alert summary
summary = realtime_alert_system.get_alert_summary(alerts)
print(f"\n📊 Alert Summary:")
print(f"  Critical: {summary['priority_breakdown']['critical']}")
print(f"  High: {summary['priority_breakdown']['high']}")
print(f"  Medium: {summary['priority_breakdown']['medium']}")
print(f"  Low: {summary['priority_breakdown']['low']}")
print(f"  Action Required: {summary['action_required']}")
print()

print("=" * 80)
print("✅ All tests completed successfully!")
print("=" * 80)
print()
print("🎯 NEW FEATURES SUMMARY:")
print()
print("1. 📊 CREDIT SCORE PREDICTION")
print("   • ML-based score prediction")
print("   • Improvement recommendations")
print("   • Timeline to excellent credit")
print("   • Risk & positive factor analysis")
print()
print("2. 💰 TAX PLANNING")
print("   • New vs Old regime comparison")
print("   • Tax-saving investment suggestions")
print("   • Advance tax calculation")
print("   • Tax efficiency analysis")
print()
print("3. 🔒 FRAUD DETECTION")
print("   • Real-time transaction analysis")
print("   • ML-powered risk scoring")
print("   • Account takeover detection")
print("   • Comprehensive fraud reports")
print()
print("4. 🔔 REAL-TIME ALERTS")
print("   • Transaction alerts")
print("   • Balance warnings")
print("   • Bill payment reminders")
print("   • Goal milestone notifications")
print("   • Investment performance alerts")
print()
print("📡 NEW API ENDPOINTS:")
print()
print("Credit Score:")
print("  GET  /api/user/{user_id}/credit-score/predict")
print()
print("Tax Planning:")
print("  POST /api/tax/calculate")
print("  POST /api/tax/compare-regimes")
print("  GET  /api/user/{user_id}/tax/analyze")
print("  POST /api/tax/investment-suggestions")
print("  POST /api/tax/advance-tax")
print()
print("Fraud Detection:")
print("  POST /api/fraud/analyze-transaction")
print("  GET  /api/user/{user_id}/fraud/report")
print("  GET  /api/user/{user_id}/fraud/account-takeover")
print()
print("Real-time Alerts:")
print("  GET  /api/user/{user_id}/alerts/realtime")
print()
