import argparse

def setup_args():
    """
    Parse CLI arguments 
    """
    parser = argparse.ArgumentParser(description='DICOM processing and renaming tool')

    parser.add_argument('--archive_dir', help= 'absolute path of the directory containing your DICOM archives')
    parser.add_argument('--visit_label', required=True, help='Enter your Visit Label')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', help='Uses the "test" part of the data_state.json')
    group.add_argument('--real', help='Uses the "real" part of the data_state.json')

    return parser.parse_args()

