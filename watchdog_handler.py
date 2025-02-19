import os
import hashlib
import time

# Define the shared folder to monitor
shared_folder = r"C:\Users\LG8223\OneDrive - EQUANS\210006 - New St. Paul’s Hospital (NSP)\7. Deliverables\3.1.01 External Modeling"

# Dictionary to store hashes of previously processed files
file_hashes = {}

# Function to compute the hash of a file
def compute_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):  # Read in 8KB chunks
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {file_path}: {e}")
        return None

# Function to check and notify about file changes
def check_for_changes():
    for root, _, files in os.walk(shared_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            current_hash = compute_file_hash(file_path)
            
            if current_hash is None:
                continue  # Skip the file if there's an error calculating its hash

            # Check if the file already exists in the hash tracking
            if file_path in file_hashes:
                # If hash has changed, notify
                if file_hashes[file_path] != current_hash:
                    print(f"File updated: {file_path}")
                    file_hashes[file_path] = current_hash  # Update hash after change
            else:
                # If file is new, notify
                print(f"New file uploaded: {file_path}")
                file_hashes[file_path] = current_hash  # Add to hash tracking

# Function to monitor the folder for changes (polling every 5 seconds)
def monitor_folder():
    while True:
        print("Checking for changes...")
        check_for_changes()  # Check and notify for any changes
        time.sleep(5)  # Wait for 5 seconds before checking again

# Start monitoring the shared folder
print("Monitoring shared folder for changes...")
monitor_folder()
