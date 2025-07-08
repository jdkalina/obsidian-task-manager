# Obsidian Task Manager

A Python-based task management system for Obsidian that automates the workflow of moving completed tasks through different stages.

## 🎯 Overview

This project provides two Python scripts that work together to manage tasks in your Obsidian vault:

1. **Task Tracker** - Moves completed tasks from daily notes to a tracker
2. **Task Logger** - Moves reviewed tasks from tracker to a permanent log

## 📁 File Structure

```
ObsidianVault/
├── YYYY-MM-DD.md       # Daily task files
├── 00 Tracker.md       # Temporary completed tasks
└── 01 Logger.md        # Permanent task history
```

## 🔄 Workflow

### Stage 1: Daily Tasks → Tracker
```
Daily file (2025-07-07.md):
- [x] Complete project documentation

Tracker (00 Tracker.md):
- [ ] [[Project]] - Complete project documentation - 2025-07-07
```

### Stage 2: Tracker → Logger
```
Tracker (00 Tracker.md):
- [x] [[Project]] - Complete project documentation - 2025-07-07

Logger (01 Logger.md):
2025-07-07 - [[Project]] - Complete project documentation
```

## 🚀 Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/jdkalina/obsidian-task-manager.git
   cd obsidian-task-manager
   ```

2. **Update the paths** in both scripts:
   - Edit `task_tracker.py` and `task_logger.py`
   - Change `obsidian_path` to your Obsidian vault location

## 📖 Usage

### Option 1: Batch Files (Windows)
- **Single scripts**: 
  - `run_task_tracker.bat` - Process daily files
  - `run_task_logger.bat` - Process tracker file
- **Combined**: `run_both_scripts.bat` - Run both scripts

### Option 2: Command Line
```bash
# Move completed daily tasks to tracker
python task_tracker.py

# Move checked tracker items to logger
python task_logger.py
```

## 🛠 Scripts

### `task_tracker.py`
- **Input**: Latest `YYYY-MM-DD.md` file with checked items
- **Output**: Moves checked items to `00 Tracker.md`
- **Features**: 
  - Preserves parent hierarchy
  - Adds source date timestamp
  - Removes completed items from daily file

### `task_logger.py`
- **Input**: `00 Tracker.md` file with checked items
- **Output**: Moves checked items to `01 Logger.md`
- **Features**:
  - Clean format (date-first)
  - No checkboxes in final log
  - Removes processed items from tracker

## 📋 Requirements

- Python 3.6+
- Obsidian vault with markdown files
- Windows (batch files) or any OS (Python directly)

## 🔧 Configuration

Update the `obsidian_path` variable in both scripts:

```python
# Example paths
obsidian_path = r"C:\Users\YourName\Documents\ObsidianVault"
obsidian_path = "/Users/YourName/Documents/ObsidianVault"  # Mac/Linux
```

## 📝 File Formats

### Daily Files (YYYY-MM-DD.md)
```markdown
- [ ] [[Project A]]
  - [ ] [[Task 1]]
    - [x] Subtask completed
  - [ ] [[Task 2]]
- [x] [[Project B]] - Simple completed task
```

### Tracker File (00 Tracker.md)
```markdown
# Task Tracker

## Completed Tasks - 2025-07-07 14:30

- [ ] [[Project A]] - [[Task 1]] - Subtask completed - 2025-07-07
- [ ] [[Project B]] - Simple completed task - 2025-07-07
```

### Logger File (01 Logger.md)
```
2025-07-07 - [[Project A]] - [[Task 1]] - Subtask completed
2025-07-07 - [[Project B]] - Simple completed task
```

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Created for Obsidian users who want to automate their task management workflow!** 🎉
