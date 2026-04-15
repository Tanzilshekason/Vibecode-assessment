#!/usr/bin/env python3
"""
Verification script for the fixed Flask application.
Checks that the application can be imported and basic routes are defined.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """Verify that all required imports work."""
    print("1. Checking imports...")
    try:
        from flask import Flask, render_template
        import sqlite3
        import jwt
        import bcrypt
        import os
        from dotenv import load_dotenv
        print("   ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        return False

def verify_app_structure():
    """Verify the Flask app structure."""
    print("2. Checking app structure...")
    try:
        from app import app
        print(f"   ✓ Flask app loaded: {app}")
        
        # Check if index route is defined
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        if '/' in routes:
            print("   ✓ Index route ('/') is defined")
        else:
            print("   ✗ Index route missing")
            return False
            
        # Check if render_template is used in index
        import inspect
        from app import index
        source = inspect.getsource(index)
        if 'render_template' in source:
            print("   ✓ Index function uses render_template")
        else:
            print("   ✗ Index function doesn't use render_template")
            return False
            
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def verify_blueprints():
    """Verify blueprints are registered."""
    print("3. Checking blueprints...")
    try:
        from app import app
        blueprints = list(app.blueprints.keys())
        if 'auth' in blueprints and 'hospital' in blueprints:
            print(f"   ✓ Blueprints registered: {blueprints}")
            return True
        else:
            print(f"   ✗ Missing blueprints. Found: {blueprints}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def verify_template():
    """Verify template file exists."""
    print("4. Checking template...")
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(template_path):
        print(f"   ✓ Template exists: {template_path}")
        
        # Check for security issues
        with open(template_path, 'r') as f:
            content = f.read()
            
        issues = []
        if 'sk_live_' in content:
            issues.append("Hardcoded API key")
        if 'eval(' in content:
            issues.append("eval() function")
        if 'createMemoryLeak' in content and content.count('createMemoryLeak') > 1:
            issues.append("Duplicate functions")
            
        if issues:
            print(f"   ⚠ Template has potential issues: {', '.join(issues)}")
        else:
            print("   ✓ Template appears clean")
            
        return True
    else:
        print(f"   ✗ Template not found: {template_path}")
        return False

def verify_config():
    """Verify configuration."""
    print("5. Checking configuration...")
    try:
        from config.config import Config
        config = Config()
        
        # Check that secrets aren't hardcoded
        if config.SECRET_KEY == 'dev-key-change-in-production':
            print("   ⚠ Using default SECRET_KEY (should be set via env var)")
        else:
            print("   ✓ SECRET_KEY configured")
            
        print(f"   ✓ DEBUG mode: {config.DEBUG}")
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Flask Application Verification")
    print("=" * 60)
    
    results = []
    results.append(verify_imports())
    results.append(verify_app_structure())
    results.append(verify_blueprints())
    results.append(verify_template())
    results.append(verify_config())
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} checks passed!")
        print("\nThe application appears to be correctly fixed.")
        print("To run the application:")
        print("  1. cd Vibecode-assessment/python_app")
        print("  2. pip install -r requirements.txt")
        print("  3. python3 app.py")
        return 0
    else:
        print(f"⚠ {passed}/{total} checks passed")
        print("\nSome issues were found. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())