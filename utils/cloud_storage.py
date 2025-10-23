from google.cloud import storage
from typing import Optional, Union, BinaryIO
import os

def get_storage_client() -> storage.Client:
    """
    Creates and returns a Google Cloud Storage client.
    If running locally, it will use credentials from GOOGLE_APPLICATION_CREDENTIALS env var.
    If running on Google Cloud, it will use the default service account.
    """
    return storage.Client()

def upload_file(
    bucket_name: str,
    source_file: Union[str, BinaryIO],
    destination_blob_name: str,
    content_type: Optional[str] = None
) -> str:
    """
    Uploads a file to Google Cloud Storage bucket.
    
    Args:
        bucket_name: Name of the GCS bucket
        source_file: Path to the file or file-like object to upload
        destination_blob_name: Name to give the file in GCS (including path)
        content_type: Optional content type of the file
    
    Returns:
        Public URL of the uploaded file
    
    Raises:
        google.cloud.exceptions.NotFound: If bucket doesn't exist
        IOError: If source_file can't be read
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # If source_file is a string (path), upload from filename
    # Otherwise, upload from file object
    if isinstance(source_file, str):
        blob.upload_from_filename(source_file, content_type=content_type)
    else:
        blob.upload_from_file(source_file, content_type=content_type)

    return blob.public_url

def download_file(
    bucket_name: str,
    source_blob_name: str,
    destination_file_name: Optional[str] = None
) -> Union[str, bytes]:
    """
    Downloads a file from Google Cloud Storage bucket.
    
    Args:
        bucket_name: Name of the GCS bucket
        source_blob_name: Path to the file in GCS
        destination_file_name: Optional local path to save the file
                             If not provided, returns the file content as bytes
    
    Returns:
        If destination_file_name is provided: path to the downloaded file
        If destination_file_name is None: file contents as bytes
    
    Raises:
        google.cloud.exceptions.NotFound: If bucket or file doesn't exist
        IOError: If destination path is invalid
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    if destination_file_name:
        blob.download_to_filename(destination_file_name)
        return destination_file_name
    else:
        return blob.download_as_bytes()

def delete_file(bucket_name: str, blob_name: str) -> None:
    """
    Deletes a file from Google Cloud Storage bucket.
    
    Args:
        bucket_name: Name of the GCS bucket
        blob_name: Path to the file in GCS
    
    Raises:
        google.cloud.exceptions.NotFound: If bucket or file doesn't exist
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

def list_files(bucket_name: str, prefix: Optional[str] = None) -> list[str]:
    """
    Lists all files in a Google Cloud Storage bucket, optionally filtered by prefix.
    
    Args:
        bucket_name: Name of the GCS bucket
        prefix: Optional prefix to filter files (like a folder path)
    
    Returns:
        List of file names/paths in the bucket
    
    Raises:
        google.cloud.exceptions.NotFound: If bucket doesn't exist
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs]
