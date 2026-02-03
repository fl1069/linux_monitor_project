#!/usr/bin/env python3
import os
import stat
from datetime import datetime
from pathlib import Path

# Use relative paths based on current script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # Go up one level from directory_monitor/

# Define all paths relative to project root
monitor_directory = os.path.join(project_root, "monitored_directory")
log_file = os.path.join(project_root, "reporting", "dir_monitor_log.txt")

# Ensure monitoring directory exists
if not os.path.exists(monitor_directory):
    os.makedirs(monitor_directory, exist_ok=True)
    print(f"Created monitoring directory: {monitor_directory}")

def get_file_metadata(filepath):
    try:
        stat_info = os.stat(filepath)
        path = Path(filepath)
        
        if stat.S_ISDIR(stat_info.st_mode):
            file_type = "directory"
        elif stat.S_ISLNK(stat_info.st_mode):
            file_type = "symbolic link"
        else:
            file_type = "regular file"
        
        return {
            'filename': path.name,
            'type': file_type,
            'size': stat_info.st_size,
            'permissions': oct(stat_info.st_mode)[-3:],
            'mtime': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'ctime': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Failed to get file metadata for {filepath}: {e}")
        return None

def log_event(event_type, filename, metadata=None, old_value=None):
    """Log directory events to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {event_type}: {filename}\n")
            if metadata:
                f.write(f"  Type: {metadata['type']}\n")
                f.write(f"  Size: {metadata['size']} bytes\n")
                f.write(f"  Permissions: {metadata['permissions']}\n")
                f.write(f"  Modified: {metadata['mtime']}\n")
            if old_value:
                f.write(f"  Previous: {old_value}\n")
            f.write("-" * 40 + "\n")
        print(f"Logged: {event_type} - {filename}")
    except Exception as e:
        print(f"Failed to write log: {e}")

def detect_and_log_changes():
    """Detect changes in directory and log them"""
    print(f"Scanning directory: {monitor_directory}")
    
    # Get current state
    current_state = {}
    try:
        files = os.listdir(monitor_directory)
        print(f"Found {len(files)} files")
        
        for filename in files:
            filepath = os.path.join(monitor_directory, filename)
            metadata = get_file_metadata(filepath)
            if metadata:
                current_state[filename] = metadata
    except Exception as e:
        print(f"Failed to scan directory: {e}")
    
    # Read previous state - store in same directory as log file
    log_dir = os.path.dirname(log_file)
    state_file = os.path.join(log_dir, ".dir_state.pkl")
    previous_state = {}
    
    if os.path.exists(state_file):
        try:
            import pickle
            with open(state_file, 'rb') as f:
                previous_state = pickle.load(f)
            print(f"Read {len(previous_state)} historical files")
        except Exception as e:
            print(f"Failed to read historical state: {e}")
    else:
        print("First run, no historical state")
    
    # Detect changes
    # 1. New files
    new_files = [f for f in current_state if f not in previous_state]
    for filename in new_files:
        log_event("FILE CREATED", filename, current_state[filename])
    
    # 2. Deleted files
    deleted_files = [f for f in previous_state if f not in current_state]
    for filename in deleted_files:
        log_event("FILE DELETED", filename)
    
    # 3. Modified files
    for filename in current_state:
        if filename in previous_state:
            old = previous_state[filename]
            new = current_state[filename]
            
            changes = []
            if old['size'] != new['size']:
                changes.append(f"size:{old['size']}->{new['size']}")
            if old['permissions'] != new['permissions']:
                changes.append(f"perms:{old['permissions']}->{new['permissions']}")
            if old['mtime'] != new['mtime']:
                changes.append(f"mtime:{old['mtime']}->{new['mtime']}")
            
            if changes:
                log_event("FILE MODIFIED", filename, new, ", ".join(changes))
    
    # Save current state
    try:
        import pickle
        with open(state_file, 'wb') as f:
            pickle.dump(current_state, f)
        print(f"Saved current state with {len(current_state)} files")
    except Exception as e:
        print(f"Failed to save state: {e}")
    
    return current_state

# Execute detection when module is imported
current_state = detect_and_log_changes()

# Calculate statistics
total_files = len(current_state)

# Read recent logs
recent_logs = ""
if os.path.exists(log_file):
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_logs = "".join(lines[-10:]) if len(lines) > 0 else "No logs yet"
    except Exception as e:
        recent_logs = f"Error reading log file: {e}"
else:
    # Create initial log entry
    try:
        with open(log_file, 'w') as f:
            f.write("Directory Monitor Log\n")
            f.write("=" * 50 + "\n")
            f.write(f"Started monitoring: {monitor_directory}\n")
            f.write(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")
        recent_logs = "Log file created"
    except Exception as e:
        recent_logs = f"Failed to create log file: {e}"

# Export variables
__all__ = ['monitor_directory', 'total_files', 'recent_logs', 'current_state', 'log_event', 'detect_and_log_changes']
