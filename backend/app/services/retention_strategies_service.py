"""
Retention strategies service for employee turnover prevention.
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.models.base import RiskZone, StrategyStatus
from app.exceptions.custom_exceptions import DataValidationError, ResourceNotFoundError
import logging

logger = logging.getLogger(__name__)


class RetentionStrategiesService:
    """Service for generating and managing retention strategies."""
    
    def __init__(self):
        self.strategies_database = self._load_strategies_database()
        self.implementation_templates = self._load_implementation_templates()
    
    def _load_strategies_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load comprehensive retention strategies database."""
        return {
            "low": [
                {
                    "id": "low_001",
                    "strategy": "Regular Check-ins",
                    "description": "Schedule monthly one-on-one meetings to maintain engagement",
                    "priority": "low",
                    "effort": "low",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["meeting attendance", "engagement scores"],
                    "implementation_steps": [
                        "Schedule recurring monthly meetings",
                        "Prepare discussion topics",
                        "Document feedback and concerns"
                    ]
                },
                {
                    "id": "low_002",
                    "strategy": "Career Development Planning",
                    "description": "Create personalized career development plans",
                    "priority": "medium",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "1-3 months",
                    "success_metrics": ["career plan completion", "skill development"],
                    "implementation_steps": [
                        "Assess current skills and interests",
                        "Identify growth opportunities",
                        "Create development roadmap",
                        "Schedule regular progress reviews"
                    ]
                },
                {
                    "id": "low_003",
                    "strategy": "Recognition Programs",
                    "description": "Implement peer and manager recognition programs",
                    "priority": "medium",
                    "effort": "low",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["recognition frequency", "employee satisfaction"],
                    "implementation_steps": [
                        "Set up recognition platform",
                        "Train managers on recognition best practices",
                        "Launch peer recognition program"
                    ]
                }
            ],
            "medium": [
                {
                    "id": "medium_001",
                    "strategy": "Increased Feedback Frequency",
                    "description": "Provide more frequent and detailed performance feedback",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["feedback frequency", "performance improvement"],
                    "implementation_steps": [
                        "Schedule bi-weekly feedback sessions",
                        "Provide specific, actionable feedback",
                        "Document progress and improvements"
                    ]
                },
                {
                    "id": "medium_002",
                    "strategy": "Mentorship Program",
                    "description": "Assign experienced mentors to provide guidance and support",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "1-2 months",
                    "success_metrics": ["mentor-mentee satisfaction", "skill development"],
                    "implementation_steps": [
                        "Identify potential mentors",
                        "Match mentors with employees",
                        "Establish mentorship guidelines",
                        "Schedule regular mentor meetings"
                    ]
                },
                {
                    "id": "medium_003",
                    "strategy": "Work-Life Balance Review",
                    "description": "Review and improve work-life balance policies",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "1-3 months",
                    "success_metrics": ["work-life balance scores", "overtime reduction"],
                    "implementation_steps": [
                        "Assess current workload",
                        "Review flexible work options",
                        "Implement work-life balance initiatives",
                        "Monitor and adjust policies"
                    ]
                },
                {
                    "id": "medium_004",
                    "strategy": "Skill Development Opportunities",
                    "description": "Provide targeted training and development opportunities",
                    "priority": "medium",
                    "effort": "high",
                    "cost": "medium",
                    "timeline": "2-6 months",
                    "success_metrics": ["training completion", "skill assessment scores"],
                    "implementation_steps": [
                        "Identify skill gaps",
                        "Select relevant training programs",
                        "Allocate training budget",
                        "Schedule and track training progress"
                    ]
                }
            ],
            "high": [
                {
                    "id": "high_001",
                    "strategy": "Immediate Manager Intervention",
                    "description": "Direct manager involvement in retention efforts",
                    "priority": "critical",
                    "effort": "high",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["manager engagement", "employee satisfaction"],
                    "implementation_steps": [
                        "Schedule urgent meeting with manager",
                        "Discuss concerns and expectations",
                        "Develop immediate action plan",
                        "Follow up within 48 hours"
                    ]
                },
                {
                    "id": "high_002",
                    "strategy": "Salary Review and Adjustment",
                    "description": "Conduct comprehensive salary review and make adjustments",
                    "priority": "critical",
                    "effort": "high",
                    "cost": "high",
                    "timeline": "1-2 months",
                    "success_metrics": ["salary competitiveness", "employee satisfaction"],
                    "implementation_steps": [
                        "Conduct market salary analysis",
                        "Review current compensation",
                        "Prepare salary adjustment proposal",
                        "Implement approved adjustments"
                    ]
                },
                {
                    "id": "high_003",
                    "strategy": "Role Adjustment and Promotion",
                    "description": "Explore role changes, promotions, or lateral moves",
                    "priority": "critical",
                    "effort": "high",
                    "cost": "medium",
                    "timeline": "2-4 months",
                    "success_metrics": ["role satisfaction", "career progression"],
                    "implementation_steps": [
                        "Assess career aspirations",
                        "Identify suitable roles",
                        "Prepare transition plan",
                        "Execute role change"
                    ]
                },
                {
                    "id": "high_004",
                    "strategy": "Retention Bonus Package",
                    "description": "Offer financial incentives to encourage retention",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "high",
                    "timeline": "immediate",
                    "success_metrics": ["retention rate", "employee satisfaction"],
                    "implementation_steps": [
                        "Design retention bonus structure",
                        "Calculate appropriate bonus amount",
                        "Present offer to employee",
                        "Execute retention agreement"
                    ]
                },
                {
                    "id": "high_005",
                    "strategy": "Flexible Work Arrangements",
                    "description": "Implement flexible work schedules and remote options",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "1-2 months",
                    "success_metrics": ["work flexibility satisfaction", "productivity"],
                    "implementation_steps": [
                        "Assess feasibility of flexible arrangements",
                        "Develop flexible work policy",
                        "Implement flexible schedule",
                        "Monitor and adjust arrangements"
                    ]
                }
            ],
            "critical": [
                {
                    "id": "critical_001",
                    "strategy": "Executive Leadership Intervention",
                    "description": "Direct involvement from senior leadership",
                    "priority": "critical",
                    "effort": "high",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["leadership engagement", "employee satisfaction"],
                    "implementation_steps": [
                        "Schedule meeting with senior leadership",
                        "Present retention case",
                        "Develop executive action plan",
                        "Implement leadership initiatives"
                    ]
                },
                {
                    "id": "critical_002",
                    "strategy": "Emergency Retention Package",
                    "description": "Comprehensive retention offer including multiple incentives",
                    "priority": "critical",
                    "effort": "high",
                    "cost": "very high",
                    "timeline": "immediate",
                    "success_metrics": ["retention success", "employee satisfaction"],
                    "implementation_steps": [
                        "Assess all retention options",
                        "Prepare comprehensive offer",
                        "Present emergency retention package",
                        "Execute retention agreement"
                    ]
                },
                {
                    "id": "critical_003",
                    "strategy": "Exit Interview Preparation",
                    "description": "Prepare for potential departure and gather insights",
                    "priority": "high",
                    "effort": "medium",
                    "cost": "low",
                    "timeline": "immediate",
                    "success_metrics": ["exit interview completion", "insights gathered"],
                    "implementation_steps": [
                        "Prepare exit interview questions",
                        "Schedule exit interview",
                        "Conduct comprehensive interview",
                        "Analyze and act on feedback"
                    ]
                },
                {
                    "id": "critical_004",
                    "strategy": "Succession Planning",
                    "description": "Develop plans for role replacement and knowledge transfer",
                    "priority": "high",
                    "effort": "high",
                    "cost": "medium",
                    "timeline": "1-3 months",
                    "success_metrics": ["succession plan completion", "knowledge transfer"],
                    "implementation_steps": [
                        "Identify potential replacements",
                        "Document critical knowledge",
                        "Create knowledge transfer plan",
                        "Execute succession planning"
                    ]
                }
            ]
        }
    
    def _load_implementation_templates(self) -> Dict[str, Any]:
        """Load implementation templates for strategies."""
        return {
            "communication_templates": {
                "manager_meeting": {
                    "subject": "Retention Strategy Discussion - {employee_name}",
                    "body": """
Dear {manager_name},

We have identified {employee_name} as a {risk_level} risk for turnover based on our predictive analytics.

Recommended immediate actions:
{strategies}

Please schedule a meeting within 48 hours to discuss these strategies.

Best regards,
HR Analytics Team
                    """
                },
                "employee_communication": {
                    "subject": "Career Development Discussion",
                    "body": """
Dear {employee_name},

We value your contributions to our team and would like to discuss your career development and job satisfaction.

We have some exciting opportunities and initiatives we'd like to share with you.

Please let us know your availability for a discussion.

Best regards,
{manager_name}
                    """
                }
            },
            "timeline_templates": {
                "immediate": "Within 24-48 hours",
                "short_term": "1-2 weeks",
                "medium_term": "1-3 months",
                "long_term": "3-6 months"
            }
        }
    
    def generate_retention_strategies(
        self, 
        employee_data: Dict[str, Any], 
        risk_zone: str,
        turnover_probability: float
    ) -> Dict[str, Any]:
        """Generate personalized retention strategies for an employee."""
        try:
            # Validate risk zone
            if risk_zone not in self.strategies_database:
                raise DataValidationError(f"Invalid risk zone: {risk_zone}")
            
            # Get base strategies for risk zone
            base_strategies = self.strategies_database[risk_zone]
            
            # Personalize strategies based on employee data
            personalized_strategies = self._personalize_strategies(
                base_strategies, employee_data, risk_zone, turnover_probability
            )
            
            # Generate implementation plan
            implementation_plan = self._generate_implementation_plan(
                personalized_strategies, employee_data
            )
            
            # Calculate expected outcomes
            expected_outcomes = self._calculate_expected_outcomes(
                personalized_strategies, turnover_probability
            )
            
            retention_plan = {
                "employee_id": employee_data.get("employee_id"),
                "risk_zone": risk_zone,
                "turnover_probability": turnover_probability,
                "generated_at": datetime.now().isoformat(),
                "strategies": personalized_strategies,
                "implementation_plan": implementation_plan,
                "expected_outcomes": expected_outcomes,
                "total_estimated_cost": self._calculate_total_cost(personalized_strategies),
                "success_probability": self._calculate_success_probability(
                    personalized_strategies, risk_zone
                )
            }
            
            logger.info(f"Generated retention strategies for employee {employee_data.get('employee_id')}")
            return retention_plan
            
        except Exception as e:
            logger.error(f"Error generating retention strategies: {str(e)}")
            raise DataValidationError(f"Failed to generate retention strategies: {str(e)}")
    
    def _personalize_strategies(
        self, 
        base_strategies: List[Dict[str, Any]], 
        employee_data: Dict[str, Any],
        risk_zone: str,
        turnover_probability: float
    ) -> List[Dict[str, Any]]:
        """Personalize strategies based on employee characteristics."""
        personalized = []
        
        for strategy in base_strategies:
            personalized_strategy = strategy.copy()
            
            # Adjust priority based on employee data
            personalized_strategy["priority"] = self._adjust_priority(
                strategy, employee_data, risk_zone
            )
            
            # Customize implementation steps
            personalized_strategy["customized_steps"] = self._customize_implementation_steps(
                strategy["implementation_steps"], employee_data
            )
            
            # Add employee-specific context
            personalized_strategy["employee_context"] = self._get_employee_context(
                employee_data, strategy
            )
            
            # Calculate personalized timeline
            personalized_strategy["personalized_timeline"] = self._calculate_personalized_timeline(
                strategy, employee_data
            )
            
            personalized.append(personalized_strategy)
        
        # Sort by priority and effort
        personalized.sort(key=lambda x: (
            self._priority_to_number(x["priority"]),
            self._effort_to_number(x["effort"])
        ))
        
        return personalized
    
    def _adjust_priority(
        self, 
        strategy: Dict[str, Any], 
        employee_data: Dict[str, Any],
        risk_zone: str
    ) -> str:
        """Adjust strategy priority based on employee data."""
        base_priority = strategy["priority"]
        
        # Increase priority for high-performing employees
        if employee_data.get("last_evaluation", 0) > 0.8:
            if base_priority == "medium":
                return "high"
            elif base_priority == "low":
                return "medium"
        
        # Increase priority for long-tenured employees
        if employee_data.get("time_spend_company", 0) > 5:
            if base_priority == "medium":
                return "high"
        
        # Increase priority for critical roles
        if employee_data.get("department") in ["IT", "Engineering", "Management"]:
            if base_priority == "low":
                return "medium"
        
        return base_priority
    
    def _customize_implementation_steps(
        self, 
        base_steps: List[str], 
        employee_data: Dict[str, Any]
    ) -> List[str]:
        """Customize implementation steps for specific employee."""
        customized_steps = []
        
        for step in base_steps:
            # Replace placeholders with employee-specific information
            customized_step = step.replace(
                "{employee_name}", employee_data.get("name", "Employee")
            ).replace(
                "{department}", employee_data.get("department", "Department")
            ).replace(
                "{manager_name}", employee_data.get("manager", "Manager")
            )
            
            customized_steps.append(customized_step)
        
        return customized_steps
    
    def _get_employee_context(
        self, 
        employee_data: Dict[str, Any], 
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get employee-specific context for strategy."""
        context = {
            "satisfaction_level": employee_data.get("satisfaction_level", 0),
            "last_evaluation": employee_data.get("last_evaluation", 0),
            "department": employee_data.get("department", "Unknown"),
            "time_at_company": employee_data.get("time_spend_company", 0),
            "salary_level": employee_data.get("salary", "medium")
        }
        
        # Add strategy-specific context
        if "salary" in strategy["strategy"].lower():
            context["salary_review_needed"] = employee_data.get("salary") == "low"
        
        if "promotion" in strategy["strategy"].lower():
            context["promotion_eligible"] = employee_data.get("promotion_last_5years", 0) == 0
        
        return context
    
    def _calculate_personalized_timeline(
        self, 
        strategy: Dict[str, Any], 
        employee_data: Dict[str, Any]
    ) -> str:
        """Calculate personalized timeline for strategy implementation."""
        base_timeline = strategy["timeline"]
        
        # Adjust timeline based on employee urgency
        if employee_data.get("satisfaction_level", 0.5) < 0.3:
            if base_timeline == "1-3 months":
                return "1-2 months"
            elif base_timeline == "2-6 months":
                return "1-3 months"
        
        return base_timeline
    
    def _generate_implementation_plan(
        self, 
        strategies: List[Dict[str, Any]], 
        employee_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive implementation plan."""
        plan = {
            "immediate_actions": [],
            "short_term_goals": [],
            "medium_term_goals": [],
            "long_term_goals": [],
            "key_milestones": [],
            "success_metrics": []
        }
        
        for strategy in strategies:
            timeline = strategy["personalized_timeline"]
            
            if timeline == "immediate":
                plan["immediate_actions"].append({
                    "strategy": strategy["strategy"],
                    "steps": strategy["customized_steps"][:2],  # First 2 steps
                    "owner": "Manager",
                    "deadline": "48 hours"
                })
            elif "1-2" in timeline or "immediate" in timeline:
                plan["short_term_goals"].append({
                    "strategy": strategy["strategy"],
                    "timeline": timeline,
                    "owner": "HR + Manager"
                })
            elif "1-3" in timeline:
                plan["medium_term_goals"].append({
                    "strategy": strategy["strategy"],
                    "timeline": timeline,
                    "owner": "HR Team"
                })
            else:
                plan["long_term_goals"].append({
                    "strategy": strategy["strategy"],
                    "timeline": timeline,
                    "owner": "Leadership"
                })
        
        # Add key milestones
        plan["key_milestones"] = [
            "Initial manager meeting (48 hours)",
            "Strategy implementation start (1 week)",
            "First progress review (1 month)",
            "Strategy effectiveness assessment (3 months)"
        ]
        
        # Add success metrics
        plan["success_metrics"] = [
            "Employee satisfaction improvement",
            "Turnover probability reduction",
            "Strategy implementation completion rate",
            "Employee engagement scores"
        ]
        
        return plan
    
    def _calculate_expected_outcomes(
        self, 
        strategies: List[Dict[str, Any]], 
        current_probability: float
    ) -> Dict[str, Any]:
        """Calculate expected outcomes of retention strategies."""
        # Base reduction factors by risk zone
        reduction_factors = {
            "low": 0.1,
            "medium": 0.2,
            "high": 0.3,
            "critical": 0.4
        }
        
        # Calculate expected probability reduction
        total_reduction = sum(reduction_factors.get(s.get("risk_zone", "medium"), 0.2) for s in strategies)
        expected_probability = max(0.1, current_probability - total_reduction)
        
        return {
            "current_turnover_probability": current_probability,
            "expected_turnover_probability": expected_probability,
            "probability_reduction": current_probability - expected_probability,
            "retention_success_rate": 1 - expected_probability,
            "time_to_see_results": "2-4 weeks",
            "long_term_impact": "3-6 months"
        }
    
    def _calculate_total_cost(self, strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total estimated cost of strategies."""
        cost_mapping = {
            "low": 0,
            "medium": 1000,
            "high": 5000,
            "very high": 15000
        }
        
        total_cost = sum(cost_mapping.get(s["cost"], 0) for s in strategies)
        
        return {
            "total_estimated_cost": total_cost,
            "cost_breakdown": [
                {
                    "strategy": s["strategy"],
                    "cost": cost_mapping.get(s["cost"], 0),
                    "cost_level": s["cost"]
                }
                for s in strategies
            ],
            "cost_justification": "Investment in retention vs. cost of replacement (typically 1.5-2x annual salary)"
        }
    
    def _calculate_success_probability(
        self, 
        strategies: List[Dict[str, Any]], 
        risk_zone: str
    ) -> float:
        """Calculate probability of retention success."""
        base_success_rates = {
            "low": 0.9,
            "medium": 0.7,
            "high": 0.5,
            "critical": 0.3
        }
        
        base_rate = base_success_rates.get(risk_zone, 0.5)
        
        # Adjust based on number and quality of strategies
        strategy_bonus = min(0.2, len(strategies) * 0.05)
        
        return min(0.95, base_rate + strategy_bonus)
    
    def _priority_to_number(self, priority: str) -> int:
        """Convert priority to number for sorting."""
        priority_map = {"low": 3, "medium": 2, "high": 1, "critical": 0}
        return priority_map.get(priority, 2)
    
    def _effort_to_number(self, effort: str) -> int:
        """Convert effort to number for sorting."""
        effort_map = {"low": 0, "medium": 1, "high": 2}
        return effort_map.get(effort, 1)
    
    def get_strategy_by_id(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get specific strategy by ID."""
        for risk_zone, strategies in self.strategies_database.items():
            for strategy in strategies:
                if strategy["id"] == strategy_id:
                    return strategy
        return None
    
    def get_strategies_by_risk_zone(self, risk_zone: str) -> List[Dict[str, Any]]:
        """Get all strategies for a specific risk zone."""
        return self.strategies_database.get(risk_zone, [])
    
    def update_strategy_status(
        self, 
        strategy_id: str, 
        status: StrategyStatus,
        notes: str = None
    ) -> Dict[str, Any]:
        """Update the status of a retention strategy."""
        strategy = self.get_strategy_by_id(strategy_id)
        if not strategy:
            raise ResourceNotFoundError(f"Strategy {strategy_id} not found")
        
        # In a real implementation, this would update the database
        return {
            "strategy_id": strategy_id,
            "status": status.value,
            "updated_at": datetime.now().isoformat(),
            "notes": notes
        }
