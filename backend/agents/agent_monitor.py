"""
Agent Monitor
Monitor and track agent performance and health
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time
import statistics


class AgentMonitor:
    """Monitor agent performance and health"""
    
    def __init__(self):
        # Agent execution history
        self.execution_history: List[Dict] = []
        
        # Agent metrics
        self.agent_metrics: Dict[str, Dict] = defaultdict(lambda: {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_execution_time": 0.0,
            "average_execution_time": 0.0,
            "last_execution": None,
            "error_count": 0,
            "errors": []
        })
        
        # Agent health status
        self.agent_health: Dict[str, str] = {}
        
        # Performance thresholds
        self.thresholds = {
            "max_execution_time": 30.0,  # seconds
            "max_error_rate": 0.1,  # 10%
            "max_consecutive_errors": 3
        }
    
    def start_execution(self, agent_name: str, task: str) -> str:
        """
        Start tracking an agent execution
        
        Args:
            agent_name: Name of the agent
            task: Task description
            
        Returns:
            Execution ID
        """
        execution_id = f"{agent_name}_{int(time.time() * 1000)}"
        
        execution = {
            "execution_id": execution_id,
            "agent_name": agent_name,
            "task": task,
            "start_time": datetime.now().isoformat(),
            "start_timestamp": time.time(),
            "status": "running"
        }
        
        self.execution_history.append(execution)
        
        return execution_id
    
    def end_execution(
        self,
        execution_id: str,
        success: bool,
        result: Optional[Any] = None,
        error: Optional[str] = None
    ):
        """
        End tracking an agent execution
        
        Args:
            execution_id: Execution ID
            success: Whether execution was successful
            result: Execution result
            error: Error message if failed
        """
        # Find execution
        execution = next(
            (e for e in self.execution_history if e["execution_id"] == execution_id),
            None
        )
        
        if not execution:
            return
        
        # Update execution
        end_time = time.time()
        execution_time = end_time - execution["start_timestamp"]
        
        execution.update({
            "end_time": datetime.now().isoformat(),
            "execution_time": execution_time,
            "status": "success" if success else "failed",
            "result": result,
            "error": error
        })
        
        # Update agent metrics
        agent_name = execution["agent_name"]
        metrics = self.agent_metrics[agent_name]
        
        metrics["total_executions"] += 1
        metrics["total_execution_time"] += execution_time
        metrics["average_execution_time"] = (
            metrics["total_execution_time"] / metrics["total_executions"]
        )
        metrics["last_execution"] = datetime.now().isoformat()
        
        if success:
            metrics["successful_executions"] += 1
        else:
            metrics["failed_executions"] += 1
            metrics["error_count"] += 1
            metrics["errors"].append({
                "timestamp": datetime.now().isoformat(),
                "error": error,
                "task": execution["task"]
            })
            
            # Keep only last 10 errors
            if len(metrics["errors"]) > 10:
                metrics["errors"] = metrics["errors"][-10:]
        
        # Update health status
        self._update_agent_health(agent_name)
    
    def _update_agent_health(self, agent_name: str):
        """Update agent health status"""
        metrics = self.agent_metrics[agent_name]
        
        # Calculate error rate
        total = metrics["total_executions"]
        if total == 0:
            self.agent_health[agent_name] = "unknown"
            return
        
        error_rate = metrics["failed_executions"] / total
        avg_time = metrics["average_execution_time"]
        
        # Check recent errors
        recent_executions = [
            e for e in self.execution_history[-10:]
            if e["agent_name"] == agent_name
        ]
        consecutive_errors = 0
        for execution in reversed(recent_executions):
            if execution.get("status") == "failed":
                consecutive_errors += 1
            else:
                break
        
        # Determine health status
        if consecutive_errors >= self.thresholds["max_consecutive_errors"]:
            health = "critical"
        elif error_rate > self.thresholds["max_error_rate"]:
            health = "degraded"
        elif avg_time > self.thresholds["max_execution_time"]:
            health = "slow"
        else:
            health = "healthy"
        
        self.agent_health[agent_name] = health
    
    def get_agent_metrics(self, agent_name: str) -> Dict:
        """Get metrics for a specific agent"""
        metrics = dict(self.agent_metrics.get(agent_name, {}))
        
        # Add health status
        metrics["health_status"] = self.agent_health.get(agent_name, "unknown")
        
        # Calculate success rate
        total = metrics.get("total_executions", 0)
        if total > 0:
            metrics["success_rate"] = round(
                (metrics.get("successful_executions", 0) / total) * 100,
                2
            )
        else:
            metrics["success_rate"] = 0.0
        
        return metrics
    
    def get_all_metrics(self) -> Dict[str, Dict]:
        """Get metrics for all agents"""
        return {
            agent_name: self.get_agent_metrics(agent_name)
            for agent_name in self.agent_metrics.keys()
        }
    
    def get_execution_history(
        self,
        agent_name: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get execution history
        
        Args:
            agent_name: Optional agent name to filter by
            limit: Maximum number of executions to return
            
        Returns:
            List of executions
        """
        history = self.execution_history
        
        if agent_name:
            history = [e for e in history if e["agent_name"] == agent_name]
        
        # Sort by start time (most recent first)
        history = sorted(
            history,
            key=lambda x: x["start_time"],
            reverse=True
        )
        
        return history[:limit]
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "total_agents": 0,
                "overall_success_rate": 0.0,
                "average_execution_time": 0.0,
                "healthy_agents": 0,
                "degraded_agents": 0,
                "critical_agents": 0
            }
        
        total_executions = len(self.execution_history)
        successful = sum(
            1 for e in self.execution_history
            if e.get("status") == "success"
        )
        
        execution_times = [
            e.get("execution_time", 0)
            for e in self.execution_history
            if "execution_time" in e
        ]
        
        # Count agents by health
        health_counts = defaultdict(int)
        for health in self.agent_health.values():
            health_counts[health] += 1
        
        return {
            "total_executions": total_executions,
            "total_agents": len(self.agent_metrics),
            "overall_success_rate": round((successful / total_executions) * 100, 2),
            "average_execution_time": round(
                statistics.mean(execution_times) if execution_times else 0,
                2
            ),
            "healthy_agents": health_counts.get("healthy", 0),
            "degraded_agents": health_counts.get("degraded", 0) + health_counts.get("slow", 0),
            "critical_agents": health_counts.get("critical", 0),
            "agent_health": dict(self.agent_health)
        }
    
    def get_agent_leaderboard(self) -> List[Dict]:
        """Get agent leaderboard by performance"""
        leaderboard = []
        
        for agent_name in self.agent_metrics.keys():
            metrics = self.get_agent_metrics(agent_name)
            
            # Calculate performance score
            success_rate = metrics.get("success_rate", 0)
            avg_time = metrics.get("average_execution_time", 0)
            
            # Score: success_rate (70%) + speed score (30%)
            speed_score = max(0, 100 - (avg_time * 2))  # Penalize slow agents
            performance_score = (success_rate * 0.7) + (speed_score * 0.3)
            
            leaderboard.append({
                "agent_name": agent_name,
                "performance_score": round(performance_score, 2),
                "success_rate": success_rate,
                "average_execution_time": round(avg_time, 2),
                "total_executions": metrics.get("total_executions", 0),
                "health_status": metrics.get("health_status", "unknown")
            })
        
        # Sort by performance score
        leaderboard.sort(key=lambda x: x["performance_score"], reverse=True)
        
        return leaderboard
    
    def get_slow_agents(self, threshold: Optional[float] = None) -> List[Dict]:
        """Get agents with slow execution times"""
        threshold = threshold or self.thresholds["max_execution_time"]
        
        slow_agents = []
        
        for agent_name, metrics in self.agent_metrics.items():
            avg_time = metrics.get("average_execution_time", 0)
            
            if avg_time > threshold:
                slow_agents.append({
                    "agent_name": agent_name,
                    "average_execution_time": round(avg_time, 2),
                    "threshold": threshold,
                    "total_executions": metrics.get("total_executions", 0)
                })
        
        # Sort by execution time
        slow_agents.sort(key=lambda x: x["average_execution_time"], reverse=True)
        
        return slow_agents
    
    def get_error_prone_agents(self, threshold: Optional[float] = None) -> List[Dict]:
        """Get agents with high error rates"""
        threshold = threshold or self.thresholds["max_error_rate"]
        
        error_prone = []
        
        for agent_name, metrics in self.agent_metrics.items():
            total = metrics.get("total_executions", 0)
            if total == 0:
                continue
            
            error_rate = metrics.get("failed_executions", 0) / total
            
            if error_rate > threshold:
                error_prone.append({
                    "agent_name": agent_name,
                    "error_rate": round(error_rate * 100, 2),
                    "threshold": round(threshold * 100, 2),
                    "total_executions": total,
                    "failed_executions": metrics.get("failed_executions", 0),
                    "recent_errors": metrics.get("errors", [])[-3:]
                })
        
        # Sort by error rate
        error_prone.sort(key=lambda x: x["error_rate"], reverse=True)
        
        return error_prone
    
    def clear_history(self, older_than_days: Optional[int] = None):
        """
        Clear execution history
        
        Args:
            older_than_days: Clear only executions older than X days
        """
        if older_than_days:
            cutoff = datetime.now() - timedelta(days=older_than_days)
            self.execution_history = [
                e for e in self.execution_history
                if datetime.fromisoformat(e["start_time"]) > cutoff
            ]
        else:
            self.execution_history = []
            self.agent_metrics.clear()
            self.agent_health.clear()


# Global instance
agent_monitor = AgentMonitor()
