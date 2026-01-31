import os
import time

def monitor_directory(path):
    print("=== Directory Monitor Started ===")
    print(f"Monitoring: {os.path.abspath(path)}")
    print("Press Ctrl+C to stop")
    print("-" * 40)

    previous_files = set(os.listdir(path))

    try:
        while True:
            time.sleep(1)
            current_files = set(os.listdir(path))

            # New files
            for file in current_files - previous_files:
                print(f"📁 New file: {file}")

            # Deleted files
            for file in previous_files - current_files:
                print(f"🗑️  Deleted file: {file}")

            previous_files = current_files

    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    monitor_dir = "./test_folder"

    if not os.path.exists(monitor_dir):
        os.makedirs(monitor_dir)
        print(f"Created directory: {monitor_dir}")

    monitor_directory(monitor_dir)

