#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/omprakash/Documents/work1/IITG/projects/employee_turn_over/backend')

def test_imports():
    print("Testing imports...")
    
    try:
        from app.api.v1.endpoints import auth
        print("✓ Auth module imported successfully")
        print(f"  Auth routes: {[route.path for route in auth.router.routes]}")
    except Exception as e:
        print(f"✗ Auth module error: {e}")
    
    try:
        from app.api.v1.endpoints import employees
        print("✓ Employees module imported successfully")
        print(f"  Employee routes: {[route.path for route in employees.router.routes]}")
    except Exception as e:
        print(f"✗ Employees module error: {e}")
    
    try:
        from app.api.v1.endpoints import analytics
        print("✓ Analytics module imported successfully")
        print(f"  Analytics routes: {[route.path for route in analytics.router.routes]}")
    except Exception as e:
        print(f"✗ Analytics module error: {e}")
    
    try:
        from app.api.v1.api import api_router
        print("✓ API router imported successfully")
        print(f"  Total routes: {len(api_router.routes)}")
    except Exception as e:
        print(f"✗ API router error: {e}")
    
    try:
        from app.main import app
        print("✓ Main app imported successfully")
        print(f"  App routes: {len(app.routes)}")
    except Exception as e:
        print(f"✗ Main app error: {e}")

if __name__ == "__main__":
    test_imports()
