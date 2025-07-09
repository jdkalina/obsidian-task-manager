"""
Configuration module for Obsidian Task Manager
Reads environment variables from .env file
"""

import os
from pathlib import Path


def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print(f"Warning: .env file not found at {env_file}")
        return
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE format
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Set environment variable
                    os.environ[key] = value
    
    except Exception as e:
        print(f"Error loading .env file: {e}")


def get_obsidian_path():
    """Get the Obsidian vault path from environment variables"""
    # Load .env file first
    load_env_file()
    
    # Get the path from environment variable
    obsidian_path = os.getenv('OBSIDIAN_VAULT_PATH')
    
    if not obsidian_path:
        raise ValueError(
            "OBSIDIAN_VAULT_PATH not found in environment variables. "
            "Please check your .env file."
        )
    
    # Convert to Path object and verify it exists
    path = Path(obsidian_path)
    
    if not path.exists():
        print(f"Warning: Obsidian vault path does not exist: {path}")
    
    return str(path)


# For backward compatibility, you can also import the path directly
try:
    OBSIDIAN_PATH = get_obsidian_path()
except Exception as e:
    print(f"Error loading Obsidian path: {e}")
    OBSIDIAN_PATH = None


if __name__ == "__main__":
    # Test the configuration
    print("Testing configuration...")
    try:
        path = get_obsidian_path()
        print(f"✅ Obsidian vault path: {path}")
        
        # Check if path exists
        if Path(path).exists():
            print("✅ Path exists")
        else:
            print("❌ Path does not exist")
            
    except Exception as e:
        print(f"❌ Error: {e}")
