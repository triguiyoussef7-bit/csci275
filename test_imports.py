#!/usr/bin/env python
"""Test if all imports work correctly"""
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

try:
    print("Testing imports...")
    from flask import Flask
    print("[OK] Flask imported")
    
    from flask_sqlalchemy import SQLAlchemy
    print("[OK] SQLAlchemy imported")
    
    from flask_login import LoginManager, UserMixin
    print("[OK] Flask-Login imported")
    
    import models_eventlogic
    print("[OK] models_eventlogic imported")
    
    print()
    print("All imports successful! App should start.")
    
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
