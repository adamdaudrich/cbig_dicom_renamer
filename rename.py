import os
import pydicom
import requests




def rename_archive(new_name):
    """
    Essentially mv <old_name> <new_name> for the current archive
    if it's already been renamed, skip
    """
    print(f"your dicom archive will be renamed to {x}. 
          The old Archive name is still stored in data_state.json"

def rename_patient_name(new_name, backup=True, dry_run=False):
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


def rename_all_patient_names(directory, cbig_label, dry_run=False):
    """
    checks status of archive in json.
    renames all DICOMS, or starts at the file that is unnamed 
    so if 0010,0010 = (str), skip
    if 0010,0010 != str, execute reaname_patient_name()
    
    Args:
        directory (str): Root directory to search
        new_patient_name (str): New patient name

        
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


