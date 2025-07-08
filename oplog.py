import os
import re
from datetime import datetime
from pathlib import Path

def get_daily_files(daily_logs_dir):
    """Get all daily files in YYYY-MM-DD.md format from the DailyLogs directory."""
    daily_logs_path = Path(daily_logs_dir)
    
    if not daily_logs_path.exists():
        print(f"Daily logs directory does not exist: {daily_logs_dir}")
        return []
    
    # Pattern for daily files YYYY-MM-DD.md
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
    
    daily_files = []
    for file in daily_logs_path.iterdir():
        if file.is_file() and date_pattern.match(file.name):
            daily_files.append(file)
    
    # Sort files by date (newest first)
    daily_files.sort(reverse=True)
    return daily_files

def extract_opportunity_link(text):
    """Extract opportunity name from [[Opportunity Name]] format."""
    match = re.search(r'\[\[([^\]]+)\]\]', text)
    return match.group(1) if match else None

def parse_completed_activities(lines):
    """Parse completed activities under opportunity parent records."""
    opportunity_activities = {}  # {opportunity_name: [activities]}
    hierarchy_stack = {}  # {depth: task_text}
    current_opportunity = None
    
    for line in lines:
        stripped_line = line.lstrip()
        indent_level = len(line) - len(stripped_line)
        
        # Check if this is a task line
        if re.match(r'^- \[[x ]\]', stripped_line):
            is_completed = stripped_line.startswith('- [x]')
            task_text = re.sub(r'^- \[[x ]\]\s*', '', stripped_line)
            
            # Calculate depth
            if line.startswith('\t'):
                depth = len(line) - len(line.lstrip('\t'))
            else:
                leading_spaces = indent_level
                if leading_spaces >= 4:
                    depth = leading_spaces // 4
                elif leading_spaces >= 2:
                    depth = leading_spaces // 2
                elif leading_spaces >= 1:
                    depth = leading_spaces
                else:
                    depth = 0
            
            # Store this task at its depth level
            hierarchy_stack[depth] = task_text
            
            # Remove deeper levels
            keys_to_remove = [k for k in hierarchy_stack.keys() if k > depth]
            for k in keys_to_remove:
                del hierarchy_stack[k]
            
            # Check if this is a top-level opportunity (depth 0)
            if depth == 0:
                opportunity_name = extract_opportunity_link(task_text)
                if opportunity_name:
                    current_opportunity = opportunity_name
                    if current_opportunity not in opportunity_activities:
                        opportunity_activities[current_opportunity] = []
            
            # If this is a completed task and we're under an opportunity
            if is_completed and current_opportunity and depth > 0:
                # Build hierarchy from level 0 to current depth, excluding the opportunity itself
                hierarchy_parts = []
                for level in sorted([k for k in hierarchy_stack.keys() if k > 0]):
                    if hierarchy_stack[level].strip():
                        hierarchy_parts.append(hierarchy_stack[level])
                
                if hierarchy_parts:
                    activity_text = ' - '.join(hierarchy_parts)
                    opportunity_activities[current_opportunity].append(activity_text)
        
        # Reset current opportunity if we hit a non-indented non-task line
        elif not line.startswith(' ') and not line.startswith('\t') and stripped_line:
            current_opportunity = None
    
    return opportunity_activities

def get_opportunity_file_path(parent_dir, opportunity_name):
    """Get the file path for an opportunity."""
    # Try common file naming patterns
    possible_names = [
        f"{opportunity_name}.md",
        f"{opportunity_name.replace(' ', '_')}.md",
        f"{opportunity_name.replace(' ', '-')}.md"
    ]
    
    parent_path = Path(parent_dir)
    
    for name in possible_names:
        file_path = parent_path / name
        if file_path.exists():
            return file_path
    
    # If file doesn't exist, create it with the first naming pattern
    return parent_path / possible_names[0]

def check_activity_exists(file_path, activity_text):
    """Check if an activity already exists in the opportunity file."""
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Check if the exact activity text exists (case-insensitive)
            return activity_text.lower() in content.lower()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

def add_activities_to_opportunity(file_path, opportunity_name, activities, date):
    """Add completed activities to an opportunity file."""
    if not activities:
        return
    
    # Filter out activities that already exist
    new_activities = [activity for activity in activities if not check_activity_exists(file_path, activity)]
    
    if not new_activities:
        print(f"All activities for {opportunity_name} already exist in the file")
        return
    
    try:
        # Read existing content if file exists
        existing_content = ""
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_content = file.read()
        
        # Append new activities
        with open(file_path, 'a', encoding='utf-8') as file:
            if existing_content and not existing_content.endswith('\n'):
                file.write('\n')
            
            file.write(f"\n## Completed Activities - {date}\n")
            for activity in new_activities:
                file.write(f"- [ ] {activity}\n")
            file.write("\n")
        
        print(f"Added {len(new_activities)} new activities to {opportunity_name}")
        for activity in new_activities:
            print(f"  - {activity}")
    
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def process_daily_file(file_path):
    """Process a single daily file and extract opportunity activities."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Remove newline characters but preserve indentation
        lines = [line.rstrip('\n') for line in lines]
        
        # Parse completed activities
        opportunity_activities = parse_completed_activities(lines)
        
        return opportunity_activities
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}

def main():
    # Configuration
    parent_directory = r'C:\Users\jdkal\Documents\ObsidianVault'
    daily_logs_directory = r'C:\Users\jdkal\Documents\ObsidianVault\DailyLogs'
    
    # Get all daily files
    daily_files = get_daily_files(daily_logs_directory)
    
    if not daily_files:
        print("No daily files found in the DailyLogs directory")
        return
    
    print(f"Found {len(daily_files)} daily files:")
    for file in daily_files[:10]:  # Show first 10 files
        print(f"  - {file.name}")
    if len(daily_files) > 10:
        print(f"  ... and {len(daily_files) - 10} more files")
    
    # Process each daily file
    all_opportunity_activities = {}
    
    for daily_file in daily_files:
        print(f"\nProcessing {daily_file.name}...")
        
        opportunity_activities = process_daily_file(daily_file)
        
        if opportunity_activities:
            date = daily_file.stem  # Gets filename without .md extension
            
            for opportunity_name, activities in opportunity_activities.items():
                print(f"Found {len(activities)} completed activities for '{opportunity_name}':")
                
                # Get opportunity file path
                opportunity_file = get_opportunity_file_path(parent_directory, opportunity_name)
                
                # Add activities to opportunity file
                add_activities_to_opportunity(opportunity_file, opportunity_name, activities, date)
                
                # Track all activities for summary
                if opportunity_name not in all_opportunity_activities:
                    all_opportunity_activities[opportunity_name] = []
                all_opportunity_activities[opportunity_name].extend(activities)
    
    # Summary
    print(f"\n{'='*50}")
    print("PROCESSING COMPLETE")
    print(f"{'='*50}")
    
    if all_opportunity_activities:
        print(f"Updated {len(all_opportunity_activities)} opportunity files:")
        for opportunity_name, activities in all_opportunity_activities.items():
            print(f"  - {opportunity_name}: {len(activities)} activities")
    else:
        print("No completed activities found under opportunity records")

if __name__ == "__main__":
    main()