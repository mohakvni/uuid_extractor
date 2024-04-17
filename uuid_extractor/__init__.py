from downloader import download_and_save_app
from analyzer import extract_uuids
import os
import tempfile

def extract_uuids_from_apks(apks: list[str]):
    """ Main function to extract UUIDs from a list of APK URLs. """
    uuids = {}
    dest_dir = tempfile.mkdtemp() 
    for apk in apks:
        apk_path = download_and_save_app(apk, dest_dir)
        if apk_path:
            apk_uuids = extract_uuids(apk_path)
            uuids[apk] = apk_uuids
            os.remove(apk_path)
    return uuids