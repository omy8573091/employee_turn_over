'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';

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
  left?: number;
  created_at?: string;
  updated_at?: string;
}

interface EmployeePrediction {
  employee_id: string;
  turnover_probability: number;
  risk_zone: 'low' | 'medium' | 'high' | 'critical';
  prediction_date: string;
  model_used: string;
  confidence_score: number;
}

interface RetentionStrategy {
  strategy_id: string;
  employee_id: string;
  risk_zone: string;
  strategy_type: string;
  description: string;
  estimated_cost: number;
  success_probability: number;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  created_at: string;
}

export default function EmployeesDashboard() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [employeePredictions, setEmployeePredictions] = useState<EmployeePrediction[]>([]);
  const [retentionStrategies, setRetentionStrategies] = useState<RetentionStrategy[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('list');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDepartment, setFilterDepartment] = useState('');
  const [filterSalary, setFilterSalary] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);

  // Form state for new employee
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
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/employees/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setEmployees(data.employees || []);
    } catch (error) {
      console.error('Error fetching employees:', error);
      // Set demo data if API fails
      setEmployees([
        {
          employee_id: "EMP001",
          satisfaction_level: 0.38,
          last_evaluation: 0.53,
          number_project: 2,
          average_monthly_hours: 157,
          time_spend_company: 3,
          work_accident: 0,
          promotion_last_5years: 0,
          department: "sales",
          salary: "low",
          left: 1,
          created_at: "2024-01-01T00:00:00Z",
          updated_at: "2024-01-01T00:00:00Z"
        },
        {
          employee_id: "EMP002",
          satisfaction_level: 0.80,
          last_evaluation: 0.86,
          number_project: 5,
          average_monthly_hours: 262,
          time_spend_company: 6,
          work_accident: 0,
          promotion_last_5years: 0,
          department: "technical",
          salary: "medium",
          left: 0,
          created_at: "2024-01-02T00:00:00Z",
          updated_at: "2024-01-02T00:00:00Z"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployeeDetails = async (employeeId: string) => {
    try {
      setLoading(true);
      
      // Fetch employee details
      const employeeResponse = await fetch(`http://localhost:8000/api/v1/employees/${employeeId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const employeeData = await employeeResponse.json();
      setSelectedEmployee(employeeData);

      // Fetch employee predictions
      const predictionsResponse = await fetch(`http://localhost:8000/api/v1/predictions/employee/${employeeId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const predictionsData = await predictionsResponse.json();
      setEmployeePredictions(predictionsData);

      // Fetch retention strategies
      const strategiesResponse = await fetch(`http://localhost:8000/api/v1/employees/${employeeId}/retention-strategies`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const strategiesData = await strategiesResponse.json();
      setRetentionStrategies(strategiesData.strategies || []);

    } catch (error) {
      console.error('Error fetching employee details:', error);
      // Set demo data if API fails
      setSelectedEmployee({
        employee_id: employeeId,
        satisfaction_level: 0.45,
        last_evaluation: 0.65,
        number_project: 3,
        average_monthly_hours: 180,
        time_spend_company: 2,
        work_accident: 0,
        promotion_last_5years: 0,
        department: "sales",
        salary: "medium",
        left: 0
      });
      setEmployeePredictions([
        {
          employee_id: employeeId,
          turnover_probability: 0.35,
          risk_zone: 'medium',
          prediction_date: '2024-01-01T00:00:00Z',
          model_used: 'random_forest',
          confidence_score: 0.85
        }
      ]);
      setRetentionStrategies([
        {
          strategy_id: `STRAT_${employeeId}_001`,
          employee_id: employeeId,
          risk_zone: 'medium',
          strategy_type: 'Career Development',
          description: 'Create a career development plan with clear promotion path',
          estimated_cost: 5000,
          success_probability: 0.7,
          status: 'pending',
          created_at: '2024-01-01T00:00:00Z'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const createEmployee = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          ...formData,
          employee_id: `EMP${Date.now()}`,
          left: 0  // Default to 0 (not left) for new employees
        })
      });
      
      if (response.ok) {
        setShowAddForm(false);
        setFormData({
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
        fetchEmployees();
        alert('Employee created successfully!');
      } else {
        alert('Failed to create employee. Please try again.');
      }
    } catch (error) {
      console.error('Error creating employee:', error);
      alert('Error creating employee. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (field: keyof Employee, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'critical': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredEmployees = employees.filter(employee => {
    const matchesSearch = employee.employee_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         employee.department.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDepartment = !filterDepartment || employee.department === filterDepartment;
    const matchesSalary = !filterSalary || employee.salary === filterSalary;
    
    return matchesSearch && matchesDepartment && matchesSalary;
  });

  const departments = [...new Set(employees.map(emp => emp.department))];
  const salaryLevels = [...new Set(employees.map(emp => emp.salary))];

  const tabs = [
    { id: 'list', label: 'Employee List' },
    { id: 'details', label: 'Employee Details' },
    { id: 'add', label: 'Add Employee' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Employees Management</h1>
        <Button onClick={fetchEmployees} className="bg-blue-600 hover:bg-blue-700">
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

      {/* Employee List Tab */}
      {activeTab === 'list' && (
        <div className="space-y-6">
          {/* Filters */}
          <Card className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
                <Input
                  placeholder="Search employees..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
                <Select
                  value={filterDepartment}
                  onChange={(e) => setFilterDepartment(e.target.value)}
                >
                  <option value="">All Departments</option>
                  {departments.map(dept => (
                    <option key={dept} value={dept}>{dept}</option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Salary Level</label>
                <Select
                  value={filterSalary}
                  onChange={(e) => setFilterSalary(e.target.value)}
                >
                  <option value="">All Salary Levels</option>
                  {salaryLevels.map(salary => (
                    <option key={salary} value={salary}>{salary}</option>
                  ))}
                </Select>
              </div>
              <div className="flex items-end">
                <Button
                  onClick={() => {
                    setSearchTerm('');
                    setFilterDepartment('');
                    setFilterSalary('');
                  }}
                  className="w-full bg-gray-600 hover:bg-gray-700"
                >
                  Clear Filters
                </Button>
              </div>
            </div>
          </Card>

          {/* Employee Table */}
          <Card className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Employees ({filteredEmployees.length})
              </h3>
              <Button
                onClick={() => setActiveTab('add')}
                className="bg-green-600 hover:bg-green-700"
              >
                Add Employee
              </Button>
            </div>

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
                      Salary
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Satisfaction
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Projects
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Years in Company
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredEmployees.map((employee, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {employee.employee_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                        {employee.department}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                        {employee.salary}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {(employee.satisfaction_level * 100).toFixed(1)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {employee.number_project}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {employee.time_spend_company} years
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          employee.left === 1 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                        }`}>
                          {employee.left === 1 ? 'Left' : 'Active'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <Button
                          onClick={() => {
                            fetchEmployeeDetails(employee.employee_id);
                            setActiveTab('details');
                          }}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          View Details
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}

      {/* Employee Details Tab */}
      {activeTab === 'details' && selectedEmployee && (
        <div className="space-y-6">
          {/* Employee Basic Info */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Employee Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div>
                <p className="text-sm font-medium text-gray-500">Employee ID</p>
                <p className="text-lg font-semibold text-gray-900">{selectedEmployee.employee_id}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Department</p>
                <p className="text-lg font-semibold text-gray-900 capitalize">{selectedEmployee.department}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Salary Level</p>
                <p className="text-lg font-semibold text-gray-900 capitalize">{selectedEmployee.salary}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Satisfaction Level</p>
                <p className="text-lg font-semibold text-gray-900">
                  {(selectedEmployee.satisfaction_level * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Last Evaluation</p>
                <p className="text-lg font-semibold text-gray-900">
                  {(selectedEmployee.last_evaluation * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Number of Projects</p>
                <p className="text-lg font-semibold text-gray-900">{selectedEmployee.number_project}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Average Monthly Hours</p>
                <p className="text-lg font-semibold text-gray-900">{selectedEmployee.average_monthly_hours}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Years in Company</p>
                <p className="text-lg font-semibold text-gray-900">{selectedEmployee.time_spend_company}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">Status</p>
                <p className="text-lg font-semibold text-gray-900">
                  {selectedEmployee.left === 1 ? 'Left' : 'Active'}
                </p>
              </div>
            </div>
          </Card>

          {/* Predictions History */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Prediction History</h3>
            {employeePredictions.length > 0 ? (
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
                    {employeePredictions.map((prediction, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(prediction.prediction_date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 text-xs rounded-full ${getRiskColor(prediction.risk_zone)}`}>
                            {prediction.risk_zone.toUpperCase()}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {(prediction.turnover_probability * 100).toFixed(1)}%
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {(prediction.confidence_score * 100).toFixed(1)}%
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
              <p className="text-gray-500 text-center py-4">No prediction history available</p>
            )}
          </Card>

          {/* Retention Strategies */}
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Retention Strategies</h3>
            {retentionStrategies.length > 0 ? (
              <div className="space-y-4">
                {retentionStrategies.map((strategy, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-900">{strategy.strategy_type}</h4>
                      <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(strategy.status)}`}>
                        {strategy.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{strategy.description}</p>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Estimated Cost:</span>
                        <span className="font-medium ml-1">${strategy.estimated_cost.toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Success Probability:</span>
                        <span className="font-medium ml-1">{(strategy.success_probability * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Created:</span>
                        <span className="font-medium ml-1">
                          {new Date(strategy.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No retention strategies available</p>
            )}
          </Card>
        </div>
      )}

      {/* Add Employee Tab */}
      {activeTab === 'add' && (
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Employee</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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

            <div className="md:col-span-2">
              <div className="flex items-center space-x-6">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="work_accident"
                    checked={formData.work_accident === 1}
                    onChange={(e) => handleFormChange('work_accident', e.target.checked ? 1 : 0)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="work_accident" className="ml-2 block text-sm text-gray-700">
                    Work Accident
                  </label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="promotion_last_5years"
                    checked={formData.promotion_last_5years === 1}
                    onChange={(e) => handleFormChange('promotion_last_5years', e.target.checked ? 1 : 0)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="promotion_last_5years" className="ml-2 block text-sm text-gray-700">
                    Promotion in Last 5 Years
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-3 mt-6">
            <Button
              onClick={() => setActiveTab('list')}
              className="bg-gray-600 hover:bg-gray-700"
            >
              Cancel
            </Button>
            <Button
              onClick={createEmployee}
              disabled={loading}
              className="bg-green-600 hover:bg-green-700"
            >
              {loading ? 'Creating...' : 'Create Employee'}
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
