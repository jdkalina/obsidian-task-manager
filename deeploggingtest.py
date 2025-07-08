#!/usr/bin/env python3
"""
Test version of task tracker to verify functionality
"""

import os
import re
from datetime import datetime
from pathlib import Path

def main():
    # Set up paths
    obsidian_path = Path(r"C:\Users\jdkal\Documents\ObsidianVault")
    
    # Find all date files
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
    date_files = []
    
    for file in os.listdir(obsidian_path):
        if date_pattern.match(file):
            date_files.append(file)
    
    print(f"Found date files: {date_files}")
    
    if date_files:
        date_files.sort(reverse=True)
        latest_file = date_files[0]
        print(f"Latest file: {latest_file}")
        
        # Read and print contents
        source_file_path = obsidian_path / latest_file
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\nContent of {latest_file}:")
        print(content)
        
        # Check for checked items
        lines = content.split('\n')
        checked_count = sum(1 for line in lines if '- [x]' in line)
        print(f"\nFound {checked_count} checked items")

if __name__ == "__main__":
    main()
