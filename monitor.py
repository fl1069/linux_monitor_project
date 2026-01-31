import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyMonitor(FileSystemEventHandler):
    def on_created(self, event):
        print(f"📁 New file created: {event.src_path}")

    def on_deleted(self, event):
        print(f"🗑️  File deleted: {event.src_path}")

    def on_modified(self, event):
        print(f"✏️  File modified: {event.src_path}")

# Start monitoring
if __name__ == "__main__":
    print("=== Directory Monitoring System Started ===")

    # Directory to monitor (test_folder in the current directory)
    monitor_dir = "./test_folder"

    # Create the directory if it does not exist
    if not os.path.exists(monitor_dir):
        os.makedirs(monitor_dir)
        print(f"Monitoring directory created: {monitor_dir}")

    print(f"Monitoring path: {os.path.abspath(monitor_dir)}")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 40)

    # Set up monitoring
    event_handler = MyMonitor()
    observer = Observer()
    observer.schedule(event_handler, monitor_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        observer.stop()

    observer.join()
    print("Monitoring stopped")
