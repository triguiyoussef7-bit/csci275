@echo off
REM Setup script with colored placeholder images and budget calculator
cls

echo.
echo ============================================================
echo [SETUP] EventLogic - Images & Budget Calculator
echo ============================================================
echo.

REM Delete old database
echo [1/3] Cleaning up old database...
if exist eventlogic.db (
    del eventlogic.db
    echo [OK] Deleted old database
) else (
    echo [OK] No old database found
)

echo.
echo [2/3] Creating fresh database and seeding data...
python seed_data.py

echo.
echo ============================================================
echo [SETUP COMPLETE!]
echo ============================================================
echo.
echo NEW FEATURES:
echo   ✓ Service images: Colored SVG placeholders with emojis
echo   ✓ Budget Calculator: Smart budget calculator with recommendations
echo   ✓ 3 Package Types: Basic, Standard, Premium
echo.
echo HOW TO ACCESS:
echo   1. Start server: double-click START_EVENTLOGIC_SERVER.bat
echo   2. Login as customer: john@example.com / customer123
echo   3. Click "Budget" in navbar or visit: http://localhost:5000/customer/budget-calculator
echo.
echo DEMO ACCOUNTS:
echo   Admin:    admin@eventlogic.com / admin123
echo   Customer: john@example.com / customer123
echo   Vendor:   venue@eventlogic.com / vendor123
echo.
pause
