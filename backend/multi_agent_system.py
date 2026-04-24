"""
AUREXIS AI — Multi-Agent Workflow System
Coordinated AI agents for specialized financial tasks
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging
from enum import Enum

logger = logging.getLogger("aurexis")


class AgentRole(Enum):
    """Different agent roles in the system"""
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    ADVISOR = "advisor"
    PLANNER = "planner"
    MONITOR = "monitor"
    EXECUTOR = "executor"


class Agent:
    """Base agent class"""
    
    def __init__(self, role: AgentRole, name: str, capabilities: List[str]):
        self.role = role
        self.name = name
        self.capabilities = capabilities
        self.memory: List[Dict] = []
        self.status = "idle"
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task"""
        self.status = "working"
        logger.info(f"Agent {self.name} processing task: {task.get('type')}")
        
        result = await self._execute_task(task)
        
        self.status = "idle"
        self.memory.append({
            "task": task,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Override in subclasses"""
        raise NotImplementedError


class AnalystAgent(Agent):
    """Agent specialized in financial analysis"""
    
    def __init__(self):
        super().__init__(
            role=AgentRole.ANALYST,
            name="Financial Analyst",
            capabilities=[
                "spending_analysis",
                "income_analysis",
                "trend_detection",
                "anomaly_detection",
                "pattern_recognition"
            ]
        )
    
    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial data"""
        task_type = task.get("type")
        data = task.get("data", {})
        
        if task_type == "spending_analysis":
            return await self._analyze_spending(data)
        elif task_type == "income_analysis":
            return await self._analyze_income(data)
        elif task_type == "trend_detection":
            return await self._detect_trends(data)
        elif task_type == "anomaly_detection":
            return await self._detect_anomalies(data)
        
        return {"status": "unknown_task", "message": f"Unknown task type: {task_type}"}
    
    async def _analyze_spending(self, data: Dict) -> Dict:
        """Analyze spending patterns"""
        transactions = data.get("transactions", [])
        
        # Calculate spending by category
        category_spending = {}
        total_spending = 0
        
        for txn in transactions:
            if txn.get("type") == "debit":
                category = txn.get("category", "Other")
                amount = abs(float(txn.get("amount", 0)))
                category_spending[category] = category_spending.get(category, 0) + amount
                total_spending += amount
        
        # Find top categories
        top_categories = sorted(
            category_spending.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "status": "success",
            "analysis": {
                "total_spending": round(total_spending, 2),
                "category_breakdown": category_spending,
                "top_categories": [
                    {"category": cat, "amount": amt, "percentage": round(amt/total_spending*100, 1)}
                    for cat, amt in top_categories
                ],
                "insights": self._generate_spending_insights(category_spending, total_spending)
            }
        }
    
    async def _analyze_income(self, data: Dict) -> Dict:
        """Analyze income patterns"""
        transactions = data.get("transactions", [])
        
        total_income = 0
        income_sources = {}
        
        for txn in transactions:
            if txn.get("type") == "credit":
                source = txn.get("category", "Other")
                amount = float(txn.get("amount", 0))
                income_sources[source] = income_sources.get(source, 0) + amount
                total_income += amount
        
        return {
            "status": "success",
            "analysis": {
                "total_income": round(total_income, 2),
                "income_sources": income_sources,
                "primary_source": max(income_sources.items(), key=lambda x: x[1])[0] if income_sources else "None",
                "income_stability": "stable" if len(income_sources) <= 2 else "variable"
            }
        }
    
    async def _detect_trends(self, data: Dict) -> Dict:
        """Detect financial trends"""
        transactions = data.get("transactions", [])
        
        # Group by month
        monthly_data = {}
        for txn in transactions:
            date = txn.get("date", "")[:7]  # YYYY-MM
            if date not in monthly_data:
                monthly_data[date] = {"income": 0, "expense": 0}
            
            amount = float(txn.get("amount", 0))
            if txn.get("type") == "credit":
                monthly_data[date]["income"] += amount
            else:
                monthly_data[date]["expense"] += abs(amount)
        
        # Calculate trends
        months = sorted(monthly_data.keys())
        if len(months) >= 2:
            recent = monthly_data[months[-1]]
            previous = monthly_data[months[-2]]
            
            income_trend = "increasing" if recent["income"] > previous["income"] else "decreasing"
            expense_trend = "increasing" if recent["expense"] > previous["expense"] else "decreasing"
        else:
            income_trend = "stable"
            expense_trend = "stable"
        
        return {
            "status": "success",
            "trends": {
                "income_trend": income_trend,
                "expense_trend": expense_trend,
                "monthly_data": monthly_data
            }
        }
    
    async def _detect_anomalies(self, data: Dict) -> Dict:
        """Detect anomalies in transactions"""
        transactions = data.get("transactions", [])
        
        # Calculate average transaction amount
        amounts = [abs(float(t.get("amount", 0))) for t in transactions if t.get("type") == "debit"]
        if not amounts:
            return {"status": "success", "anomalies": []}
        
        avg_amount = sum(amounts) / len(amounts)
        std_dev = (sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)) ** 0.5
        
        # Find anomalies (> 2 standard deviations)
        anomalies = []
        for txn in transactions:
            if txn.get("type") == "debit":
                amount = abs(float(txn.get("amount", 0)))
                if amount > avg_amount + (2 * std_dev):
                    anomalies.append({
                        "transaction": txn,
                        "amount": amount,
                        "deviation": round((amount - avg_amount) / std_dev, 2)
                    })
        
        return {
            "status": "success",
            "anomalies": anomalies,
            "threshold": round(avg_amount + (2 * std_dev), 2)
        }
    
    def _generate_spending_insights(self, category_spending: Dict, total: float) -> List[str]:
        """Generate insights from spending data"""
        insights = []
        
        # Check for high spending categories
        for category, amount in category_spending.items():
            percentage = (amount / total * 100) if total > 0 else 0
            if percentage > 30:
                insights.append(f"{category} accounts for {percentage:.1f}% of spending - consider reviewing")
        
        return insights


class AdvisorAgent(Agent):
    """Agent specialized in financial advice"""
    
    def __init__(self):
        super().__init__(
            role=AgentRole.ADVISOR,
            name="Financial Advisor",
            capabilities=[
                "recommendation_generation",
                "risk_assessment",
                "opportunity_identification",
                "strategy_formulation"
            ]
        )
    
    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide financial advice"""
        task_type = task.get("type")
        data = task.get("data", {})
        
        if task_type == "generate_recommendations":
            return await self._generate_recommendations(data)
        elif task_type == "assess_risk":
            return await self._assess_risk(data)
        elif task_type == "identify_opportunities":
            return await self._identify_opportunities(data)
        
        return {"status": "unknown_task"}
    
    async def _generate_recommendations(self, data: Dict) -> Dict:
        """Generate personalized recommendations"""
        analysis = data.get("analysis", {})
        user_profile = data.get("user_profile", {})
        
        recommendations = []
        
        # Spending recommendations
        if analysis.get("total_spending", 0) > analysis.get("total_income", 0):
            recommendations.append({
                "category": "Spending",
                "priority": "high",
                "title": "Reduce Expenses",
                "description": "Your spending exceeds income. Focus on cutting discretionary expenses.",
                "action": "Review top spending categories and identify areas to reduce",
                "impact": "high"
            })
        
        # Savings recommendations
        savings_rate = data.get("savings_rate", 0)
        if savings_rate < 20:
            recommendations.append({
                "category": "Savings",
                "priority": "high",
                "title": "Increase Savings Rate",
                "description": f"Current savings rate is {savings_rate}%. Aim for 20%+",
                "action": "Set up automatic transfers to savings account",
                "impact": "high"
            })
        
        # Investment recommendations
        if data.get("investment_value", 0) < data.get("net_worth", 0) * 0.3:
            recommendations.append({
                "category": "Investment",
                "priority": "medium",
                "title": "Diversify Investments",
                "description": "Consider increasing investment allocation for long-term growth",
                "action": "Explore mutual funds, stocks, or retirement accounts",
                "impact": "medium"
            })
        
        return {
            "status": "success",
            "recommendations": recommendations
        }
    
    async def _assess_risk(self, data: Dict) -> Dict:
        """Assess financial risk"""
        debt_to_income = data.get("debt_to_income", 0)
        emergency_fund = data.get("emergency_fund_months", 0)
        credit_score = data.get("credit_score", 750)
        
        risk_factors = []
        risk_score = 0
        
        if debt_to_income > 40:
            risk_factors.append("High debt-to-income ratio")
            risk_score += 30
        
        if emergency_fund < 3:
            risk_factors.append("Insufficient emergency fund")
            risk_score += 25
        
        if credit_score < 650:
            risk_factors.append("Low credit score")
            risk_score += 20
        
        risk_level = "low" if risk_score < 30 else "medium" if risk_score < 60 else "high"
        
        return {
            "status": "success",
            "risk_assessment": {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "mitigation_strategies": self._get_mitigation_strategies(risk_factors)
            }
        }
    
    async def _identify_opportunities(self, data: Dict) -> Dict:
        """Identify financial opportunities"""
        opportunities = []
        
        # Tax optimization
        if data.get("tax_efficiency", 0) < 70:
            opportunities.append({
                "type": "tax_optimization",
                "title": "Tax Optimization Opportunity",
                "description": "Potential to save on taxes through strategic investments",
                "potential_savings": "₹50,000 - ₹1,00,000 annually"
            })
        
        # Credit score improvement
        if data.get("credit_score", 750) < 800:
            opportunities.append({
                "type": "credit_improvement",
                "title": "Credit Score Enhancement",
                "description": "Improve credit score to access better loan rates",
                "potential_savings": "Lower interest rates on future loans"
            })
        
        return {
            "status": "success",
            "opportunities": opportunities
        }
    
    def _get_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get strategies to mitigate risks"""
        strategies = []
        
        for factor in risk_factors:
            if "debt" in factor.lower():
                strategies.append("Create debt repayment plan focusing on high-interest debt first")
            elif "emergency" in factor.lower():
                strategies.append("Build emergency fund to cover 6 months of expenses")
            elif "credit" in factor.lower():
                strategies.append("Improve credit score through timely payments and low utilization")
        
        return strategies


class PlannerAgent(Agent):
    """Agent specialized in financial planning"""
    
    def __init__(self):
        super().__init__(
            role=AgentRole.PLANNER,
            name="Financial Planner",
            capabilities=[
                "goal_planning",
                "budget_creation",
                "timeline_projection",
                "milestone_tracking"
            ]
        )
    
    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create financial plans"""
        task_type = task.get("type")
        data = task.get("data", {})
        
        if task_type == "create_goal_plan":
            return await self._create_goal_plan(data)
        elif task_type == "create_budget":
            return await self._create_budget(data)
        elif task_type == "project_timeline":
            return await self._project_timeline(data)
        
        return {"status": "unknown_task"}
    
    async def _create_goal_plan(self, data: Dict) -> Dict:
        """Create a plan to achieve financial goal"""
        goal_amount = data.get("goal_amount", 0)
        current_savings = data.get("current_savings", 0)
        monthly_savings = data.get("monthly_savings", 0)
        timeline_months = data.get("timeline_months", 12)
        
        remaining = goal_amount - current_savings
        required_monthly = remaining / timeline_months if timeline_months > 0 else 0
        
        is_achievable = required_monthly <= monthly_savings * 1.5
        
        # Create milestones
        milestones = []
        for i in range(1, min(timeline_months + 1, 13)):
            milestone_amount = current_savings + (required_monthly * i)
            milestones.append({
                "month": i,
                "target": round(milestone_amount, 2),
                "percentage": round((milestone_amount / goal_amount * 100), 1)
            })
        
        return {
            "status": "success",
            "plan": {
                "goal_amount": goal_amount,
                "current_savings": current_savings,
                "remaining": remaining,
                "required_monthly_savings": round(required_monthly, 2),
                "is_achievable": is_achievable,
                "timeline_months": timeline_months,
                "milestones": milestones,
                "recommendations": self._get_goal_recommendations(
                    required_monthly,
                    monthly_savings,
                    is_achievable
                )
            }
        }
    
    async def _create_budget(self, data: Dict) -> Dict:
        """Create optimized budget"""
        income = data.get("income", 0)
        current_expenses = data.get("current_expenses", {})
        
        # 50/30/20 rule
        needs_budget = income * 0.50
        wants_budget = income * 0.30
        savings_budget = income * 0.20
        
        budget = {
            "income": income,
            "needs": {
                "budget": needs_budget,
                "categories": ["Rent", "Groceries", "Utilities", "Healthcare", "Transportation"]
            },
            "wants": {
                "budget": wants_budget,
                "categories": ["Entertainment", "Dining", "Shopping", "Travel"]
            },
            "savings": {
                "budget": savings_budget,
                "categories": ["Emergency Fund", "Investments", "Goals"]
            }
        }
        
        return {
            "status": "success",
            "budget": budget
        }
    
    async def _project_timeline(self, data: Dict) -> Dict:
        """Project financial timeline"""
        current_net_worth = data.get("current_net_worth", 0)
        monthly_savings = data.get("monthly_savings", 0)
        investment_return = data.get("investment_return", 0.10)  # 10% annual
        
        # Project 5 years
        projections = []
        net_worth = current_net_worth
        
        for year in range(1, 6):
            # Add savings
            net_worth += monthly_savings * 12
            # Add investment returns
            net_worth *= (1 + investment_return)
            
            projections.append({
                "year": year,
                "projected_net_worth": round(net_worth, 2)
            })
        
        return {
            "status": "success",
            "projections": projections
        }
    
    def _get_goal_recommendations(
        self,
        required: float,
        current: float,
        achievable: bool
    ) -> List[str]:
        """Get recommendations for goal achievement"""
        recommendations = []
        
        if not achievable:
            gap = required - current
            recommendations.append(f"Increase monthly savings by ₹{gap:,.0f} or extend timeline")
        
        recommendations.append("Set up automatic transfers on payday")
        recommendations.append("Review and reduce discretionary spending")
        recommendations.append("Consider additional income sources")
        
        return recommendations


class MultiAgentCoordinator:
    """Coordinates multiple agents to solve complex tasks"""
    
    def __init__(self):
        self.agents = {
            "analyst": AnalystAgent(),
            "advisor": AdvisorAgent(),
            "planner": PlannerAgent(),
        }
        self.workflow_history: List[Dict] = []
    
    async def execute_workflow(
        self,
        workflow_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a multi-agent workflow"""
        logger.info(f"Starting workflow: {workflow_type}")
        
        workflow_start = datetime.now()
        results = {}
        
        if workflow_type == "comprehensive_analysis":
            results = await self._comprehensive_analysis_workflow(data)
        elif workflow_type == "goal_planning":
            results = await self._goal_planning_workflow(data)
        elif workflow_type == "financial_checkup":
            results = await self._financial_checkup_workflow(data)
        else:
            return {"status": "error", "message": f"Unknown workflow: {workflow_type}"}
        
        workflow_end = datetime.now()
        duration = (workflow_end - workflow_start).total_seconds()
        
        # Record workflow
        self.workflow_history.append({
            "workflow_type": workflow_type,
            "start_time": workflow_start.isoformat(),
            "end_time": workflow_end.isoformat(),
            "duration_seconds": duration,
            "results": results
        })
        
        return {
            "status": "success",
            "workflow_type": workflow_type,
            "duration_seconds": round(duration, 2),
            "results": results
        }
    
    async def _comprehensive_analysis_workflow(self, data: Dict) -> Dict:
        """Comprehensive financial analysis workflow"""
        # Step 1: Analyst analyzes spending and income
        spending_task = {"type": "spending_analysis", "data": data}
        income_task = {"type": "income_analysis", "data": data}
        trend_task = {"type": "trend_detection", "data": data}
        
        spending_result, income_result, trend_result = await asyncio.gather(
            self.agents["analyst"].process(spending_task),
            self.agents["analyst"].process(income_task),
            self.agents["analyst"].process(trend_task)
        )
        
        # Step 2: Advisor generates recommendations based on analysis
        advisor_data = {
            "analysis": {
                **spending_result.get("analysis", {}),
                **income_result.get("analysis", {}),
                **trend_result.get("trends", {})
            },
            "user_profile": data.get("user_profile", {})
        }
        
        recommendations_task = {"type": "generate_recommendations", "data": advisor_data}
        risk_task = {"type": "assess_risk", "data": data}
        
        recommendations_result, risk_result = await asyncio.gather(
            self.agents["advisor"].process(recommendations_task),
            self.agents["advisor"].process(risk_task)
        )
        
        return {
            "spending_analysis": spending_result,
            "income_analysis": income_result,
            "trends": trend_result,
            "recommendations": recommendations_result,
            "risk_assessment": risk_result
        }
    
    async def _goal_planning_workflow(self, data: Dict) -> Dict:
        """Goal planning workflow"""
        # Step 1: Planner creates goal plan
        goal_plan_task = {"type": "create_goal_plan", "data": data}
        budget_task = {"type": "create_budget", "data": data}
        
        goal_plan_result, budget_result = await asyncio.gather(
            self.agents["planner"].process(goal_plan_task),
            self.agents["planner"].process(budget_task)
        )
        
        # Step 2: Advisor identifies opportunities
        opportunities_task = {"type": "identify_opportunities", "data": data}
        opportunities_result = await self.agents["advisor"].process(opportunities_task)
        
        return {
            "goal_plan": goal_plan_result,
            "budget": budget_result,
            "opportunities": opportunities_result
        }
    
    async def _financial_checkup_workflow(self, data: Dict) -> Dict:
        """Complete financial health checkup"""
        # Run all analyses in parallel
        tasks = [
            self.agents["analyst"].process({"type": "spending_analysis", "data": data}),
            self.agents["analyst"].process({"type": "anomaly_detection", "data": data}),
            self.agents["advisor"].process({"type": "assess_risk", "data": data}),
            self.agents["planner"].process({"type": "project_timeline", "data": data}),
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "spending_analysis": results[0],
            "anomalies": results[1],
            "risk_assessment": results[2],
            "projections": results[3]
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            agent_name: {
                "role": agent.role.value,
                "status": agent.status,
                "capabilities": agent.capabilities,
                "tasks_completed": len(agent.memory)
            }
            for agent_name, agent in self.agents.items()
        }


# Singleton instance
multi_agent_coordinator = MultiAgentCoordinator()
