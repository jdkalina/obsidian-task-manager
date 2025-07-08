#!/usr/bin/env python3
"""
Setup script for Obsidian Task Manager
Helps configure the correct paths in both scripts
"""

import os
import re
from pathlib import Path


def find_obsidian_vault():
    """Try to find common Obsidian vault locations"""
    common_paths = [
        Path.home() / "Documents" / "ObsidianVault",
        Path.home() / "Documents" / "Obsidian",
        Path.home() / "Documents" / "Notes",
        Path.home() / "ObsidianVault",
        Path.home() / "Obsidian",
    ]
    
    for path in common_paths:
        if path.exists():
            return str(path)
    return None


def update_script_path(script_path, new_obsidian_path):
    """Update the obsidian_path in a script file"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the obsidian_path line
        pattern = r'obsidian_path = r["\'].*?["\']'
        replacement = f'obsidian_path = r"{new_obsidian_path}"'
        
        updated_content = re.sub(pattern, replacement, content)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        return True
    except Exception as e:
        print(f"Error updating {script_path}: {e}")
        return False


def main():
    print("🔧 Obsidian Task Manager Setup")
    print("=" * 40)
    
    # Try to find Obsidian vault automatically
    auto_path = find_obsidian_vault()
    if auto_path:
        print(f"📁 Found possible Obsidian vault: {auto_path}")
        use_auto = input("Use this path? (y/n): ").lower().strip()
        if use_auto == 'y':
            obsidian_path = auto_path
        else:
            obsidian_path = input("Enter your Obsidian vault path: ").strip()
    else:
        print("📁 Could not auto-detect Obsidian vault")
        obsidian_path = input("Enter your Obsidian vault path: ").strip()
    
    # Validate path
    if not os.path.exists(obsidian_path):
        print(f"❌ Path does not exist: {obsidian_path}")
        return
    
    print(f"✅ Using Obsidian vault: {obsidian_path}")
    
    # Update both scripts
    scripts = ['task_tracker.py', 'task_logger.py']
    updated_count = 0
    
    for script in scripts:
        if os.path.exists(script):
            if update_script_path(script, obsidian_path):
                print(f"✅ Updated {script}")
                updated_count += 1
            else:
                print(f"❌ Failed to update {script}")
        else:
            print(f"⚠️  Script not found: {script}")
    
    if updated_count == len(scripts):
        print("🎉 Setup completed successfully!")
        print("You can now run the scripts:")
        print("  - task_tracker.py")
        print("  - task_logger.py")
    else:
        print("⚠️  Setup completed with some issues")


if __name__ == "__main__":
    main()
