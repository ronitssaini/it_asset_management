#!/usr/bin/env python3
"""
Test script to verify the application structure and imports work correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without circular dependencies."""
    try:
        print("Testing imports...")
        
        # Test database imports
        from backend.database.session import Base, engine, SessionLocal
        print("✅ Database imports successful")
        
        # Test models imports
        from backend.models.asset import Asset
        from backend.models.user import User
        print("✅ Models imports successful")
        
        # Test dependencies
        from backend.dependencies import get_db
        print("✅ Dependencies imports successful")
        
        # Test auth imports
        from backend.auth.security import create_access_token, verify_password
        from backend.auth.dependencies import admin_required, manager_or_admin_required
        print("✅ Auth imports successful")
        
        # Test routers imports
        from backend.routers.assets import router as assets_router
        from backend.routers.upload import router as upload_router
        from backend.routers.auth import router as auth_router
        print("✅ Routers imports successful")
        
        # Test services imports
        from backend.services.excel_handler import parse_inventory
        print("✅ Services imports successful")
        
        # Test main app
        from backend.main import app
        print("✅ Main app import successful")
        
        print("\n🎉 All imports successful! No circular dependencies detected.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    try:
        print("\nTesting database connection...")
        from backend.database.session import engine
        
        # Try to connect to the database
        with engine.connect() as conn:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Note: This is expected if PostgreSQL is not running or configured.")
        return False

if __name__ == "__main__":
    print("IT Asset Management - Application Test")
    print("=" * 50)
    
    success = test_imports()
    
    if success:
        test_database_connection()
        print("\n✅ Application structure is consistent and ready to run!")
        print("\nTo start the application, run:")
        print("uvicorn backend.main:app --reload")
    else:
        print("\n❌ Application has issues that need to be fixed.")
        sys.exit(1) 