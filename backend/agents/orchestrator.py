"""
Agent Orchestrator
Coordinates multiple specialized agents for complex financial tasks
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent
from .query_agent import QueryUnderstandingAgent
from .expense_agent import ExpenseAnalysisAgent
from .savings_agent import SavingsAgent
from .goal_agent import GoalPlanningAgent
from .risk_agent import RiskAnalysisAgent
from .investment_agent import InvestmentAgent
from .forecast_agent import ForecastingAgent
from .recommendation_agent import RecommendationAgent
from .alert_agent import AlertAgent
from .report_agent import ReportGenerationAgent
from .scenario_agent import ScenarioSimulationAgent
from .health_agent import FinancialHealthAgent
from .chat_agent import ChatResponseAgent
from .security_agent import SecurityValidationAgent


class AgentOrchestrator:
    """Orchestrates multiple specialized agents"""
    
    def __init__(self):
        # Initialize all agents
        self.agents: Dict[str, BaseAgent] = {
            "query": QueryUnderstandingAgent(),
            "expense": ExpenseAnalysisAgent(),
            "savings": SavingsAgent(),
            "goal": GoalPlanningAgent(),
            "risk": RiskAnalysisAgent(),
            "investment": InvestmentAgent(),
            "forecast": ForecastingAgent(),
            "recommendation": RecommendationAgent(),
            "alert": AlertAgent(),
            "report": ReportGenerationAgent(),
            "scenario": ScenarioSimulationAgent(),
            "health": FinancialHealthAgent(),
            "chat": ChatResponseAgent(),
            "security": SecurityValidationAgent(),
        }
        
        self.execution_history: List[Dict] = []
    
    async def execute_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a predefined workflow using multiple agents
        
        Args:
            workflow_type: Type of workflow to execute
            data: Input data for the workflow
            
        Returns:
            Workflow execution results
        """
        workflow_start = datetime.now()
        
        if workflow_type == "comprehensive_analysis":
            result = await self._comprehensive_analysis_workflow(data)
        elif workflow_type == "goal_planning":
            result = await self._goal_planning_workflow(data)
        elif workflow_type == "financial_checkup":
            result = await self._financial_checkup_workflow(data)
        elif workflow_type == "risk_assessment":
            result = await self._risk_assessment_workflow(data)
        elif workflow_type == "investment_review":
            result = await self._investment_review_workflow(data)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        workflow_end = datetime.now()
        execution_time = (workflow_end - workflow_start).total_seconds()
        
        # Record execution
        self.execution_history.append({
            "workflow_type": workflow_type,
            "timestamp": workflow_start.isoformat(),
            "execution_time": execution_time,
            "success": True
        })
        
        result["execution_time"] = execution_time
        result["timestamp"] = workflow_start.isoformat()
        
        return result
    
    async def _comprehensive_analysis_workflow(self, data: Dict) -> Dict:
        """Complete financial analysis workflow"""
        results = {}
        
        # Step 1: Analyze expenses
        expense_task = {"type": "analyze_expenses", "data": data}
        results["expense_analysis"] = await self.agents["expense"].execute(expense_task)
        
        # Step 2: Analyze savings
        savings_task = {"type": "analyze_savings", "data": data}
        results["savings_analysis"] = await self.agents["savings"].execute(savings_task)
        
        # Step 3: Check financial health
        health_task = {"type": "calculate_health", "data": data}
        results["health_score"] = await self.agents["health"].execute(health_task)
        
        # Step 4: Assess risks
        risk_task = {"type": "assess_risks", "data": data}
        results["risk_assessment"] = await self.agents["risk"].execute(risk_task)
        
        # Step 5: Generate recommendations
        rec_task = {
            "type": "generate_recommendations",
            "data": data,
            "context": {
                "expense_analysis": results["expense_analysis"],
                "savings_analysis": results["savings_analysis"],
                "health_score": results["health_score"],
                "risk_assessment": results["risk_assessment"]
            }
        }
        results["recommendations"] = await self.agents["recommendation"].execute(rec_task)
        
        return {
            "workflow": "comprehensive_analysis",
            "results": results,
            "summary": self._generate_analysis_summary(results)
        }
    
    async def _goal_planning_workflow(self, data: Dict) -> Dict:
        """Goal planning workflow"""
        results = {}
        
        # Step 1: Analyze current financial state
        savings_task = {"type": "analyze_savings", "data": data}
        results["savings_analysis"] = await self.agents["savings"].execute(savings_task)
        
        # Step 2: Create goal plan
        goal_task = {
            "type": "create_goal_plan",
            "data": data,
            "context": {"savings_analysis": results["savings_analysis"]}
        }
        results["goal_plan"] = await self.agents["goal"].execute(goal_task)
        
        # Step 3: Forecast goal timeline
        forecast_task = {
            "type": "forecast_goals",
            "data": data,
            "context": {"goal_plan": results["goal_plan"]}
        }
        results["timeline_forecast"] = await self.agents["forecast"].execute(forecast_task)
        
        # Step 4: Generate recommendations
        rec_task = {
            "type": "goal_recommendations",
            "data": data,
            "context": {
                "goal_plan": results["goal_plan"],
                "timeline_forecast": results["timeline_forecast"]
            }
        }
        results["recommendations"] = await self.agents["recommendation"].execute(rec_task)
        
        return {
            "workflow": "goal_planning",
            "results": results,
            "summary": self._generate_goal_summary(results)
        }
    
    async def _financial_checkup_workflow(self, data: Dict) -> Dict:
        """Complete financial health checkup"""
        results = {}
        
        # Step 1: Calculate health score
        health_task = {"type": "calculate_health", "data": data}
        results["health_score"] = await self.agents["health"].execute(health_task)
        
        # Step 2: Analyze spending patterns
        expense_task = {"type": "analyze_patterns", "data": data}
        results["spending_patterns"] = await self.agents["expense"].execute(expense_task)
        
        # Step 3: Check for anomalies
        alert_task = {"type": "detect_anomalies", "data": data}
        results["anomalies"] = await self.agents["alert"].execute(alert_task)
        
        # Step 4: Assess risks
        risk_task = {"type": "assess_risks", "data": data}
        results["risk_assessment"] = await self.agents["risk"].execute(risk_task)
        
        # Step 5: Generate forecast
        forecast_task = {"type": "forecast_monthly", "data": data}
        results["forecast"] = await self.agents["forecast"].execute(forecast_task)
        
        # Step 6: Generate recommendations
        rec_task = {
            "type": "health_recommendations",
            "data": data,
            "context": results
        }
        results["recommendations"] = await self.agents["recommendation"].execute(rec_task)
        
        return {
            "workflow": "financial_checkup",
            "results": results,
            "summary": self._generate_checkup_summary(results)
        }
    
    async def _risk_assessment_workflow(self, data: Dict) -> Dict:
        """Risk assessment workflow"""
        results = {}
        
        # Step 1: Assess financial risks
        risk_task = {"type": "assess_risks", "data": data}
        results["risk_assessment"] = await self.agents["risk"].execute(risk_task)
        
        # Step 2: Run scenario simulations
        scenario_task = {
            "type": "simulate_risks",
            "data": data,
            "context": {"risk_assessment": results["risk_assessment"]}
        }
        results["risk_scenarios"] = await self.agents["scenario"].execute(scenario_task)
        
        # Step 3: Generate mitigation recommendations
        rec_task = {
            "type": "risk_mitigation",
            "data": data,
            "context": {
                "risk_assessment": results["risk_assessment"],
                "risk_scenarios": results["risk_scenarios"]
            }
        }
        results["mitigation_plan"] = await self.agents["recommendation"].execute(rec_task)
        
        return {
            "workflow": "risk_assessment",
            "results": results,
            "summary": self._generate_risk_summary(results)
        }
    
    async def _investment_review_workflow(self, data: Dict) -> Dict:
        """Investment portfolio review workflow"""
        results = {}
        
        # Step 1: Analyze investment portfolio
        investment_task = {"type": "analyze_portfolio", "data": data}
        results["portfolio_analysis"] = await self.agents["investment"].execute(investment_task)
        
        # Step 2: Assess investment risks
        risk_task = {"type": "assess_investment_risks", "data": data}
        results["investment_risks"] = await self.agents["risk"].execute(risk_task)
        
        # Step 3: Generate investment recommendations
        rec_task = {
            "type": "investment_recommendations",
            "data": data,
            "context": {
                "portfolio_analysis": results["portfolio_analysis"],
                "investment_risks": results["investment_risks"]
            }
        }
        results["recommendations"] = await self.agents["recommendation"].execute(rec_task)
        
        return {
            "workflow": "investment_review",
            "results": results,
            "summary": self._generate_investment_summary(results)
        }
    
    def _generate_analysis_summary(self, results: Dict) -> str:
        """Generate summary for comprehensive analysis"""
        health = results.get("health_score", {}).get("overall_score", 0)
        risk_level = results.get("risk_assessment", {}).get("risk_level", "Unknown")
        rec_count = len(results.get("recommendations", {}).get("recommendations", []))
        
        return f"Financial Health: {health}/100 | Risk Level: {risk_level} | {rec_count} Recommendations"
    
    def _generate_goal_summary(self, results: Dict) -> str:
        """Generate summary for goal planning"""
        goals = results.get("goal_plan", {}).get("goals", [])
        achievable = sum(1 for g in goals if g.get("achievable", False))
        
        return f"{len(goals)} Goals Analyzed | {achievable} Achievable with Current Savings"
    
    def _generate_checkup_summary(self, results: Dict) -> str:
        """Generate summary for financial checkup"""
        health = results.get("health_score", {}).get("overall_score", 0)
        anomalies = len(results.get("anomalies", {}).get("alerts", []))
        
        return f"Health Score: {health}/100 | {anomalies} Anomalies Detected"
    
    def _generate_risk_summary(self, results: Dict) -> str:
        """Generate summary for risk assessment"""
        risk_level = results.get("risk_assessment", {}).get("risk_level", "Unknown")
        risk_count = len(results.get("risk_assessment", {}).get("risks", []))
        
        return f"Risk Level: {risk_level} | {risk_count} Risks Identified"
    
    def _generate_investment_summary(self, results: Dict) -> str:
        """Generate summary for investment review"""
        portfolio = results.get("portfolio_analysis", {})
        total_value = portfolio.get("total_value", 0)
        returns = portfolio.get("overall_returns", 0)
        
        return f"Portfolio Value: ₹{total_value:,.0f} | Returns: {returns:.1f}%"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            name: agent.get_status()
            for name, agent in self.agents.items()
        }
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """Get recent execution history"""
        return self.execution_history[-limit:]


# Global orchestrator instance
orchestrator = AgentOrchestrator()
