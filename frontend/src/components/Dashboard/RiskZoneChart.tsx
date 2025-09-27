import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { RiskZoneDistribution } from '@/types';

interface RiskZoneChartProps {
  data: RiskZoneDistribution;
}

const RiskZoneChart: React.FC<RiskZoneChartProps> = ({ data }) => {
  const chartData = [
    { name: 'Low Risk Zone (Green)', value: data['Low Risk Zone (Green)'] || 0, color: '#10B981' },
    { name: 'Medium Risk Zone (Orange)', value: data['Medium Risk Zone (Orange)'] || 0, color: '#F59E0B' },
    { name: 'High Risk Zone (Red)', value: data['High Risk Zone (Red)'] || 0, color: '#EF4444' },
  ];

  const total = chartData.reduce((sum, item) => sum + item.value, 0);

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      const percentage = ((data.value / total) * 100).toFixed(1);
      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg">
          <p className="font-medium">{data.name}</p>
          <p className="text-sm text-gray-600">
            {data.value} employees ({percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-soft">
      <CardHeader className="bg-gradient-to-r from-green-50 to-blue-50 border-b border-green-100">
        <CardTitle className="text-xl font-bold text-gray-900 flex items-center">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-green-500 to-blue-500 flex items-center justify-center text-white mr-3">
            📊
          </div>
          Risk Zone Distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={120}
                paddingAngle={5}
                dataKey="value"
                stroke="#fff"
                strokeWidth={2}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-6 grid grid-cols-1 gap-3">
          {chartData.map((item, index) => (
            <div key={item.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div
                  className="w-4 h-4 rounded-full shadow-sm"
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-sm font-medium text-gray-700">{item.name}</span>
              </div>
              <div className="text-right">
                <span className="text-lg font-bold text-gray-900">{item.value.toLocaleString()}</span>
                <div className="text-xs text-gray-500">
                  {total > 0 ? ((item.value / total) * 100).toFixed(1) : 0}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default RiskZoneChart;
