data_dir = '/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/news-portal-user-interactions-by-globocom/'
nb = 5

# Azure CosmosDB storage

cosmos_endpoint = 'https://cosmos-db-p9.documents.azure.com:443/'
cosmos_write_key = 'gniYekC4tX7M5Q1ISSAZhtRlH4jktzeONkuNWXgCWujAMfGpUvWtV4ahB0N9s3GIE9tsrXqONnXliO1qBWH6oQ=='
cosmos_read_key = 'WFz5sMOg5dOL7UzQTxU4YDvicAuJSJGyDW98UvafkuvzVDqJSDAsf64BR4fcTnnekqvDjttcCO2lfUFYZlh3iQ=='
cosmos_database_name = 'BookshelfDatabase'
cosmos_clicks_container_name = 'Clicks'
cosmos_metadata_container_name = 'Metadata'
cosmos_embeddings_container_name = 'Embeddings'

# Azure Blob storage
blob_account_url = 'https://p9storage.blob.core.windows.net/'
blob_account_key = 'vqrHDdX2ANqgo6P+RX4gJV7x5KrUVqv8ig05RJbYCsfaBAiL89PMURmu+BAzVkszgMN5BKw0RNC7+AStPFpuCQ=='
blob_container_name = 'model'
blob_blob_name = 'knn_model.pkl'