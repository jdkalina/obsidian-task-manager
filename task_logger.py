#!/usr/bin/env python3
"""
Task Logger Script
Moves checked items from 00 Tracker.md to 01 Logger.md
Converts "- [x] task - date" to "date - task"
"""

import os
import re
from datetime import datetime
from pathlib import Path
import sys


class TaskLogger:
    def __init__(self, obsidian_path):
        self.obsidian_path = Path(obsidian_path)
        self.tracker_file = self.obsidian_path / "00 Tracker.md"
        self.logger_file = self.obsidian_path / "01 Logger.md"
    
    def parse_tracker_file(self):
        """Parse tracker file and extract checked items"""
        if not self.tracker_file.exists():
            print("❌ 00 Tracker.md not found")
            return [], []
        
        try:
            with open(self.tracker_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ Error reading 00 Tracker.md: {e}")
            return [], []
        
        checked_items = []
        updated_lines = []
        
        for line in lines:
            original_line = line
            line_content = line.rstrip()
            
            # Check for checked checkbox pattern: - [x] task text - date
            checkbox_match = re.match(r'^- \[x\] (.+) - (\d{4}-\d{2}-\d{2})$', line_content)
            if checkbox_match:
                task_text = checkbox_match.group(1)
                date = checkbox_match.group(2)
                
                # Create new format: date - task text
                logged_item = f"{date} - {task_text}"
                checked_items.append(logged_item)
                
                # Skip adding this line to updated_lines (remove it)
                continue
            
            # Keep all other lines
            updated_lines.append(original_line)
        
        return checked_items, updated_lines
    
    def update_tracker_file(self, updated_lines):
        """Update tracker file with checked items removed"""
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
        except Exception as e:
            print(f"❌ Error updating 00 Tracker.md: {e}")
            return False
        return True
    
    def append_to_logger(self, checked_items):
        """Append checked items to logger file"""
        if not checked_items:
            return True
        
        try:
            # Create logger file if it doesn't exist
            if not self.logger_file.exists():
                with open(self.logger_file, 'w', encoding='utf-8') as f:
                    pass  # Create empty file
            
            # Append new logged items
            with open(self.logger_file, 'a', encoding='utf-8') as f:
                for item in checked_items:
                    f.write(f"{item}\n")
            
        except Exception as e:
            print(f"❌ Error updating 01 Logger.md: {e}")
            return False
        
        return True
    
    def process_tracker(self):
        """Main processing function"""
        print("📄 Processing 00 Tracker.md")
        
        # Parse tracker file
        checked_items, updated_lines = self.parse_tracker_file()
        
        if not checked_items:
            print("ℹ️  No checked items found in tracker")
            return True
        
        print(f"✅ Found {len(checked_items)} checked items:")
        for item in checked_items:
            print(f"   • {item}")
        
        # Update tracker file (remove checked items)
        if not self.update_tracker_file(updated_lines):
            return False
        
        print(f"🔄 Updated 00 Tracker.md (removed checked items)")
        
        # Append to logger file
        if not self.append_to_logger(checked_items):
            return False
        
        print(f"📝 Added items to 01 Logger.md")
        return True


def main():
    # Configuration
    obsidian_path = r"C:\Users\jdkal\Documents\ObsidianVault"
    
    # Verify obsidian directory exists
    if not os.path.exists(obsidian_path):
        print(f"❌ Obsidian directory not found: {obsidian_path}")
        sys.exit(1)
    
    # Run task logger
    logger = TaskLogger(obsidian_path)
    success = logger.process_tracker()
    
    if success:
        print("✨ Task logging completed successfully!")
    else:
        print("❌ Task logging failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
