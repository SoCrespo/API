import os
import sys
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path += [CURRENT_DIR, PARENT_DIR]
from prediction import params
from azure.storage.blob import BlobClient    


class BlobManager:
    def __init__(self) -> None:
        self.blob_client = BlobClient(
            account_url=params.account_url, 
            container_name=params.container_name,
            blob_name=params.blob_name,
            credential=params.account_key)

    
    def send_file(self, file_path) -> None:
        """Upload the local file to the blob storage."""
        self.blob_client.upload_blob(file_path, overwrite=True)

    def load_file(self, file_path) -> None:
        """Download the blob file to the local file_path."""
        with open(file_path, "wb") as f:
            f.write(self.blob_client.download_blob().readall())


   