# -*- coding: gbk -*-

import os
import zipfile
import gzip
import tarfile
from pathlib import Path
from typing import List, Tuple


def extract_archive(file_path: str, extract_to: str) -> List[str]:
    """Extract archive files to the specified directory.
    
    Args:
        file_path: Path to the archive file
        extract_to: Directory to extract files to
        
    Returns:
        List of extracted file paths
    """
    extracted_files = []
    ext = os.path.splitext(file_path)[1].lower()
    
    # Create extract directory if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)
    
    try:
        if ext == '.zip':
            extracted_files = _extract_zip(file_path, extract_to)
        elif ext == '.gz':
            if ".tar" in file_path:
                extracted_files = _extract_tar(file_path, extract_to)
            else:
                extracted_files = _extract_gzip(file_path, extract_to)
        elif ext in ['.tar', '.tgz', '.bz2', '.xz']:
            extracted_files = _extract_tar(file_path, extract_to)
        else:
            # Not an archive, just copy the file
            dest_path = os.path.join(extract_to, os.path.basename(file_path))
            import shutil
            shutil.copy2(file_path, dest_path)
            extracted_files.append(dest_path)
    except Exception as e:
        raise Exception(f"Error extracting archive: {e}")
    
    return extracted_files


def _extract_zip(zip_path: str, extract_to: str) -> List[str]:
    """Extract ZIP file."""
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file_info in zip_ref.infolist():
            if not file_info.is_dir():
                extracted_path = os.path.join(extract_to, file_info.filename)
                extracted_files.append(extracted_path)
    return extracted_files


def _extract_gzip(gzip_path: str, extract_to: str) -> List[str]:
    """Extract GZIP file."""
    extracted_files = []
    filename = os.path.basename(gzip_path)
    output_filename = filename[:-3]  # Remove .gz extension
    output_path = os.path.join(extract_to, output_filename)
    
    with gzip.open(gzip_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            f_out.write(f_in.read())
    
    extracted_files.append(output_path)
    return extracted_files


def _extract_tar(tar_path: str, extract_to: str) -> List[str]:
    """Extract TAR file."""
    extracted_files = []
    with tarfile.open(tar_path, 'r') as tar_ref:
        tar_ref.extractall(extract_to)
        for member in tar_ref.getmembers():
            if member.isfile():
                extracted_path = os.path.join(extract_to, member.name)
                extracted_files.append(extracted_path)
    return extracted_files


def get_supported_archive_extensions() -> List[str]:
    """Get list of supported archive extensions."""
    return ['.zip', '.gz', '.tar', '.tgz', '.bz2', '.xz']


def is_archive_file(file_path: str) -> bool:
    """Check if a file is an archive."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in get_supported_archive_extensions()
