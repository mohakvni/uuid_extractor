from .downloader import download_and_save_app
from .analyzer import extract_uuids
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_uuids_from_apks(apks: list[str]) -> dict[str, list[str]]:
    """ Main function to extract UUIDs from a list of APK URLs using multi-threading. """
    uuids = {}
    dest_dir = tempfile.mkdtemp()  # Create a temporary directory for downloads
    
    # Function to download and extract UUIDs for a single APK
    def process_apk(apk):
        apk_path = download_and_save_app(apk, dest_dir)
        if apk_path:
            apk_uuids = extract_uuids(apk_path)
            os.remove(apk_path)
            return (apk, apk_uuids)
        return (apk, [])

    # Use ThreadPoolExecutor to manage multiple threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all APKs for processing
        future_to_apk = {executor.submit(process_apk, apk): apk for apk in apks}
        
        # As each thread completes, gather results
        for future in as_completed(future_to_apk):
            apk, apk_uuids = future.result()
            uuids[apk] = apk_uuids

    return uuids
