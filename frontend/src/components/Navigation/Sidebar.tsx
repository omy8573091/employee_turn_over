'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavigationItem {
  name: string;
  href: string;
  icon: string;
  description: string;
}

const navigation: NavigationItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: '📊',
    description: 'Overview and key metrics'
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: '📈',
    description: 'Detailed analytics and insights'
  },
  {
    name: 'Employees',
    href: '/employees',
    icon: '👥',
    description: 'Employee management and details'
  },
  {
    name: 'Predictions',
    href: '/predictions',
    icon: '🔮',
    description: 'Turnover predictions and risk analysis'
  },
  {
    name: 'Admin',
    href: '/admin',
    icon: '⚙️',
    description: 'System administration and settings'
  }
];

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div className={`bg-gray-900 text-white transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div>
              <h1 className="text-xl font-bold">Employee Turnover</h1>
              <p className="text-sm text-gray-400">Prediction System</p>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
          >
            <span className="text-lg">
              {isCollapsed ? '→' : '←'}
            </span>
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center p-3 rounded-lg transition-colors group ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
              title={isCollapsed ? item.name : undefined}
            >
              <span className="text-xl mr-3">{item.icon}</span>
              {!isCollapsed && (
                <div className="flex-1">
                  <div className="font-medium">{item.name}</div>
                  <div className="text-xs text-gray-400">{item.description}</div>
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Info */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-sm font-bold">U</span>
            </div>
            <div className="flex-1">
              <div className="text-sm font-medium">Admin User</div>
              <div className="text-xs text-gray-400">admin@company.com</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
