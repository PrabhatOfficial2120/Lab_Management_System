#!/usr/bin/env python
"""
Database Connection Test Script
Tests connection to MySQL database and displays tables
"""

import os
import sys
import pymysql
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'lab'

def test_mysql_connection():
    """Test direct MySQL connection (without database)"""
    print("=" * 60)
    print("TEST 1: Direct MySQL Connection")
    print("=" * 60)
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Successfully connected to MySQL!")
        print(f"   Host: {DB_HOST}")
        print(f"   User: {DB_USER}")
        
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        print("\n📊 Available Databases:")
        for db in databases:
            print(f"   - {db[0]}")
        
        if ('lab',) in databases:
            print("\n✅ 'lab' database EXISTS!")
        else:
            print("\n❌ 'lab' database NOT FOUND!")
            print("   → You need to create it first")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to connect to MySQL: {e}")
        return False

def test_database_tables():
    """Test connection to specific database and list tables"""
    print("\n" + "=" * 60)
    print("TEST 2: Database Tables & Schema")
    print("=" * 60)
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print(f"✅ Connected to database: {DB_NAME}")
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n📋 Tables in '{DB_NAME}' database:")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESC {table_name};")
                columns = cursor.fetchall()
                print(f"\n   📌 Table: {table_name}")
                print(f"      Columns: {len(columns)}")
                for col in columns:
                    print(f"         • {col[0]} ({col[1]})")
        else:
            print(f"\n⚠️  No tables found in '{DB_NAME}' database")
            print("   → You need to import the schema from ww.sql")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to connect to database '{DB_NAME}': {e}")
        return False

def test_flask_connection():
    """Test Flask SQLAlchemy connection"""
    print("\n" + "=" * 60)
    print("TEST 3: Flask SQLAlchemy Connection")
    print("=" * 60)
    try:
        # Import Flask app
        os.chdir(os.path.join(os.path.dirname(__file__), 'project'))
        from main import app, db
        
        with app.app_context():
            # Try to execute a simple query
            result = db.session.execute("SELECT 1")
            print("✅ Flask SQLAlchemy connected successfully!")
            print(f"   Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Try to reflect tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"\n✅ Flask can access {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("\n⚠️  No tables accessible via Flask")
        
        return True
    except Exception as e:
        print(f"❌ Flask connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  DATABASE CONNECTION TEST".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    # Test 1: MySQL Connection
    results.append(("MySQL Connection", test_mysql_connection()))
    
    # Test 2: Database Tables
    results.append(("Database Tables", test_database_tables()))
    
    # Test 3: Flask Connection
    results.append(("Flask SQLAlchemy", test_flask_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed! Database is properly configured!")
    else:
        print("\n⚠️  Some tests failed. See details above.")

if __name__ == '__main__':
    main()
