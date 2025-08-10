import os
import sys
import argparse
from pathlib import Path
import pydicom
from pydicom.errors import InvalidDicomError
import requests
import json

def main():
    args = parse_arguments()
    
    # Validate directory
    validate_dicom_directory(dicom_archive_path)

    get_ids()
    rename_dicom_archive(cbig_label)
    rename_all_patient_names(cbig_label)

    # Confirm with user unless dry run
    if not args.dry_run:
        print(f"This will rename patient names in all DICOM files in:")
        print(f"  {os.path.abspath(args.directory)}")
        print(f"New patient name: '{}'")
        print(f"Backup files: {'No' if args.no_backup else 'Yes'}")
        
        confirm = input("\nContinue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled")
            sys.exit(0)
    
    # Perform the renaming
    success_count, total_count = find_and_process_dicom_files(
        args.directory,
        backup=not args.no_backup,
        dry_run=args.dry_run
    )
    
    # Summary
    print("-" * 50)
    if args.dry_run:
        print(f"DRY RUN COMPLETE:")
        print(f"  Would update: {success_count}/{total_count} DICOM files")
    else:
        print(f"OPERATION COMPLETE:")
        print(f"  Successfully updated: {success_count}/{total_count} DICOM files")
        if success_count < total_count:
            print(f"  Failed: {total_count - success_count} files")


if __name__ == "__main__":
    main()