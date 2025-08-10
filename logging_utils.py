def scan_dicom_dir()
    """
    Copy Dicom file names into the json. Create new items if they don't exist
    """


def load_rename_log():
    """Load existing rename log or create new one."""
    log_filename = "dicom_rename_log.json"
    
    if os.path.exists(log_filename):
        try:
            with open(log_filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read existing log file, creating new one")
    
    return {}

def save_rename_log(log_data):
    """Save rename log to JSON file."""
    log_filename = "dicom_rename_log.json"
    try:
        with open(log_filename, 'w') as f:
            json.dump(log_data, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save log file: {e}")

def get_patient_name_from_dicom(filepath):
    """
    Extract patient name from a DICOM file.
    
    Args:
        filepath (str): Path to DICOM file
        
    Returns:
        str: Patient name or None if not found/error
    """
    try:
        ds = pydicom.dcmread(filepath, stop_before_pixels=True)
        return str(ds.PatientName) if hasattr(ds, 'PatientName') else None
    except (InvalidDicomError, FileNotFoundError, Exception):
        return None

def verify_dicom_patient_names(directory_path, expected_name):
    """
    Check if first and last DICOM files have the expected patient name.
    
    Args:
        directory_path (str): Directory containing DICOM files
        expected_name (str): Expected patient name
        
    Returns:
        tuple: (bool, first_patient_name, last_patient_name)
    """
    try:
        # Get all files in directory
        files = [f for f in os.listdir(directory_path) 
                if os.path.isfile(os.path.join(directory_path, f))]
        
        if len(files) < 1:
            return False, None, None
        
        # Sort files to get consistent first/last
        files.sort()
        
        first_file = os.path.join(directory_path, files[0])
        last_file = os.path.join(directory_path, files[-1])
        
        first_patient = get_patient_name_from_dicom(first_file)
        last_patient = get_patient_name_from_dicom(last_file)
        
        # Check if both match expected name
        names_match = (first_patient == expected_name and 
                      last_patient == expected_name)
        
        return names_match, first_patient, last_patient
        
    except (OSError, Exception) as e:
        print(f"Error verifying patient names: {e}")
        return False, None, None

def is_already_renamed(filepath):
    """
    Check if this directory has already been renamed by looking at the JSON log.
    
    Args:
        filepath (str): Current directory path
    
    Returns:
        bool: True if already renamed, False otherwise
    """
    current_name = os.path.basename(filepath.rstrip('/'))
    log_data = load_rename_log()
    
    # Check if current name appears as a former name in any entry
    for new_name, entry in log_data.items():
        if entry.get('Former Name') == current_name:
            return True
    
    # Check if current name is already a new name (key) in log
    return current_name in log_data



