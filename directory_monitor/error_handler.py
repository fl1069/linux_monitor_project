import os
from datetime import datetime

def log_error(error_type, filepath, message):
    """Log error information to a file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} | {error_type} | {filepath} | {message}\n"

    # Write to log file
    with open("errors.log", "a") as f:
        f.write(log_line)

    # Also print to the console
    print(f"⚠️  Error: {error_type} - {filepath}")
    return False

def check_file_exists(filepath):
    """Check whether the file exists"""
    if not os.path.exists(filepath):
        log_error("FILE_NOT_FOUND", filepath, "File does not exist")
        return False
    return True

def check_file_permission(filepath):
    """Check file read permission"""
    if not os.access(filepath, os.R_OK):
        log_error("PERMISSION_DENIED", filepath, "No read permission")
        return False
    return True

# Test
if __name__ == "__main__":
    print("Testing error handling...")

    # Test non-existing file
    check_file_exists("/tmp/no_such_file_12345.txt")

    # Test existing file
    if check_file_exists("test_folder/test2.txt"):
        print("✅ File exists")

    print("Error log saved in: errors.log")
