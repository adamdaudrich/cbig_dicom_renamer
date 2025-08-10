def get_cbig_mapping(dicom_archive_path):
    """
    Authenticate with CBIGR API and get the candidate mapping for this DICOM archive.

    Args:
        dicom_archive_path (str): Path to DICOM archive

    Returns: 
        str: CBIG label in format '<pscid>_<candid>' or None if not found
    """
    
    # Authenticate with API
    login_url = "https://cbigr.loris.ca/api/v0.0.3/login" 
    credentials = {
        "username": "",
        "password": "your_password_here"
    }

    try:
        response = requests.post(login_url, json=credentials)
        print(f"Login Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Login failed with status code: {response.status_code}")
            return None
            
        print("✓ Successfully Connected to CBIGR-API. Submitting authntication token.")
        token = response.json().get("token")
        if not token:
            print("Error: Authentication failed: No token found.")
            return None
            
    except requests.RequestException as e:
        print(f"Error connecting to CBIGR API: {e}")
        return None

    # Get candidates and find match
    headers = {"Authorization": f"Bearer {token}"}
    candidates_url = "https://cbigr.loris.ca/cbigr_api/candidatesPlus"
    
    try:
        candidates_response = requests.get(candidates_url, headers=headers)
        
        if candidates_response.status_code != 200:
            print(f"Failed to fetch candidates. Status code: {candidates_response.status_code}")
            return None
        #you can define the error codes here (RED)
            
        candidates = candidates_response.json().get("Candidates", [])
        
        # Extract archive name and convert to search format
        archive_name = os.path.basename(dicom_archive_path.rstrip('/'))
        #improve this so it looks for the substring
        filepath_hyphenated = archive_name[:16].replace('_', '-')
        print(f"Looking for match with: {filepath_hyphenated}")
        
        # Search through candidates
        for candidate in candidates:
            ext_study_ids = candidate.get('ExtStudyIDs', {})
            #gets the 'Q1K' key in the ExtStudIDs 
            # because there could be more than one
            q1k_id = ext_study_ids.get('Q1K', '')
            pscid = candidate.get('PSCID', '')
            cand_id = candidate.get('CandID', '')
            
            if q1k_id and filepath_hyphenated in q1k_id:
                cbig_label = f"{pscid}_{cand_id}"
                print(f"✓ Match found! {q1k_id} → {cbig_label}")
                return cbig_label
        
        print(f"No match found for {filepath_hyphenated}")
        return None
        
    except requests.RequestException as e:
        print(f"Error fetching candidates: {e}")
        return None
    