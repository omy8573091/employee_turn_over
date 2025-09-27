'use client';

import React from 'react';
import Sidebar from '../../components/Navigation/Sidebar';
import PredictionsDashboard from '../../components/Predictions/PredictionsDashboard';

export default function PredictionsPage() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <h2 className="text-2xl font-semibold text-gray-900">Predictions Dashboard</h2>
            <p className="text-sm text-gray-600">Make predictions and analyze employee turnover risk</p>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <PredictionsDashboard />
        </main>
      </div>
    </div>
  );
}
