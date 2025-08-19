import os

def get_path_to_archives(path):
    """
    Convert the '--archivedir' argument to a variable pointing to absolute file path
    """
    archives = os.path.abspath(path)
    return archives

def is_dir(path):
    """
    Checks if archive path exists and is a directory
    arg: str
    returns: bool.
    """

    dicom_archives = os.path.join('dicom_archives')
    for archive_path in dicom_archives:
        # Check if directory exists
        if not os.path.exists(archive_path):
            print(f"Error: Directory '{archive_path}' does not exist")
            return False
    
        if not os.path.isdir(archive_path):
            print(f"Error: '{archive_path}' is not a directory")
            return False
        
    # Fast check for subdirectories - exit immediately if found
        try:
            for item in os.listdir(archive_path):
                item_path = os.path.join(archive_path, item)
                if os.path.isdir(item_path):
                    print(f"Error: DICOM archive contains subdirectories (found: '{item}')")
                    print("This function expects a flat directory structure with DICOM files only.")
                    return False
        except OSError as e:
            print(f"Error reading directory: {e}")
            return False
        
        print("✓ DICOM archive structure validated")
        return True
    
def has_dicoms(current_dir):
    """
    uses pydicom to check if dicom files in the dir
    arg: str
    returns:bool
    """
    for root, _, files in os.walk(current_dir):
        for f in files:
            filepath = os.path.join(root, f)
        try:
            pydicom.dcm(filepath, stop_before_pixels = True)
            return True
        except Exception:
            continue