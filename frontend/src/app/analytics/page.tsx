'use client';

import React from 'react';
import Sidebar from '../../components/Navigation/Sidebar';
import AnalyticsDashboard from '../../components/Dashboard/AnalyticsDashboard';

export default function AnalyticsPage() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <h2 className="text-2xl font-semibold text-gray-900">Analytics Dashboard</h2>
            <p className="text-sm text-gray-600">Detailed analytics and insights about employee turnover</p>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <AnalyticsDashboard />
        </main>
      </div>
    </div>
  );
}