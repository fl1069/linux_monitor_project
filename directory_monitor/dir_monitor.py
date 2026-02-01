#!/usr/bin/env python3
import os
import stat
import time
from datetime import datetime
from pathlib import Path

# Configuration
monitor_directory = "./monitored_directory"
log_file = "/home/aix/linux_monitor_project/reporting/dir_monitor_log.txt"

# Ensure the monitoring directory exists
if not os.path.exists(monitor_directory):
    os.makedirs(monitor_directory, exist_ok=True)

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
    except:
        return None

def log_event(event_type, filename, metadata=None, old_value=None):
    """Log directory events to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {event_type}: {filename}\n")
        if metadata:
            f.write(f"  Type: {metadata['type']}\n")
            f.write(f"  Size: {metadata['size']} bytes\n")
            f.write(f"  Permissions: {metadata['permissions']}\n")
            f.write(f"  Modified: {metadata['mtime']}\n")
        if old_value:
            f.write(f"  Previous value: {old_value}\n")
        f.write("-" * 40 + "\n")

def detect_and_log_changes():
    """Detect changes in the directory and log them"""
    # Get current state
    current_state = {}
    try:
        files = os.listdir(monitor_directory)
        for filename in files:
            filepath = os.path.join(monitor_directory, filename)
            metadata = get_file_metadata(filepath)
            if metadata:
                current_state[filename] = metadata
    except:
        current_state = {}
    
    # Read previous state from a hidden file
    state_file = "/home/aix/linux_monitor_project/reporting/.dir_state.pkl"
    previous_state = {}
    
    try:
        import pickle
        if os.path.exists(state_file):
            with open(state_file, 'rb') as f:
                previous_state = pickle.load(f)
    except:
        pass
    
    # Detect changes
    # 1. New files
    for filename in current_state:
        if filename not in previous_state:
            log_event("FILE CREATED", filename, current_state[filename])
    
    # 2. Deleted files
    for filename in previous_state:
        if filename not in current_state:
            log_event("FILE DELETED", filename)
    
    # 3. Modified files
    for filename in current_state:
        if filename in previous_state:
            old_meta = previous_state[filename]
            new_meta = current_state[filename]
            
            changes = []
            if old_meta['size'] != new_meta['size']:
                changes.append(f"size:{old_meta['size']}->{new_meta['size']}")
            if old_meta['permissions'] != new_meta['permissions']:
                changes.append(f"permissions:{old_meta['permissions']}->{new_meta['permissions']}")
            if old_meta['mtime'] != new_meta['mtime']:
                changes.append(f"modified:{old_meta['mtime']}->{new_meta['mtime']}")
            
            if changes:
                log_event("FILE MODIFIED", filename, new_meta, ", ".join(changes))
    
    # Save current state for next comparison
    try:
        import pickle
        with open(state_file, 'wb') as f:
            pickle.dump(current_state, f)
    except:
        pass
    
    return current_state

# Get current directory state and detect changes
current_state = detect_and_log_changes()

# Calculate statistics
total_files = len(current_state)

# Read recent logs (if any)
recent_logs = ""
if os.path.exists(log_file):
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_logs = "".join(lines[-10:]) if len(lines) > 0 else "No logs yet"
    except:
        recent_logs = "Error reading log file"
else:
    # Create initial log entry
    with open(log_file, 'w') as f:
        f.write("Directory Monitor Log\n")
        f.write("=" * 50 + "\n")
        f.write(f"Started monitoring: {monitor_directory}\n")
        f.write(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
    recent_logs = "Log file created"

# Create some sample logs if file is empty
if os.path.exists(log_file) and os.path.getsize(log_file) < 100:
    # Add sample events for testing
    sample_files = list(current_state.keys())[:3]
    for i, filename in enumerate(sample_files):
        if i < len(sample_files):
            metadata = current_state[filename]
            log_event(f"SAMPLE EVENT {i+1}", filename, metadata)

# Export variables
__all__ = ['monitor_directory', 'total_files', 'recent_logs', 'current_state', 'log_event', 'detect_and_log_changes']
