'use client';

import React from 'react';
import Sidebar from '../../components/Navigation/Sidebar';
import EmployeesDashboard from '../../components/Employees/EmployeesDashboard';

export default function EmployeesPage() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <h2 className="text-2xl font-semibold text-gray-900">Employee Management</h2>
            <p className="text-sm text-gray-600">Manage employee data and view individual details</p>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <EmployeesDashboard />
        </main>
      </div>
    </div>
  );
}