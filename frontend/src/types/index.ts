export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface Employee {
  id: number;
  employee_id: string;
  satisfaction_level: number;
  last_evaluation: number;
  number_project: number;
  average_monthly_hours: number;
  time_spend_company: number;
  work_accident: number;
  left: number;
  promotion_last_5years: number;
  sales: string;
  salary: string;
  created_at: string;
  updated_at?: string;
}

export interface Prediction {
  id: number;
  employee_id: number;
  turnover_probability: number;
  risk_zone: string;
  model_used: string;
  prediction_confidence: string;
  created_at: string;
  created_by: number;
}

export interface RetentionStrategy {
  id: number;
  employee_id: number;
  risk_zone: string;
  strategies: string;
  status: string;
  assigned_to?: string;
  created_at: string;
  updated_at?: string;
}

export interface AnalyticsResponse {
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  high_risk_employees: number;
  safe_employees: number;
  department_stats: DepartmentStats[];
  salary_stats: SalaryStats[];
}

export interface DepartmentStats {
  department: string;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
}

export interface SalaryStats {
  salary_level: string;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
}

export interface RiskZoneDistribution {
  safe_zone: number;
  low_risk_zone: number;
  medium_risk_zone: number;
  high_risk_zone: number;
}

export interface TurnoverByDepartment {
  department: string;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
  avg_evaluation: number;
  avg_hours: number;
}

export interface TurnoverBySalary {
  salary_level: string;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
  avg_evaluation: number;
  avg_hours: number;
}

export interface SatisfactionDistribution {
  status: string;
  avg_satisfaction: number;
  min_satisfaction: number;
  max_satisfaction: number;
  std_satisfaction: number;
}

export interface ProjectCountAnalysis {
  project_count: number;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
  avg_evaluation: number;
  avg_hours: number;
}

export interface ClusteringAnalysis {
  total_employees_analyzed: number;
  clusters: Record<string, {
    description: string;
    count: number;
    avg_satisfaction: number;
    avg_evaluation: number;
  }>;
  interpretations: Record<string, string>;
  error?: string;
}

export interface ModelPerformance {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  auc_score: number;
  model_version: string;
  training_date: string;
}

export interface HighRiskEmployee {
  id: number;
  employee_id: number;
  turnover_probability: number;
  risk_zone: string;
  model_used: string;
  prediction_confidence: string;
  created_at: string;
  created_by: number;
}
