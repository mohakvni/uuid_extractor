# UUID Extractor

This is a repository created to extract UUID's from an application available on the appstore.
What it does:
1. Makes a temporary directory to store APK's
2. Download the APK's from APKPure
3. Decompiles the APK
4. Recursively searches files to match UUID pattern
5. Returns a list of found UUID's and deletes the APK

## How To install

```
pip install git+https://github.com/mohakvni/uuid_extractor.git
```

## How to Use

```
import uuid_extractor

uuids = uuid_extractor.extract_uuids_from_apks([<List of Applications>])
```