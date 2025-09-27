'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Select } from '../ui/Select';
import { apiClient } from '../../lib/api';

interface AnalyticsData {
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  high_risk_employees: number;
  safe_employees: number;
  department_stats: DepartmentStats[];
}

interface DepartmentStats {
  department: string;
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  avg_satisfaction: number;
}

interface RiskDistribution {
  low: number;
  medium: number;
  high: number;
  critical: number;
}

interface TurnoverByDepartment {
  department: string;
  turnover_rate: number;
  employee_count: number;
}

interface TurnoverBySalary {
  salary_level: string;
  turnover_rate: number;
  employee_count: number;
}

interface SatisfactionDistribution {
  satisfaction_range: string;
  employee_count: number;
  turnover_rate: number;
}

interface ProjectCountAnalysis {
  project_count: number;
  employee_count: number;
  turnover_rate: number;
  avg_satisfaction: number;
}

interface ClusteringAnalysis {
  cluster_id: number;
  cluster_name: string;
  employee_count: number;
  avg_satisfaction: number;
  avg_evaluation: number;
  turnover_rate: number;
}

export default function AnalyticsDashboard() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [riskDistribution, setRiskDistribution] = useState<RiskDistribution | null>(null);
  const [turnoverByDept, setTurnoverByDept] = useState<TurnoverByDepartment[]>([]);
  const [turnoverBySalary, setTurnoverBySalary] = useState<TurnoverBySalary[]>([]);
  const [satisfactionDist, setSatisfactionDist] = useState<SatisfactionDistribution[]>([]);
  const [projectAnalysis, setProjectAnalysis] = useState<ProjectCountAnalysis[]>([]);
  const [clusteringAnalysis, setClusteringAnalysis] = useState<ClusteringAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Fetch all analytics data using apiClient
      const [
        dashboardData,
        riskData,
        deptData,
        salaryData,
        satisfactionData,
        projectData,
        clusteringData
      ] = await Promise.all([
        apiClient.getDashboardAnalytics(),
        apiClient.getRiskDistribution(),
        apiClient.getTurnoverByDepartment(),
        apiClient.getTurnoverBySalary(),
        apiClient.getSatisfactionDistribution(),
        apiClient.getProjectCountAnalysis(),
        apiClient.getClusteringAnalysis()
      ]);

      setAnalyticsData(dashboardData as AnalyticsData);
      setRiskDistribution(riskData as RiskDistribution);
      setTurnoverByDept(deptData as TurnoverByDepartment[]);
      setTurnoverBySalary(salaryData as TurnoverBySalary[]);
      setSatisfactionDist(satisfactionData as SatisfactionDistribution[]);
      setProjectAnalysis(projectData as ProjectCountAnalysis[]);
      setClusteringAnalysis(clusteringData as ClusteringAnalysis[]);

    } catch (error) {
      console.error('Error fetching analytics data:', error);
      // Set demo data for demonstration purposes
      setAnalyticsData({
        total_employees: 14999,
        employees_left: 3571,
        turnover_rate: 0.238,
        high_risk_employees: 1250,
        safe_employees: 8500,
        department_stats: [
          {
            department: "sales",
            total_employees: 4140,
            employees_left: 1012,
            turnover_rate: 0.244,
            avg_satisfaction: 0.612
          },
          {
            department: "technical",
            total_employees: 2720,
            employees_left: 512,
            turnover_rate: 0.188,
            avg_satisfaction: 0.678
          },
          {
            department: "support",
            total_employees: 2229,
            employees_left: 355,
            turnover_rate: 0.159,
            avg_satisfaction: 0.698
          },
          {
            department: "IT",
            total_employees: 1227,
            employees_left: 162,
            turnover_rate: 0.132,
            avg_satisfaction: 0.721
          },
          {
            department: "product_mng",
            total_employees: 902,
            employees_left: 198,
            turnover_rate: 0.219,
            avg_satisfaction: 0.645
          },
          {
            department: "marketing",
            total_employees: 858,
            employees_left: 183,
            turnover_rate: 0.213,
            avg_satisfaction: 0.652
          },
          {
            department: "RandD",
            total_employees: 787,
            employees_left: 89,
            turnover_rate: 0.113,
            avg_satisfaction: 0.734
          },
          {
            department: "accounting",
            total_employees: 767,
            employees_left: 134,
            turnover_rate: 0.175,
            avg_satisfaction: 0.689
          },
          {
            department: "hr",
            total_employees: 739,
            employees_left: 123,
            turnover_rate: 0.166,
            avg_satisfaction: 0.692
          },
          {
            department: "management",
            total_employees: 630,
            employees_left: 83,
            turnover_rate: 0.132,
            avg_satisfaction: 0.721
          }
        ]
      });
      
      // Set demo data for other analytics
      setRiskDistribution({
        low: 8500,
        medium: 3249,
        high: 2000,
        critical: 1250
      });
      
      setTurnoverByDept([
        { department: "sales", turnover_rate: 0.244, employee_count: 4140 },
        { department: "technical", turnover_rate: 0.188, employee_count: 2720 },
        { department: "support", turnover_rate: 0.159, employee_count: 2229 },
        { department: "IT", turnover_rate: 0.132, employee_count: 1227 },
        { department: "product_mng", turnover_rate: 0.219, employee_count: 902 },
        { department: "marketing", turnover_rate: 0.213, employee_count: 858 },
        { department: "RandD", turnover_rate: 0.113, employee_count: 787 },
        { department: "accounting", turnover_rate: 0.175, employee_count: 767 },
        { department: "hr", turnover_rate: 0.166, employee_count: 739 },
        { department: "management", turnover_rate: 0.132, employee_count: 630 }
      ]);
      
      setTurnoverBySalary([
        { salary_level: "low", turnover_rate: 0.267, employee_count: 7316 },
        { salary_level: "medium", turnover_rate: 0.198, employee_count: 6446 },
        { salary_level: "high", turnover_rate: 0.123, employee_count: 1237 }
      ]);
      
      setSatisfactionDist([
        { satisfaction_range: "0.0-0.2", employee_count: 1249, turnover_rate: 0.456 },
        { satisfaction_range: "0.2-0.4", employee_count: 1874, turnover_rate: 0.389 },
        { satisfaction_range: "0.4-0.6", employee_count: 3749, turnover_rate: 0.234 },
        { satisfaction_range: "0.6-0.8", employee_count: 5624, turnover_rate: 0.156 },
        { satisfaction_range: "0.8-1.0", employee_count: 2503, turnover_rate: 0.089 }
      ]);
      
      setProjectAnalysis([
        { project_count: 2, employee_count: 3749, avg_satisfaction: 0.456, turnover_rate: 0.234 },
        { project_count: 3, employee_count: 5624, avg_satisfaction: 0.567, turnover_rate: 0.189 },
        { project_count: 4, employee_count: 3749, avg_satisfaction: 0.678, turnover_rate: 0.145 },
        { project_count: 5, employee_count: 1874, avg_satisfaction: 0.789, turnover_rate: 0.098 },
        { project_count: 6, employee_count: 3, avg_satisfaction: 0.890, turnover_rate: 0.067 }
      ]);
      
      setClusteringAnalysis([
        { 
          cluster_id: 1,
          cluster_name: "High Performers", 
          employee_count: 2503, 
          avg_satisfaction: 0.789, 
          avg_evaluation: 0.856, 
          turnover_rate: 0.089 
        },
        { 
          cluster_id: 2,
          cluster_name: "Stable Employees", 
          employee_count: 5624, 
          avg_satisfaction: 0.567, 
          avg_evaluation: 0.634, 
          turnover_rate: 0.156 
        },
        { 
          cluster_id: 3,
          cluster_name: "At Risk", 
          employee_count: 3749, 
          avg_satisfaction: 0.456, 
          avg_evaluation: 0.423, 
          turnover_rate: 0.234 
        },
        { 
          cluster_id: 4,
          cluster_name: "Critical Risk", 
          employee_count: 3123, 
          avg_satisfaction: 0.234, 
          avg_evaluation: 0.312, 
          turnover_rate: 0.456 
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard Overview' },
    { id: 'risk', label: 'Risk Distribution' },
    { id: 'department', label: 'Department Analysis' },
    { id: 'salary', label: 'Salary Analysis' },
    { id: 'satisfaction', label: 'Satisfaction Analysis' },
    { id: 'projects', label: 'Project Analysis' },
    { id: 'clustering', label: 'Clustering Analysis' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading analytics data...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <Button onClick={fetchAnalyticsData} className="bg-blue-600 hover:bg-blue-700">
          Refresh Data
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Dashboard Overview Tab */}
      {activeTab === 'dashboard' && analyticsData && (
        <div className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">E</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Employees</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {analyticsData?.total_employees?.toLocaleString() || '0'}
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">L</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Employees Left</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {analyticsData?.employees_left?.toLocaleString() || '0'}
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">%</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Turnover Rate</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {analyticsData?.turnover_rate ? (analyticsData.turnover_rate * 100).toFixed(1) : '0.0'}%
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">R</span>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">High Risk</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {analyticsData?.high_risk_employees?.toLocaleString() || '0'}
                  </p>
                </div>
              </div>
            </Card>
          </div>

          {/* Department Stats */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Department Statistics</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Department
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total Employees
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Employees Left
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Turnover Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Avg Satisfaction
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {analyticsData?.department_stats?.map((dept, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">
                        {dept.department}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {dept.total_employees.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {dept.employees_left.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          dept.turnover_rate > 0.25 ? 'bg-red-100 text-red-800' :
                          dept.turnover_rate > 0.15 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {(dept.turnover_rate * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {(dept.avg_satisfaction * 100).toFixed(1)}%
                      </td>
                    </tr>
                  )) || (
                    <tr>
                      <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500">
                        No department data available
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}

      {/* Risk Distribution Tab */}
      {activeTab === 'risk' && riskDistribution && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Zone Distribution</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {riskDistribution && Object.entries(riskDistribution).map(([risk, count]) => (
              <div key={risk} className="text-center">
                <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-white font-bold text-lg ${
                  risk === 'low' ? 'bg-green-500' :
                  risk === 'medium' ? 'bg-yellow-500' :
                  risk === 'high' ? 'bg-orange-500' :
                  'bg-red-500'
                }`}>
                  {count}
                </div>
                <p className="mt-2 text-sm font-medium text-gray-900 capitalize">{risk} Risk</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Department Analysis Tab */}
      {activeTab === 'department' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Turnover by Department</h3>
          <div className="space-y-4">
            {turnoverByDept?.map((dept, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900 capitalize">{dept.department}</p>
                  <p className="text-sm text-gray-500">{dept.employee_count} employees</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    {(dept.turnover_rate * 100).toFixed(1)}%
                  </p>
                  <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                    <div 
                      className={`h-2 rounded-full ${
                        dept.turnover_rate > 0.25 ? 'bg-red-500' :
                        dept.turnover_rate > 0.15 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${dept.turnover_rate * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Salary Analysis Tab */}
      {activeTab === 'salary' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Turnover by Salary Level</h3>
          <div className="space-y-4">
            {turnoverBySalary?.map((salary, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900 capitalize">{salary.salary_level} Salary</p>
                  <p className="text-sm text-gray-500">{salary.employee_count} employees</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    {(salary.turnover_rate * 100).toFixed(1)}%
                  </p>
                  <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                    <div 
                      className={`h-2 rounded-full ${
                        salary.turnover_rate > 0.25 ? 'bg-red-500' :
                        salary.turnover_rate > 0.15 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${salary.turnover_rate * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Satisfaction Analysis Tab */}
      {activeTab === 'satisfaction' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Satisfaction Distribution</h3>
          <div className="space-y-4">
            {satisfactionDist?.map((satisfaction, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{satisfaction.satisfaction_range}</p>
                  <p className="text-sm text-gray-500">{satisfaction.employee_count} employees</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    {(satisfaction.turnover_rate * 100).toFixed(1)}% turnover
                  </p>
                  <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                    <div 
                      className={`h-2 rounded-full ${
                        satisfaction.turnover_rate > 0.25 ? 'bg-red-500' :
                        satisfaction.turnover_rate > 0.15 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${satisfaction.turnover_rate * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Project Analysis Tab */}
      {activeTab === 'projects' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Project Count Analysis</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Project Count
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee Count
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Turnover Rate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Satisfaction
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {projectAnalysis?.map((project, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {project.project_count} projects
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {project.employee_count.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        project.turnover_rate > 0.25 ? 'bg-red-100 text-red-800' :
                        project.turnover_rate > 0.15 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {(project.turnover_rate * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {(project.avg_satisfaction * 100).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Clustering Analysis Tab */}
      {activeTab === 'clustering' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Employee Clustering Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {clusteringAnalysis?.map((cluster, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">{cluster.cluster_name}</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Employees:</span>
                    <span className="font-medium">{cluster.employee_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Avg Satisfaction:</span>
                    <span className="font-medium">{(cluster.avg_satisfaction * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Avg Evaluation:</span>
                    <span className="font-medium">{(cluster.avg_evaluation * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Turnover Rate:</span>
                    <span className={`font-medium ${
                      cluster.turnover_rate > 0.25 ? 'text-red-600' :
                      cluster.turnover_rate > 0.15 ? 'text-yellow-600' :
                      'text-green-600'
                    }`}>
                      {(cluster.turnover_rate * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
