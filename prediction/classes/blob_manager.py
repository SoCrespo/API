# coding=utf-8

from azure.storage.blob import BlobClient    
from prediction import params


class BlobManager:
    def __init__(self) -> None:
        self.blob_client = BlobClient(
            account_url=params.blob_account_url, 
            container_name=params.blob_container_name,
            blob_name=params.blob_blob_name,
            credential=params.blob_account_key)    

    
    def send_file(self, file_path) -> None:
        """Upload the local file to the blob storage."""
        self.blob_client.upload_blob(file_path, overwrite=True)

    def load_file(self) -> None:
        """Download the blob file and return its content (bytes)."""
        dowloaded = self.blob_client.download_blob().readall()
        return dowloaded
