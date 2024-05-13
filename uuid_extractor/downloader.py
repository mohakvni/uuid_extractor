import io
import logging
from typing import Optional, BinaryIO

import requests
from tqdm import tqdm
from DrissionPage import SessionPage
from DrissionPage.errors import ElementNotFoundError
from urllib.parse import urlparse, urlunparse, ParseResult
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


def get_file_size(url: str) -> Optional[int]:
    """
    Get the size of the file at the given URL.

    Args:
        url (str): URL of the file.

    Returns:
        Optional[int]: Size of the file in bytes, or None if the size cannot be determined.
    """
    response = requests.head(url, headers=HEADERS, timeout=10)
    content_length = response.headers.get("Content-Length")
    return int(content_length) if content_length is not None else None



def download_single(sha256: str) -> Optional[BinaryIO]:
    """
    Download a single APK from APKPure

    Args:
        keywords (str): Search keywords

    Returns:
        Optional[BinaryIO]: Downloaded file pointer
    """

    download_link = f"https://androzoo.uni.lu/api/download?apikey={API_KEY}&sha256={sha256}"
    file_size = get_file_size(download_link)

    response = requests.get(download_link, stream=True, timeout=300, headers=HEADERS)
    response.raise_for_status()

    file_stream = io.BytesIO()

    if file_size:  # If file size is known
        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Downloading"
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file_stream.write(chunk)
                    pbar.update(len(chunk))
    else:  # If file size is not known
        for chunk in response.iter_content(chunk_size=8192):
            file_stream.write(chunk)

    file_stream.seek(0)
    return file_stream

def save_file(file_stream: io.BytesIO, file_path: str):
    """
    Save the content of file_stream to a file.

    Args:
        file_stream (io.BytesIO): The file stream to write.
        file_path (str): The path where the file will be saved.
    """
    # Open the file_path in binary write mode
    with open(file_path, 'wb') as f:
        # Write the contents of file_stream to the file
        f.write(file_stream.getbuffer())

def download_and_save_app(app_keyword: str, dest_dir: str = None):
    """
    Download an app by its search keywords and save it to a specified path.

    Args:
        app_keyword (str): Search keywords to find the app.
        app_id (str): Identifier for saving the file.
    """
    try:
        logging.log(logging.INFO, f"Downloading {app_keyword}")
        stream = download_single(app_keyword)
        if stream:
            if dest_dir is None:
                raise Exception("Destination directory not provided")
            dest_path = os.path.join(dest_dir, f'{app_keyword}.apk')
            save_file(stream, dest_path)
            return dest_path
        else:
            logging.log(logging.ERROR, f"App {app_keyword} not found")
            return
    except Exception as e:
        logging.log(logging.ERROR, e)