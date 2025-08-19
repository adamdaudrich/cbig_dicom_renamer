import os
import json
from utilities.arg_parser import setup_args, process_paths

#bring in variables from other files
args = setup_args()
paths = process_paths()
archives = os.listdir(paths['archive_dir'])


def check_and_add_new_archives(archives, active_data, paths):
    """
    Check if archive exists in data_state. If not, add it with basic info.
    """
    
    # Get list of original names already in data_state
    existing_names = [
        entry.get("original_name", "") 
        for entry in active_data.values()
        if entry.get("original_name", "")
    ]

    for archive in archives:
        # Skip if already in data_state
        if archive in existing_names:
            print(f"Archive {archive} already exists - skipping")
            continue
        
        # Get full path and check if it's a directory
        archive_path = os.path.join(paths['archive_dir'], archive)
        if not os.path.isdir(archive_path):
            print(f"Skipping {archive} - not a directory")
            continue
        
        # Add new entry to active_data
        active_data[archive] = {  # Use archive name as key
            "original_name": archive,
            "status": 0,
            "visit_label": "",
            "ids": {
                "pscid": "",
                "candid": "",
                "extid": ""
            },
            "date_updated": ""
        }
        print(f"Added new archive: {archive}")

# Usage:
archives = os.listdir(paths['archive_dir'])
check_and_add_new_archives(archives, active_data, paths)

# Save the updated data_state
with open("data_state.json", "w") as f:
    json.dump(data_states, f, indent=2)