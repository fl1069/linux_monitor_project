import os
import stat
from datetime import datetime
from pathlib import Path

def get_file_info(filepath):
    """Get basic file metadata"""
    try:
        # Check whether the file exists
        if not os.path.exists(filepath):
            return {"error": "File does not exist"}

        # Get file status
        stat_info = os.stat(filepath)
        path = Path(filepath)

        # Determine file type
        if path.is_symlink():
            file_type = "Symbolic Link"
        elif path.is_dir():
            file_type = "Directory"
        elif path.is_file():
            file_type = "Regular File"
        else:
            file_type = "Unknown"

        # Get file permissions
        permissions = oct(stat_info.st_mode)[-3:]

        # Get timestamps
        create_time = datetime.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        modify_time = datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        # Return all metadata
        return {
            "File Name": path.name,
            "Full Path": str(path.absolute()),
            "File Type": file_type,
            "Size (Bytes)": stat_info.st_size,
            "Permissions": permissions,
            "Owner ID": stat_info.st_uid,
            "Group ID": stat_info.st_gid,
            "Created Time": create_time,
            "Modified Time": modify_time,
            "Status OK": True
        }

    except Exception as e:
        return {"error": str(e), "Status OK": False}

# Test function
def test_extractor():
    """Test metadata extraction"""
    test_file = input("Enter file path to check (press Enter to use current directory): ").strip()

    if not test_file:
        test_file = "."

    info = get_file_info(test_file)

    print("\n" + "=" * 50)
    print("File Metadata Information")
    print("=" * 50)

    for key, value in info.items():
        print(f"{key:15}: {value}")

if __name__ == "__main__":
    test_extractor()
