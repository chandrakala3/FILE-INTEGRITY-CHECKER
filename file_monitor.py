import hashlib
import os
import json

HASHES_FILE = "file_hashes.json"

def calculate_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def scan_directory(directory):
    """Scan directory and return dict of file paths and their hashes."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            file_hash = calculate_hash(path)
            if file_hash:  # Avoid adding None values
                file_hashes[path] = file_hash
    return file_hashes

def save_hashes(hashes, filename=HASHES_FILE):
    """Save hash dictionary to JSON file."""
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=2)
    print(f"✅ Hashes saved successfully to {filename}")

def load_hashes(filename=HASHES_FILE):
    """Load stored hashes from JSON."""
    if not os.path.exists(filename):
        print("⚠️ No previous hash records found. Run initialization first.")
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def compare_hashes(old_hashes, new_hashes):
    """Compare stored hashes with new ones."""
    changed, added, removed = [], [], []
    
    for path in new_hashes:
        if path not in old_hashes:
            added.append(path)
        elif old_hashes[path] != new_hashes[path]:
            changed.append(path)
    
    for path in old_hashes:
        if path not in new_hashes:
            removed.append(path)

    return changed, added, removed

def main():
    """Main function to monitor files."""
    directory = input("Enter directory to monitor: ").strip()
    if not os.path.isdir(directory):
        print("❌ Invalid directory path! Please try again.")
        return

    print("\n📌 Options:")
    print("1️⃣ Initialize file hashes")
    print("2️⃣ Check for file changes")
    
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        hashes = scan_directory(directory)
        save_hashes(hashes)
        print(f"✅ File hashes initialized and saved.")
    
    elif choice == "2":
        old_hashes = load_hashes()
        new_hashes = scan_directory(directory)
        changed, added, removed = compare_hashes(old_hashes, new_hashes)

        if not (changed or added or removed):
            print("\n✅ No file changes detected.")
        else:
            print("\n🔍 Changes Detected:")
            if changed:
                print("✏️ Modified files:")
                for path in changed:
                    print(f"  - {path}")
            if added:
                print("➕ Newly added files:")
                for path in added:
                    print(f"  - {path}")
            if removed:
                print("❌ Removed files:")
                for path in removed:
                    print(f"  - {path}")
            
        save_hashes(new_hashes)  # Update records

    else:
        print("⚠️ Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()