def update_patient_names():
    """
    Update the patient name header with the mapping
    """

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
