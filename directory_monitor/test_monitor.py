import os
import time
import random

def create_test_files(folder="test_folder", num_files=5):
    """Create test files"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    print(f"📂 Creating test files in {folder}...")

    files_created = []

    for i in range(num_files):
        filename = f"test_{i+1}.txt"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w") as f:
            f.write(f"This is test file #{i+1}\n")
            f.write(f"Created at: {time.ctime()}\n")

        files_created.append(filepath)
        print(f"  ✅ Created: {filename}")
        time.sleep(0.5)  # Small delay

    return files_created

def modify_test_files(files):
    """Modify test files"""
    print("\n✏️  Modifying test files...")

    for filepath in files:
        if os.path.exists(filepath):
            with open(filepath, "a") as f:
                f.write(f"[Modified] Time: {time.ctime()}\n")
            print(f"  ✏️  Modified: {os.path.basename(filepath)}")
            time.sleep(0.3)

def delete_some_files(files):
    """Delete some test files"""
    print("\n🗑️  Deleting some files...")

    # Randomly delete part of the files
    files_to_delete = random.sample(files, min(2, len(files)))

    for filepath in files_to_delete:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  🗑️  Deleted: {os.path.basename(filepath)}")
            time.sleep(0.3)

    return files_to_delete

def run_full_test():
    """Run full test process"""
    print("=" * 40)
    print("Starting Directory Monitoring Test")
    print("=" * 40)

    # 1. Create files
    files = create_test_files(num_files=3)
    time.sleep(1)

    # 2. Modify files
    modify_test_files(files)
    time.sleep(1)

    # 3. Delete some files
    deleted = delete_some_files(files)

    # 4. Display results
    print("\n" + "=" * 40)
    print("Test completed!")
    print("-" * 40)
    print(f"Number of files created: {len(files)}")
    print(f"Number of files deleted: {len(deleted)}")
    print(f"Number of remaining files: {len(files) - len(deleted)}")

    # Show remaining files
    remaining = [f for f in files if os.path.exists(f)]
    if remaining:
        print("\nRemaining files:")
        for filepath in remaining:
            print(f"  📄 {os.path.basename(filepath)}")

    print("\n💡 Tip: Run `python3 monitor.py` in another terminal to observe these changes")

if __name__ == "__main__":
    run_full_test()
