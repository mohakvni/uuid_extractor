from downloader import download_and_save_app
from analyzer import extract_uuids
import os

def extract_uuids_from_apks(jadx_path, apks):
    """ Main function to extract UUIDs from a list of APK URLs. """
    uuids = {}
    for apk in apks:
        apk_path = download_and_save_app(apk)
        apk_uuids = extract_uuids(jadx_path, apk_path)
        uuids[apk] = apk_uuids
        os.remove(apk_path)
    return uuids