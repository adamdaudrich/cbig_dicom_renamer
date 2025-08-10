#!/usr/bin/env python3
"""
DICOM Renamer Script

This script uses the CBIGR API to rename all dicom directories and the Patient Name headers
(0010,0010) of each dicom file. This prepares the dicoms for 
a) direct ingestion 
or 
b)bids conversion + eventual ingestion 

Requirements:
    pip install pydicom

Usage:
    python dicom_rename.py /path/to/dicom/folder "New Patient Name"
"""



def parse_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description='Rename DICOM archive and patient names based on CBIGR API mapping'
    )
    
    parser.add_argument('dicom_archive', 
                       help='Path to DICOM archive directory')
    
    return parser.parse_args()

def validate_dicom_directory(dicom_archive_path):
    """
    Validate DICOM archive path before processing
    arg: str
    returns: bool.
    """
    # Check if directory exists
    if not os.path.exists(dicom_archive_path):
        print(f"Error: Directory '{dicom_archive_path}' does not exist")
        return False
    
    if not os.path.isdir(dicom_archive_path):
        print(f"Error: '{dicom_archive_path}' is not a directory")
        return False
    
    # Fast check for subdirectories - exit immediately if found
    try:
        for item in os.listdir(dicom_archive_path):
            item_path = os.path.join(dicom_archive_path, item)
            if os.path.isdir(item_path):
                print(f"Error: DICOM archive contains subdirectories (found: '{item}')")
                print("This function expects a flat directory structure with DICOM files only.")
                return False
    except OSError as e:
        print(f"Error reading directory: {e}")
        return False
    
    print("✓ DICOM archive structure validated")
    return True

def rename_dicom_archive(filepath, cbig_label):
    """
    Essentially mv <old_name> <new_name> for the current archive
    if it's already been renamed, skip
    """


def rename_patient_name(filepath, new_patient_name, backup=True, dry_run=False):
    """
    Process a single file: check if DICOM, and update patient name if requested.
    
    Args:
        filepath (str): Path to the file
        new_patient_name (str): New patient name to set
        backup (bool): Whether to create a backup
        dry_run (bool): If True, only show what would be changed
        
    Returns:
        tuple: (is_dicom, success, original_name)
    """
    try:
        # Single dcmread call - this both validates DICOM and gets the data
        ds = pydicom.dcmread(filepath, stop_before_pixels=True)
        
        # Get original patient name
        original_name = getattr(ds, 'PatientName', 'Unknown')
        
        if dry_run:
            print(f"Would update: {filepath}")
            print(f"  {original_name} → {new_patient_name}")
            return True, True, str(original_name)
        
        # Create backup (with --backup=True. This takes twice as long)
        if backup:
            backup_path = f"{filepath}.backup"
            if not os.path.exists(backup_path):
                # read the full DICOM for backup
                ds_full = pydicom.dcmread(filepath)
                ds_full.save_as(backup_path)
                
                # Update the patient name on all DICOMS
                ds_full.PatientName = new_patient_name
                ds_full.save_as(filepath)
            else:
                # the case where the backup path already exists
                ds_full = pydicom.dcmread(filepath)
                ds_full.PatientName = new_patient_name
                ds_full.save_as(filepath)
        else:
            # No backup needed, but we still need full data to save
            ds_full = pydicom.dcmread(filepath)
            ds_full.PatientName = new_patient_name
            ds_full.save_as(filepath)
        
        print(f"✓ Updated: {filepath}")
        print(f"  Original: {original_name} → New: {new_patient_name}")
        
        return True, True, str(original_name)
        
    except (InvalidDicomError, FileNotFoundError, PermissionError):
        # Not a DICOM file or can't read it
        return False, False, None
    except Exception as e:
        # DICOM file but failed to update
        print(f"✗ Error updating {filepath}: {str(e)}")
        return True, False, None


def rename_all_patient_names(directory, cbig_label, backup=False, dry_run=False):
    """
    rename all DICOMS in the current archive, checking the file if it's a DICOM (isdicom = true)
    is_dicom is from rename_patient_name
    
    Args:
        directory (str): Root directory to search
        new_patient_name (str): New patient name
        backup (bool): Whether to create backups
        dry_run (bool): If True, only show what would be changed
        
    Returns:
        tuple: (success_count, total_dicom_count)
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    print(f"Scanning directory: {directory}")
    print(f"{'DRY RUN: ' if dry_run else ''}Renaming patient to: '{new_patient_name}'")
    print(f"Backup files: {'Yes' if backup else 'No'}")
    print("-" * 50)
    
    success_count = 0
    total_dicom_count = 0
    
    try:
        # Recursively walk through all files
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                is_dicom, success, original_name = rename_patient_name(
                    str(file_path), new_patient_name, backup, dry_run
                )
                
                if is_dicom:
                    total_dicom_count += 1
                    if success:
                        success_count += 1

                        if total_dicom_count = success_count:
                            put 'Y' in json
    
    except KeyboardInterrupt:
        print("\n⚠ Operation cancelled by user")
    except Exception as e:
        print(f"⚠ Error: {str(e)}")
    
    return success_count, total_dicom_count


