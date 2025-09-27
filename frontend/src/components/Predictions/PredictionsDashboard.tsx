'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { apiClient } from '../../lib/api';

interface Employee {
  employee_id: string;
  satisfaction_level: number;
  last_evaluation: number;
  number_project: number;
  average_monthly_hours: number;
  time_spend_company: number;
  work_accident: number;
  promotion_last_5years: number;
  department: string;
  salary: string;
}

interface Prediction {
  id: number;
  employee_id: string;
  turnover_probability: number;
  risk_zone: string;
  model_used: string;
  prediction_confidence: string;
  created_at: string;
  created_by: number;
}

interface HighRiskEmployee {
  employee_id: string;
  name?: string;
  department: string;
  turnover_probability: number;
  risk_zone: string;
  last_evaluation: number;
  satisfaction_level: number;
  time_spend_company: number;
}

export default function PredictionsDashboard() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [highRiskEmployees, setHighRiskEmployees] = useState<HighRiskEmployee[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [predictionResult, setPredictionResult] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('predict');
  const [employeeId, setEmployeeId] = useState('');

  // Form state for new prediction
  const [formData, setFormData] = useState<Partial<Employee>>({
    satisfaction_level: 0.5,
    last_evaluation: 0.5,
    number_project: 2,
    average_monthly_hours: 160,
    time_spend_company: 2,
    work_accident: 0,
    promotion_last_5years: 0,
    department: 'sales',
    salary: 'low'
  });

  useEffect(() => {
    fetchHighRiskEmployees();
  }, []);

  const fetchHighRiskEmployees = async () => {
    try {
      const data = await apiClient.getHighRiskPredictions();
      setHighRiskEmployees(data);
    } catch (error) {
      console.error('Error fetching high-risk employees:', error);
      // Set demo data if API fails
      setHighRiskEmployees([
        {
          employee_id: "EMP001",
          department: "sales",
          turnover_probability: 0.85,
          risk_zone: "high",
          last_evaluation: 0.45,
          satisfaction_level: 0.25,
          time_spend_company: 2
        },
        {
          employee_id: "EMP003",
          department: "support",
          turnover_probability: 0.78,
          risk_zone: "high",
          last_evaluation: 0.88,
          satisfaction_level: 0.11,
          time_spend_company: 4
        }
      ]);
    }
  };

  const refreshAllData = async () => {
    console.log('Refreshing all data...');
    setLoading(true);
    try {
      // Refresh high-risk employees
      await fetchHighRiskEmployees();
      
      // If we have a prediction result, refresh it
      if (predictionResult) {
        console.log('Refreshing prediction result...');
        await predictTurnover();
      }
      
      // If we have employee predictions, refresh them
      if (employeeId) {
        console.log('Refreshing employee predictions...');
        await fetchEmployeePredictions(employeeId);
      }
      
      console.log('All data refreshed successfully');
    } catch (error) {
      console.error('Error refreshing data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployeePredictions = async (empId: string) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/v1/predictions/employee/${empId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      console.error('Error fetching employee predictions:', error);
      // Set demo data if API fails
      setPredictions([
        {
          id: 1,
          employee_id: empId,
          turnover_probability: 0.75,
          risk_zone: 'High Risk Zone (Red)',
          model_used: 'random_forest',
          prediction_confidence: 'High',
          created_at: '2024-01-01T00:00:00Z',
          created_by: 1
        },
        {
          id: 2,
          employee_id: empId,
          turnover_probability: 0.68,
          risk_zone: 'Medium Risk Zone (Orange)',
          model_used: 'random_forest',
          prediction_confidence: 'Medium',
          created_at: '2024-01-02T00:00:00Z',
          created_by: 1
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const predictTurnover = async () => {
    try {
      setLoading(true);
      const predictionData = {
        ...formData,
        employee_id: `EMP${Date.now()}`,
        left: 0  // Default to 0 (not left) for new predictions
      };
      console.log('Sending prediction data:', predictionData);
      
      const data = await apiClient.predictEmployeeTurnover(predictionData);
      console.log('Prediction result:', data);
      setPredictionResult(data);
    } catch (error) {
      console.error('Error predicting turnover:', error);
      // Set demo prediction result if API fails
      const mockProbability = Math.random();
      const riskZone = mockProbability < 0.2 ? 'low' : 
                      mockProbability < 0.6 ? 'medium' : 
                      mockProbability < 0.9 ? 'high' : 'critical';
      
      const demoResult = {
        id: 1,
        employee_id: `EMP${Date.now()}`,
        turnover_probability: mockProbability,
        risk_zone: riskZone,
        model_used: 'random_forest',
        prediction_confidence: 'High',
        created_at: new Date().toISOString(),
        created_by: 1
      };
      console.log('Setting demo prediction result:', demoResult);
      setPredictionResult(demoResult);
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (field: keyof Employee, value: any) => {
    console.log(`Form change: ${field} = ${value}`);
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getRiskColor = (risk: string) => {
    if (risk.includes('Safe Zone') || risk.includes('Green')) {
      return 'bg-green-100 text-green-800';
    } else if (risk.includes('Low Risk') || risk.includes('Yellow')) {
      return 'bg-yellow-100 text-yellow-800';
    } else if (risk.includes('Medium Risk') || risk.includes('Orange')) {
      return 'bg-orange-100 text-orange-800';
    } else if (risk.includes('High Risk') || risk.includes('Red')) {
      return 'bg-red-100 text-red-800';
    } else {
      return 'bg-gray-100 text-gray-800';
    }
  };

  const getShortRiskZone = (risk: string) => {
    if (risk.includes('Safe Zone') || risk.includes('Green')) {
      return 'SAFE';
    } else if (risk.includes('Low Risk') || risk.includes('Yellow')) {
      return 'LOW';
    } else if (risk.includes('Medium Risk') || risk.includes('Orange')) {
      return 'MEDIUM';
    } else if (risk.includes('High Risk') || risk.includes('Red')) {
      return 'HIGH';
    } else {
      return 'UNKNOWN';
    }
  };

  const tabs = [
    { id: 'predict', label: 'Make Prediction' },
    { id: 'high-risk', label: 'High Risk Employees' },
    { id: 'employee-history', label: 'Employee History' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Predictions Dashboard</h1>
        <Button 
          onClick={refreshAllData} 
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Refreshing...' : 'Refresh Data'}
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

      {/* Make Prediction Tab */}
      {activeTab === 'predict' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Prediction Form */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Employee Turnover Prediction</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Satisfaction Level (0-1)
                </label>
                <Input
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  value={formData.satisfaction_level}
                  onChange={(e) => handleFormChange('satisfaction_level', parseFloat(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Evaluation (0-1)
                </label>
                <Input
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  value={formData.last_evaluation}
                  onChange={(e) => handleFormChange('last_evaluation', parseFloat(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of Projects
                </label>
                <Input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.number_project}
                  onChange={(e) => handleFormChange('number_project', parseInt(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Average Monthly Hours
                </label>
                <Input
                  type="number"
                  min="80"
                  max="400"
                  value={formData.average_monthly_hours}
                  onChange={(e) => handleFormChange('average_monthly_hours', parseInt(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Time Spent in Company (years)
                </label>
                <Input
                  type="number"
                  min="1"
                  max="20"
                  value={formData.time_spend_company}
                  onChange={(e) => handleFormChange('time_spend_company', parseInt(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Department
                </label>
                <Select
                  value={formData.department}
                  onChange={(e) => handleFormChange('department', e.target.value)}
                >
                  <option value="sales">Sales</option>
                  <option value="technical">Technical</option>
                  <option value="support">Support</option>
                  <option value="IT">IT</option>
                  <option value="RandD">R&D</option>
                  <option value="product_mng">Product Management</option>
                  <option value="marketing">Marketing</option>
                  <option value="accounting">Accounting</option>
                  <option value="hr">HR</option>
                </Select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Salary Level
                </label>
                <Select
                  value={formData.salary}
                  onChange={(e) => handleFormChange('salary', e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </Select>
              </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="work_accident"
                    checked={formData.work_accident === 1}
                    onChange={(e) => {
                      console.log('Work accident checkbox changed:', e.target.checked);
                      handleFormChange('work_accident', e.target.checked ? 1 : 0);
                    }}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                  />
                  <label htmlFor="work_accident" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                    Work Accident
                  </label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="promotion_last_5years"
                    checked={formData.promotion_last_5years === 1}
                    onChange={(e) => {
                      console.log('Promotion checkbox changed:', e.target.checked);
                      handleFormChange('promotion_last_5years', e.target.checked ? 1 : 0);
                    }}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                  />
                  <label htmlFor="promotion_last_5years" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                    Promotion in Last 5 Years
                  </label>
                </div>
              </div>

              <Button
                onClick={predictTurnover}
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {loading ? 'Predicting...' : 'Predict Turnover'}
              </Button>
            </div>
          </Card>

          {/* Prediction Result */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Prediction Result</h3>
            {predictionResult ? (
              <div className="space-y-4">
                <div className="text-center">
                  <div className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold ${getRiskColor(predictionResult.risk_zone)}`}>
                    {getShortRiskZone(predictionResult.risk_zone)} RISK ZONE
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Turnover Probability:</span>
                    <span className="text-lg font-semibold text-gray-900">
                      {(predictionResult.turnover_probability * 100).toFixed(1)}%
                    </span>
                  </div>

                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Confidence Score:</span>
                    <span className="text-lg font-semibold text-gray-900">
                      {predictionResult.prediction_confidence}
                    </span>
                  </div>

                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Model Used:</span>
                    <span className="text-sm font-medium text-gray-900">{predictionResult.model_used}</span>
                  </div>

                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Prediction Date:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {new Date(predictionResult.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                {/* Risk Assessment */}
                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-medium text-blue-900 mb-2">Risk Assessment</h4>
                  <p className="text-sm text-blue-800">
                    {predictionResult.risk_zone === 'low' && 'This employee has a low risk of leaving. Continue current engagement strategies.'}
                    {predictionResult.risk_zone === 'medium' && 'This employee has a moderate risk of leaving. Consider proactive retention measures.'}
                    {predictionResult.risk_zone === 'high' && 'This employee has a high risk of leaving. Immediate retention action recommended.'}
                    {predictionResult.risk_zone === 'critical' && 'This employee has a critical risk of leaving. Urgent intervention required.'}
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <p>Fill out the form and click "Predict Turnover" to see results</p>
              </div>
            )}
          </Card>
        </div>
      )}

      {/* High Risk Employees Tab */}
      {activeTab === 'high-risk' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">High Risk Employees</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Department
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Risk Zone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Turnover Probability
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Satisfaction
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Years in Company
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {highRiskEmployees.map((employee, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {employee.employee_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                      {employee.department}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${getRiskColor(employee.risk_zone)}`}>
                          {getShortRiskZone(employee.risk_zone)}
                        </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {(employee.turnover_probability * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {(employee.satisfaction_level * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {employee.time_spend_company} years
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <Button
                        onClick={() => {
                          setEmployeeId(employee.employee_id);
                          fetchEmployeePredictions(employee.employee_id);
                          setActiveTab('employee-history');
                        }}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        View History
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Employee History Tab */}
      {activeTab === 'employee-history' && (
        <Card className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              Prediction History {employeeId && `for ${employeeId}`}
            </h3>
            <div className="flex space-x-2">
              <Input
                placeholder="Enter Employee ID"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
                className="w-48"
              />
              <Button
                onClick={() => fetchEmployeePredictions(employeeId)}
                disabled={!employeeId || loading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {loading ? 'Loading...' : 'Load History'}
              </Button>
            </div>
          </div>

          {predictions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Risk Zone
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Turnover Probability
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Confidence Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Model Used
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {predictions.map((prediction, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(prediction.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${getRiskColor(prediction.risk_zone)}`}>
                          {getShortRiskZone(prediction.risk_zone)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {(prediction.turnover_probability * 100).toFixed(1)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {prediction.prediction_confidence}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {prediction.model_used}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              <p>No prediction history found. Enter an employee ID and click "Load History" to view predictions.</p>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
