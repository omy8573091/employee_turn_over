import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import StatsCard from '@/components/Dashboard/StatsCard';
import RiskZoneChart from '@/components/Dashboard/RiskZoneChart';
import TurnoverChart from '@/components/Dashboard/TurnoverChart';
import HighRiskTable from '@/components/Dashboard/HighRiskTable';

// Mock data
const mockStatsData = {
  title: 'Total Employees',
  value: '1000',
  change: '+5%',
  changeType: 'positive' as const,
  icon: 'Users'
};

const mockRiskData = [
  { name: 'Safe Zone', value: 600, color: '#10B981' },
  { name: 'Low Risk', value: 250, color: '#F59E0B' },
  { name: 'Medium Risk', value: 100, color: '#F97316' },
  { name: 'High Risk', value: 50, color: '#EF4444' }
];

const mockTurnoverData = [
  { department: 'IT', turnover_rate: 0.15 },
  { department: 'HR', turnover_rate: 0.12 },
  { department: 'Sales', turnover_rate: 0.25 }
];

const mockHighRiskEmployees = [
  {
    id: 1,
    employee_id: 'EMP001',
    name: 'John Doe',
    department: 'IT',
    risk_score: 0.85,
    risk_zone: 'High Risk Zone (Red)',
    last_updated: '2024-01-15T10:00:00Z'
  },
  {
    id: 2,
    employee_id: 'EMP002',
    name: 'Jane Smith',
    department: 'Sales',
    risk_score: 0.75,
    risk_zone: 'Medium Risk Zone (Orange)',
    last_updated: '2024-01-15T10:00:00Z'
  }
];

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('applies correct variant styles', () => {
    render(<Button variant="outline">Outline</Button>);
    const button = screen.getByText('Outline');
    expect(button).toHaveClass('border-gray-300');
  });
});

describe('Card Component', () => {
  it('renders card with content', () => {
    render(
      <Card>
        <div>Card content</div>
      </Card>
    );
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('renders card with header', () => {
    render(
      <Card>
        <Card.Header>
          <Card.Title>Card Title</Card.Title>
        </Card.Header>
        <Card.Content>
          <div>Card content</div>
        </Card.Content>
      </Card>
    );
    expect(screen.getByText('Card Title')).toBeInTheDocument();
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });
});

describe('Input Component', () => {
  it('renders input with label', () => {
    render(<Input label="Test Label" placeholder="Enter text" />);
    expect(screen.getByText('Test Label')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('handles input changes', () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test input' } });
    expect(handleChange).toHaveBeenCalled();
  });

  it('shows error message', () => {
    render(<Input error="This is an error" />);
    expect(screen.getByText('This is an error')).toBeInTheDocument();
  });
});

describe('Select Component', () => {
  const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' }
  ];

  it('renders select with options', () => {
    render(<Select options={options} />);
    expect(screen.getByDisplayValue('Option 1')).toBeInTheDocument();
  });

  it('handles selection changes', () => {
    const handleChange = jest.fn();
    render(<Select options={options} onChange={handleChange} />);
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'option2' } });
    expect(handleChange).toHaveBeenCalled();
  });
});

describe('StatsCard Component', () => {
  it('renders stats card with data', () => {
    render(<StatsCard {...mockStatsData} />);
    expect(screen.getByText('Total Employees')).toBeInTheDocument();
    expect(screen.getByText('1000')).toBeInTheDocument();
    expect(screen.getByText('+5%')).toBeInTheDocument();
  });

  it('applies correct change type styling', () => {
    render(<StatsCard {...mockStatsData} />);
    const changeElement = screen.getByText('+5%');
    expect(changeElement).toHaveClass('text-green-600');
  });
});

describe('RiskZoneChart Component', () => {
  it('renders risk zone chart', () => {
    render(<RiskZoneChart data={mockRiskData} />);
    expect(screen.getByText('Risk Zone Distribution')).toBeInTheDocument();
  });

  it('displays risk zone data', () => {
    render(<RiskZoneChart data={mockRiskData} />);
    expect(screen.getByText('Safe Zone')).toBeInTheDocument();
    expect(screen.getByText('High Risk')).toBeInTheDocument();
  });
});

describe('TurnoverChart Component', () => {
  it('renders turnover chart', () => {
    render(<TurnoverChart data={mockTurnoverData} />);
    expect(screen.getByText('Turnover by Department')).toBeInTheDocument();
  });

  it('displays department data', () => {
    render(<TurnoverChart data={mockTurnoverData} />);
    expect(screen.getByText('IT')).toBeInTheDocument();
    expect(screen.getByText('Sales')).toBeInTheDocument();
  });
});

describe('HighRiskTable Component', () => {
  it('renders high risk table', () => {
    render(<HighRiskTable employees={mockHighRiskEmployees} />);
    expect(screen.getByText('High Risk Employees')).toBeInTheDocument();
  });

  it('displays employee data', () => {
    render(<HighRiskTable employees={mockHighRiskEmployees} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
  });

  it('shows risk scores', () => {
    render(<HighRiskTable employees={mockHighRiskEmployees} />);
    expect(screen.getByText('85%')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
  });
});

// Integration tests
describe('Component Integration', () => {
  it('renders dashboard components together', () => {
    render(
      <div>
        <StatsCard {...mockStatsData} />
        <RiskZoneChart data={mockRiskData} />
        <TurnoverChart data={mockTurnoverData} />
        <HighRiskTable employees={mockHighRiskEmployees} />
      </div>
    );

    expect(screen.getByText('Total Employees')).toBeInTheDocument();
    expect(screen.getByText('Risk Zone Distribution')).toBeInTheDocument();
    expect(screen.getByText('Turnover by Department')).toBeInTheDocument();
    expect(screen.getByText('High Risk Employees')).toBeInTheDocument();
  });
});

// Accessibility tests
describe('Accessibility', () => {
  it('button has proper accessibility attributes', () => {
    render(<Button aria-label="Submit form">Submit</Button>);
    const button = screen.getByLabelText('Submit form');
    expect(button).toBeInTheDocument();
  });

  it('input has proper label association', () => {
    render(<Input label="Email" id="email" />);
    const input = screen.getByLabelText('Email');
    expect(input).toBeInTheDocument();
  });

  it('select has proper accessibility', () => {
    const options = [{ value: 'test', label: 'Test Option' }];
    render(<Select options={options} aria-label="Choose option" />);
    const select = screen.getByLabelText('Choose option');
    expect(select).toBeInTheDocument();
  });
});
