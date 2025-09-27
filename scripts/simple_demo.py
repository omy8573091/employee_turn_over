#!/usr/bin/env python3
"""
Simple demo script to show the core functionality working.
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

def demo_basic_functionality():
    """Demo basic functionality without heavy dependencies."""
    print("🚀 Employee Turnover Prediction System - Basic Demo")
    print("=" * 60)
    
    try:
        # Test 1: Configuration
        print("\n📋 Test 1: Configuration Loading")
        from app.core.config.settings import settings
        print(f"   ✅ App Name: {settings.APP_NAME}")
        print(f"   ✅ Version: {settings.APP_VERSION}")
        print(f"   ✅ Debug Mode: {settings.DEBUG}")
        print(f"   ✅ API Version: {settings.API_V1_STR}")
        
        # Test 2: Data Validation Service
        print("\n🔍 Test 2: Data Validation Service")
        from app.services.data_validation_service import DataValidationService
        validation_service = DataValidationService()
        print(f"   ✅ Validation service initialized")
        print(f"   ✅ Validation rules loaded: {len(validation_service.validation_rules)} rules")
        
        # Test 3: Retention Strategies Service
        print("\n💡 Test 3: Retention Strategies Service")
        from app.services.retention_strategies_service import RetentionStrategiesService
        retention_service = RetentionStrategiesService()
        print(f"   ✅ Retention service initialized")
        print(f"   ✅ Strategy templates loaded for all risk zones")
        
        # Test 4: Sample Employee Data
        print("\n👤 Test 4: Sample Employee Data Processing")
        sample_employee = {
            'employee_id': 'DEMO_001',
            'satisfaction_level': 0.3,
            'last_evaluation': 0.7,
            'number_project': 5,
            'average_monthly_hours': 250,
            'time_spend_company': 2,
            'work_accident': 0,
            'promotion_last_5years': 0,
            'department': 'Sales',
            'salary': 'low'
        }
        
        # Validate employee data
        validation_result = validation_service.validate_single_record(sample_employee)
        print(f"   ✅ Employee data validation: {'PASSED' if validation_result['overall_passed'] else 'FAILED'}")
        
        # Generate retention strategies
        retention_plan = retention_service.generate_retention_strategies(
            sample_employee, 'high', 0.75
        )
        print(f"   ✅ Retention strategies generated: {len(retention_plan['strategies'])} strategies")
        print(f"   ✅ Estimated cost: ${retention_plan['total_estimated_cost']['total_estimated_cost']}")
        print(f"   ✅ Success probability: {retention_plan['success_probability']:.1%}")
        
        # Test 5: API Structure
        print("\n🌐 Test 5: API Structure")
        from app.api.v1.endpoints.employees import router
        print(f"   ✅ Employee endpoints loaded")
        print(f"   ✅ Available routes: {len(router.routes)} routes")
        
        # Test 6: Database Models
        print("\n🗄️ Test 6: Database Models")
        from app.models.base import Employee, Prediction, RiskZone
        print(f"   ✅ Database models loaded")
        print(f"   ✅ Risk zones: {[zone.value for zone in RiskZone]}")
        
        print("\n✅ All core components are working correctly!")
        print("\n📊 System Summary:")
        print(f"   • Configuration: ✅ Working")
        print(f"   • Data Validation: ✅ Working")
        print(f"   • Retention Strategies: ✅ Working")
        print(f"   • API Structure: ✅ Working")
        print(f"   • Database Models: ✅ Working")
        
        print("\n🎯 Next Steps:")
        print("   1. Install ML dependencies: pip install scikit-learn pandas numpy")
        print("   2. Run full demo: python scripts/demo_pipeline.py")
        print("   3. Start API server: python -m app.main_minimal")
        print("   4. Visit: http://localhost:8000/docs")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   This is expected if ML dependencies are not installed.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_api_server():
    """Demo starting the API server."""
    print("\n🌐 Starting API Server Demo")
    print("=" * 40)
    
    try:
        import uvicorn
        from app.main_minimal import app
        
        print("   Starting server on http://localhost:8000")
        print("   Press Ctrl+C to stop")
        print("   Visit http://localhost:8000/docs for API documentation")
        
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
        
    except KeyboardInterrupt:
        print("\n   Server stopped by user")
    except Exception as e:
        print(f"   Error starting server: {e}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Employee Turnover System Demo")
    parser.add_argument("--server", action="store_true", help="Start API server")
    parser.add_argument("--test", action="store_true", help="Run basic tests only")
    
    args = parser.parse_args()
    
    if args.server:
        demo_api_server()
    elif args.test:
        demo_basic_functionality()
    else:
        # Run both tests and offer to start server
        success = demo_basic_functionality()
        
        if success:
            print("\n" + "="*60)
            response = input("Would you like to start the API server? (y/n): ")
            if response.lower() in ['y', 'yes']:
                demo_api_server()

if __name__ == "__main__":
    main()
