'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import Sidebar from '../../components/Navigation/Sidebar';
import AnalyticsDashboard from '../../components/Dashboard/AnalyticsDashboard';
import PredictionsDashboard from '../../components/Predictions/PredictionsDashboard';
import EmployeesDashboard from '../../components/Employees/EmployeesDashboard';
import AdminDashboard from '../../components/Admin/AdminDashboard';
import { apiClient } from '../../lib/api';

interface DashboardStats {
  total_employees: number;
  employees_left: number;
  turnover_rate: number;
  high_risk_employees: number;
  safe_employees: number;
  department_stats: Array<{
    department: string;
    total_employees: number;
    employees_left: number;
    turnover_rate: number;
    avg_satisfaction: number;
  }>;
}

export default function Dashboard() {
  const [activeView, setActiveView] = useState('overview');
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/landing';
      return;
    }
    setIsAuthenticated(true);
    // Only fetch dashboard stats if authenticated
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getDashboardAnalytics();
      setDashboardStats(data);
      } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

  const renderActiveView = () => {
    switch (activeView) {
      case 'analytics':
        return <AnalyticsDashboard />;
      case 'employees':
        return <EmployeesDashboard />;
      case 'predictions':
        return <PredictionsDashboard />;
      case 'admin':
        return <AdminDashboard />;
      default:
        return (
          <div className="space-y-6">
            {/* Welcome Section */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white">
              <h1 className="text-4xl font-bold mb-2">Welcome to Employee Turnover Prediction System</h1>
              <p className="text-xl opacity-90">
                Monitor, predict, and prevent employee turnover with AI-powered insights
              </p>
            </div>

            {/* Quick Stats */}
            {dashboardStats && (
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
                        {dashboardStats.total_employees.toLocaleString()}
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
                        {dashboardStats.employees_left.toLocaleString()}
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
                        {(dashboardStats.turnover_rate * 100).toFixed(1)}%
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
                        {dashboardStats.high_risk_employees.toLocaleString()}
                      </p>
                    </div>
                  </div>
                </Card>
              </div>
            )}

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setActiveView('analytics')}>
                <div className="text-center">
                  <div className="text-4xl mb-4">📈</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Analytics</h3>
                  <p className="text-gray-600 text-sm">View detailed analytics and insights about employee turnover patterns</p>
                  <Button className="mt-4 w-full bg-blue-600 hover:bg-blue-700">
                    View Analytics
                  </Button>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setActiveView('predictions')}>
                <div className="text-center">
                  <div className="text-4xl mb-4">🔮</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Predictions</h3>
                  <p className="text-gray-600 text-sm">Make predictions and analyze employee turnover risk</p>
                  <Button className="mt-4 w-full bg-purple-600 hover:bg-purple-700">
                    Make Predictions
                  </Button>
                </div>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setActiveView('employees')}>
                <div className="text-center">
                  <div className="text-4xl mb-4">👥</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Employees</h3>
                  <p className="text-gray-600 text-sm">Manage employee data and view individual details</p>
                  <Button className="mt-4 w-full bg-green-600 hover:bg-green-700">
                    Manage Employees
                  </Button>
                </div>
              </Card>
            </div>

            {/* Department Overview */}
            {dashboardStats && (
              <Card className="p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Department Overview</h3>
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
                      {dashboardStats.department_stats.map((dept, index) => (
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
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            )}

            {/* Recent Activity */}
            <Card className="p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-900">System started successfully</span>
                  <span className="text-xs text-gray-500 ml-auto">2 minutes ago</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-sm text-gray-900">New prediction made for employee EMP_001</span>
                  <span className="text-xs text-gray-500 ml-auto">5 minutes ago</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-sm text-gray-900">Analytics data refreshed</span>
                  <span className="text-xs text-gray-500 ml-auto">10 minutes ago</span>
                </div>
              </div>
            </Card>
          </div>
        );
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Checking authentication...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navigation */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">
                  {activeView === 'overview' && 'Dashboard Overview'}
                  {activeView === 'analytics' && 'Analytics Dashboard'}
                  {activeView === 'employees' && 'Employee Management'}
                  {activeView === 'predictions' && 'Predictions Dashboard'}
                  {activeView === 'admin' && 'Admin Dashboard'}
                </h2>
                <p className="text-sm text-gray-600">
                  {activeView === 'overview' && 'Monitor key metrics and system overview'}
                  {activeView === 'analytics' && 'Detailed analytics and insights'}
                  {activeView === 'employees' && 'Manage employee data and information'}
                  {activeView === 'predictions' && 'Make predictions and analyze risk'}
                  {activeView === 'admin' && 'System administration and settings'}
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <Button
                  onClick={() => setActiveView('overview')}
                  className="bg-gray-600 hover:bg-gray-700"
                >
                  ← Back to Overview
                </Button>
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-bold">U</span>
          </div>
        </div>
      </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-lg">Loading dashboard...</div>
            </div>
          ) : (
            renderActiveView()
          )}
        </main>
      </div>
    </div>
  );
}
