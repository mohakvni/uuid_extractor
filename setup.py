from setuptools import setup, find_packages

setup(
    name='uuid_extractor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',  
        'tqdm',
        'DrissionPage'
    ],
    entry_points={
        'console_scripts': [
            'extract_uuids=uuid_extractor:extract_uuids_from_apks',
        ],
    }
)