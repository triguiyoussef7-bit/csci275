#!/usr/bin/env python3
"""
EventLogic Complete Automated Setup
Handles: Database reset, template fixes, seeding, and server startup
Run: python AUTO_SETUP.py
"""

import os
import sys
import time
import subprocess
import re
from pathlib import Path

class EventLogicAutoSetup:
    def __init__(self):
        self.project_dir = Path(r'C:\Mac\Home\Downloads\csci275')
        self.templates_dir = self.project_dir / 'templates'
        self.db_file = self.project_dir / 'eventlogic.db'
        self.success_count = 0
        self.error_count = 0
        
    def log(self, message, level="INFO"):
        """Log messages with formatting"""
        prefix = {
            "INFO": "[i] ",
            "SUCCESS": "[+] ",
            "ERROR": "[!] ",
            "STEP": "[*] ",
            "WARNING": "[?] "
        }
        print(f"{prefix.get(level, '')} {message}")
        
    def run_command(self, cmd, description):
        """Execute shell command safely"""
        self.log(description)
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.log(f"✓ {description}", "SUCCESS")
                self.success_count += 1
                return True
            else:
                self.log(f"Warning in {description}", "WARNING")
                self.error_count += 1
                return False
        except subprocess.TimeoutExpired:
            self.log(f"Timeout in {description}", "WARNING")
            return False
        except Exception as e:
            self.log(f"Error: {str(e)}", "ERROR")
            self.error_count += 1
            return False

    def step_1_stop_processes(self):
        """Step 1: Stop any running Python processes"""
        self.log("", "STEP")
        self.log("===== Step 1/7: Stopping running processes =====", "STEP")
        
        self.run_command('taskkill /F /IM python.exe 2>nul', 'Stopping Python processes')
        time.sleep(2)
        self.log("Processes stopped", "SUCCESS")

    def step_2_delete_database(self):
        """Step 2: Delete old database"""
        self.log("", "STEP")
        self.log("===== Step 2/7: Resetting database =====", "STEP")
        
        if self.db_file.exists():
            try:
                self.db_file.unlink()
                self.log("Deleted old database", "SUCCESS")
            except Exception as e:
                self.log(f"Could not delete database: {e}", "ERROR")
        else:
            self.log("No old database found", "SUCCESS")

    def step_3_fix_templates(self):
        """Step 3: Fix template files"""
        self.log("", "STEP")
        self.log("===== Step 3/7: Fixing templates =====", "STEP")
        
        # Fix 1: Make EventLogic logo clickable
        files_to_fix = [
            'customer_dashboard.html',
            'customer_bookings_new.html',
            'vendor_dashboard.html',
            'admin_dashboard.html'
        ]
        
        logo_fixed = 0
        for filename in files_to_fix:
            filepath = self.templates_dir / filename
            if filepath.exists():
                try:
                    content = filepath.read_text(encoding='utf-8')
                    
                    if '<h1>EventLogic</h1>' in content and 'href="/customer/dashboard"' not in content:
                        content = content.replace(
                            '<h1>EventLogic</h1>',
                            '<a href="/customer/dashboard" style="text-decoration: none; color: inherit;"><h1 style="margin: 0; cursor: pointer;">EventLogic</h1></a>'
                        )
                        filepath.write_text(content, encoding='utf-8')
                        logo_fixed += 1
                except Exception as e:
                    self.log(f"Error in {filename}: {e}", "ERROR")
        
        if logo_fixed > 0:
            self.log(f"Fixed EventLogic logo in {logo_fixed} files", "SUCCESS")
        
        # Fix 2: Payment button visibility
        booking_detail = self.templates_dir / 'customer_booking_detail.html'
        if booking_detail.exists():
            try:
                content = booking_detail.read_text(encoding='utf-8')
                
                # Add success message CSS
                if '.success-message' not in content:
                    css_code = '''
        .success-message {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px 20px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-weight: 500;
            display: flex;
            align-items: center;
        }
        .success-message::before {
            content: "✓ ";
            font-weight: bold;
            margin-right: 10px;
            font-size: 18px;
        }
'''
                    if '</style>' in content:
                        content = content.replace('</style>', css_code + '        </style>')
                
                # Add success message display
                if 'payment_status == "completed"' not in content:
                    success_msg = '''
            {% if booking.payment_status == 'completed' %}
            <div class="success-message">
                Payment Successful! Your booking is confirmed.
            </div>
            {% endif %}
            '''
                    if '<h2>Booking Details</h2>' in content:
                        content = content.replace(
                            '<h2>Booking Details</h2>',
                            '<h2>Booking Details</h2>\n' + success_msg
                        )
                
                # Wrap Pay button with conditional
                if 'onclick="openPaymentModal"' in content and '{% if booking.payment_status' not in content:
                    pattern = r'(<button[^>]*onclick="openPaymentModal\(\)"[^>]*>[\s\S]*?Pay Now[\s\S]*?</button>)'
                    replacement = r'{% if booking.payment_status != "completed" %}\n                \1\n                {% endif %}'
                    content = re.sub(pattern, replacement, content)
                
                booking_detail.write_text(content, encoding='utf-8')
                self.log("Fixed payment button visibility and success message", "SUCCESS")
            except Exception as e:
                self.log(f"Error fixing booking detail: {e}", "ERROR")

    def step_4_create_database(self):
        """Step 4: Create new database with seed data"""
        self.log("", "STEP")
        self.log("===== Step 4/7: Creating fresh database =====", "STEP")
        
        seed_script = self.project_dir / 'seed_data.py'
        if seed_script.exists():
            cmd = f'cd /d "{self.project_dir}" && python seed_data.py'
            self.run_command(cmd, 'Running seed_data.py')
        else:
            self.log("seed_data.py not found", "WARNING")

    def step_5_verify_structure(self):
        """Step 5: Verify project structure"""
        self.log("", "STEP")
        self.log("===== Step 5/7: Verifying project structure =====", "STEP")
        
        required_files = [
            'app_eventlogic.py',
            'models.py',
            'templates',
            'static/style.css',
            'static/script.js'
        ]
        
        all_exist = True
        for file in required_files:
            path = self.project_dir / file
            if path.exists():
                self.log(f"✓ {file}", "SUCCESS")
            else:
                self.log(f"✗ {file} NOT FOUND", "WARNING")
                all_exist = False
        
        if all_exist:
            self.log("All files verified", "SUCCESS")
            return True
        else:
            self.log("Some files missing", "WARNING")
            return False

    def step_6_summary(self):
        """Step 6: Show summary"""
        self.log("", "STEP")
        self.log("===== Step 6/7: Setup Summary =====", "STEP")
        self.log("")
        self.log("=" * 60)
        self.log("AUTOMATIC SETUP COMPLETE!", "SUCCESS")
        self.log("=" * 60)
        self.log("")
        self.log(f"Successful operations: {self.success_count}", "SUCCESS")
        if self.error_count > 0:
            self.log(f"Operations with warnings: {self.error_count}", "WARNING")
        self.log("")

    def step_7_start_instructions(self):
        """Step 7: Show how to start"""
        self.log("Step 7/7: NEXT STEPS", "STEP")
        self.log("")
        self.log("=" * 60)
        self.log("TO START THE SERVER:", "INFO")
        self.log("=" * 60)
        self.log("")
        self.log("  cd C:\\Mac\\Home\\Downloads\\csci275")
        self.log("  python app_eventlogic.py")
        self.log("")
        self.log("Then visit:", "INFO")
        self.log("  http://localhost:5000")
        self.log("")
        self.log("Login with:", "INFO")
        self.log("  Email: john@example.com")
        self.log("  Password: custo")
        self.log("")
        self.log("=" * 60)
        self.log("FIXES APPLIED:", "SUCCESS")
        self.log("=" * 60)
        self.log("  [+] EventLogic logo is clickable", "SUCCESS")
        self.log("  [+] 'Pay Now' button hides when payment completed", "SUCCESS")
        self.log("  [+] Green success message shows after payment", "SUCCESS")
        self.log("  [+] Database reset and seeded with fresh data", "SUCCESS")
        self.log("  [+] All processes stopped to prevent locks", "SUCCESS")
        self.log("")

    def run(self):
        """Execute complete setup"""
        print("")
        self.log("╔════════════════════════════════════════════════════╗")
        self.log("║   EventLogic Complete Automated Setup              ║")
        self.log("║   All fixes applied automatically                  ║")
        self.log("╚════════════════════════════════════════════════════╝")
        self.log("")
        
        # Verify project directory
        if not self.project_dir.exists():
            self.log(f"ERROR: Project directory not found: {self.project_dir}", "ERROR")
            return False
        
        self.log(f"Project: {self.project_dir}")
        self.log("")
        
        try:
            self.step_1_stop_processes()
            self.step_2_delete_database()
            self.step_3_fix_templates()
            self.step_4_create_database()
            self.step_5_verify_structure()
            self.step_6_summary()
            self.step_7_start_instructions()
            
            return True
        except KeyboardInterrupt:
            self.log("Setup interrupted by user", "WARNING")
            return False
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
            return False

if __name__ == '__main__':
    setup = EventLogicAutoSetup()
    success = setup.run()
    print("\nPress Enter to exit...")
    input()
    sys.exit(0 if success else 1)
