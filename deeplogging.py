#!/usr/bin/env python3
"""
Enhanced Task Tracker Script
Moves checked items from the latest YYYY-MM-DD.md file to 00 Tracker.md
Converts checked items to unchecked and includes parent hierarchy
*** PRESERVES ORIGINAL DAILY FILES - DOES NOT MODIFY THEM ***
"""

import os
import re
from datetime import datetime
from pathlib import Path
import sys
from config import get_obsidian_path


class TaskTracker:
    def __init__(self, obsidian_path):
        self.obsidian_path = Path(obsidian_path)
        self.tracker_file = self.obsidian_path / "00 Tracker.md"
        
    def find_latest_date_file(self):
        """Find the latest YYYY-MM-DD.md file"""
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
        date_files = []
        
        for file in os.listdir(self.obsidian_path):
            if date_pattern.match(file):
                date_files.append(file)
        
        if not date_files:
            return None
        
        date_files.sort(reverse=True)
        return date_files[0]
    
    def parse_markdown_hierarchy(self, lines):
        """Parse markdown lines and extract hierarchy with checked items"""
        checked_items = []
        parent_stack = []
        
        for line in lines:
            line_content = line.rstrip()
            
            if not line_content:
                continue
            
            # Calculate indentation level
            indent_level = 0
            if line_content.startswith('\t'):
                indent_level = len(line_content) - len(line_content.lstrip('\t'))
            elif line_content.startswith('    '):
                indent_level = (len(line_content) - len(line_content.lstrip(' '))) // 4
            
            content = line_content.strip()
            
            # Check for checkbox item
            checkbox_match = re.match(r'^- \[([ x])\] (.+)$', content)
            if checkbox_match:
                is_checked = checkbox_match.group(1) == 'x'
                task_text = checkbox_match.group(2)
                
                # Adjust parent stack to current level
                parent_stack = parent_stack[:indent_level]
                
                if is_checked:
                    # Build parent hierarchy
                    parent_hierarchy = ' - '.join(parent_stack) if parent_stack else ''
                    full_text = f"{parent_hierarchy} - {task_text}" if parent_hierarchy else task_text
                    checked_items.append(full_text)
                else:
                    # Add unchecked item to parent stack
                    parent_stack.append(task_text)
        
        return checked_items
    
    def create_or_update_tracker(self, checked_items, source_date):
        """Create or update the tracker file"""
        if not checked_items:
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Create header if file doesn't exist
        if not self.tracker_file.exists():
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                f.write("# Task Tracker\n\n")
        
        # Append new completed tasks with section header
        with open(self.tracker_file, 'a', encoding='utf-8') as f:
            for item in checked_items:
                f.write(f"- [ ] {item} - {source_date}\n")
            f.write("\n")
    
    def process_latest_file(self):
        """Main processing function"""
        # Find latest date file
        latest_file = self.find_latest_date_file()
        if not latest_file:
            print("❌ No YYYY-MM-DD.md files found")
            return False
        
        # Extract date from filename (remove .md extension)
        source_date = latest_file[:-3]  # Remove '.md'
        
        source_file_path = self.obsidian_path / latest_file
        print(f"📄 Processing: {latest_file}")
        
        # Read source file
        try:
            with open(source_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ Error reading {latest_file}: {e}")
            return False
        
        # Parse and extract checked items (WITHOUT modifying the original file)
        checked_items = self.parse_markdown_hierarchy(lines)
        
        if not checked_items:
            print("ℹ️  No checked items found")
            return True
        
        print(f"✅ Found {len(checked_items)} checked items:")
        for item in checked_items:
            print(f"   • {item}")
        
        # *** REMOVED THE FILE MODIFICATION CODE ***
        # The original daily file is now preserved with all checkmarks intact
        print(f"📚 Preserved {latest_file} (kept all checkmarks for historical record)")
        
        # Update tracker file
        try:
            self.create_or_update_tracker(checked_items, source_date)
            print(f"📝 Added items to 00 Tracker.md")
        except Exception as e:
            print(f"❌ Error updating tracker: {e}")
            return False
        
        return True


def main():
    # Configuration - Load from environment file
    obsidian_path = get_obsidian_path()
    
    # Verify obsidian directory exists
    if not os.path.exists(obsidian_path):
        print(f"❌ Obsidian directory not found: {obsidian_path}")
        sys.exit(1)
    
    # Run task tracker
    tracker = TaskTracker(obsidian_path)
    success = tracker.process_latest_file()
    
    if success:
        print("✨ Task tracking completed successfully!")
    else:
        print("❌ Task tracking failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
