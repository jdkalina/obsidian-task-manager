import os
import re
from datetime import datetime
from pathlib import Path
from config import get_obsidian_path

def get_latest_daily_file(daily_logs_dir):
    """Get the most recent daily file in YYYY-MM-DD.md format."""
    daily_logs_path = Path(daily_logs_dir)
    
    if not daily_logs_path.exists():
        print(f"Daily logs directory does not exist: {daily_logs_dir}")
        return None
    
    # Pattern for daily files YYYY-MM-DD.md
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
    
    daily_files = []
    for file in daily_logs_path.iterdir():
        if file.is_file() and date_pattern.match(file.name):
            daily_files.append(file)
    
    if not daily_files:
        print("No daily files found")
        return None
    
    # Sort files by date (newest first) and return the latest
    daily_files.sort(reverse=True)
    return daily_files[0]

def remove_completed_tasks(lines):
    """Remove lines that contain completed tasks (- [x])."""
    filtered_lines = []
    
    for line in lines:
        stripped_line = line.lstrip()
        # Skip lines that are completed tasks
        if re.match(r'^- \[x\]', stripped_line):
            continue
        filtered_lines.append(line)
    
    return filtered_lines

def create_todays_file(daily_logs_dir, content):
    """Create today's daily file with the filtered content."""
    today = datetime.now().strftime('%Y-%m-%d')
    today_file_path = Path(daily_logs_dir) / f"{today}.md"
    
    # Check if today's file already exists
    if today_file_path.exists():
        user_input = input(f"Today's file ({today}.md) already exists. Overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print("Aborted. Today's file was not created.")
            return None
    
    try:
        with open(today_file_path, 'w', encoding='utf-8') as file:
            file.writelines(content)
        print(f"Created today's file: {today_file_path}")
        return today_file_path
    except Exception as e:
        print(f"Error creating today's file: {e}")
        return None

def process_latest_daily_file(daily_logs_dir):
    """Process the latest daily file and create today's file without completed tasks."""
    
    # Get the latest daily file
    latest_file = get_latest_daily_file(daily_logs_dir)
    
    if not latest_file:
        print("No daily files found to process")
        return
    
    print(f"Processing latest file: {latest_file.name}")
    
    try:
        # Read the latest file
        with open(latest_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        print(f"Original file has {len(lines)} lines")
        
        # Remove completed tasks
        filtered_lines = remove_completed_tasks(lines)
        
        completed_count = len(lines) - len(filtered_lines)
        print(f"Removed {completed_count} completed task lines")
        print(f"Remaining {len(filtered_lines)} lines for today's file")
        
        # Create today's file
        if filtered_lines:
            create_todays_file(daily_logs_dir, filtered_lines)
        else:
            print("No tasks remaining after filtering completed tasks")
            
    except Exception as e:
        print(f"Error processing file {latest_file}: {e}")

def main():
    # Configuration - Load from environment file
    daily_logs_directory = get_obsidian_path()
    
    # Process the latest daily file
    process_latest_daily_file(daily_logs_directory)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()