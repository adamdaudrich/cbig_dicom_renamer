import os
import sys
import argparse
from pathlib import Path
import pydicom
from pydicom.errors import InvalidDicomError
import requests
import json
from dicom_rename import validate_dicom_directory

def main():
    
    parser = argparse.ArgumentParser(
        description='Rename DICOM archives and patient names based on CBIGR API mapping'
    )
    
    parser.add_argument('source_dir', 
                       help='Path to directory containing all DICOM archives')
    
    parser.add_argument('visit_label', help='The visit label to be used')
    parser.add_argument('test', help='the part of the data_state.json to populate. Test is for testing the script on' \
    'directories with 2 or 3 dicom archives' )


        # ... rest of your logic

    connect_to_api()
    fetch_id_mapping()
    for i in dicom_archives:
        if is_dir()
        if has_dicoms()
        populate_json()
    #use the json to:
    rename_archive()
    rename_patient_name()

if __name__ == "__main__":
    main()