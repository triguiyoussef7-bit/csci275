"""
Database migration script to add missing columns
Run this to fix the database schema
"""

import sqlite3
import os

db_path = 'database.db'

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Checking database schema...")
        
        # Check if budget column exists
        cursor.execute("PRAGMA table_info(events)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current columns: {columns}")
        
        # Add missing columns if they don't exist
        if 'budget' not in columns:
            print("Adding 'budget' column...")
            cursor.execute("ALTER TABLE events ADD COLUMN budget REAL DEFAULT 0.0")
        
        if 'estimated_cost' not in columns:
            print("Adding 'estimated_cost' column...")
            cursor.execute("ALTER TABLE events ADD COLUMN estimated_cost REAL DEFAULT 0.0")
        
        if 'event_type' not in columns:
            print("Adding 'event_type' column...")
            cursor.execute("ALTER TABLE events ADD COLUMN event_type TEXT DEFAULT 'custom'")
        
        conn.commit()
        conn.close()
        
        print("✓ Database schema updated successfully!")
        print("You can now start the Flask server: python app.py")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        print("If this doesn't work, delete database.db and restart Flask")
else:
    print("database.db not found. It will be created when you start Flask.")
