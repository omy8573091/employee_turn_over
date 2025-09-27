import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { HighRiskEmployee } from '@/types';
import { formatPercentage, formatDateTime, getRiskZoneColor } from '@/lib/utils';

interface HighRiskTableProps {
  data: HighRiskEmployee[];
}

const HighRiskTable: React.FC<HighRiskTableProps> = ({ data }) => {
  return (
    <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-soft">
      <CardHeader className="bg-gradient-to-r from-red-50 to-orange-50 border-b border-red-100">
        <CardTitle className="text-xl font-bold text-gray-900 flex items-center">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center text-white mr-3">
            ⚠️
          </div>
          High Risk Employees
          <span className="ml-2 text-sm font-normal text-gray-600">
            ({data.length} employees)
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Employee
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Department
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Salary
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Risk Level
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Probability
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Predicted
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {data.map((employee, index) => (
                <tr 
                  key={employee.employee_id} 
                  className="hover:bg-gradient-to-r hover:from-red-50 hover:to-orange-50 transition-all duration-200"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm mr-3">
                        {employee.employee_code.slice(-2)}
                      </div>
                      <div>
                        <div className="text-sm font-semibold text-gray-900">
                          {employee.employee_code}
                        </div>
                        <div className="text-xs text-gray-500">ID: {employee.employee_id}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900 capitalize">
                      {employee.department.replace('_', ' ')}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-3 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 capitalize">
                      {employee.salary}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-3 py-1 text-xs font-bold rounded-full ${getRiskZoneColor(
                        employee.risk_zone
                      )}`}
                    >
                      {employee.risk_zone}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="text-sm font-bold text-red-600">
                        {formatPercentage(employee.turnover_probability)}
                      </div>
                      <div className="ml-2 h-2 w-16 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-red-500 to-orange-500 rounded-full"
                          style={{ width: `${employee.turnover_probability * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-600">
                      {formatDateTime(employee.prediction_date)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {data.length === 0 && (
          <div className="text-center py-12">
            <div className="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">✅</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No High Risk Employees</h3>
            <p className="text-gray-500">Great news! All employees are currently in safe zones.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default HighRiskTable;
