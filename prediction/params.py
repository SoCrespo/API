data_dir = '/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/news-portal-user-interactions-by-globocom/'
nb = 5

# Azure CosmosDB storage

endpoint = 'https://cosmos-db-p9.documents.azure.com:443/'
write_key = 'gniYekC4tX7M5Q1ISSAZhtRlH4jktzeONkuNWXgCWujAMfGpUvWtV4ahB0N9s3GIE9tsrXqONnXliO1qBWH6oQ=='
read_key = 'WFz5sMOg5dOL7UzQTxU4YDvicAuJSJGyDW98UvafkuvzVDqJSDAsf64BR4fcTnnekqvDjttcCO2lfUFYZlh3iQ=='
database_name = 'BookshelfDatabase'
clicks_container_name = 'Clicks'
metadata_container_name = 'Metadata'
embeddings_container_name = 'Embeddings'

# Azure Blob storage
account_url = 'https://p9storage.blob.core.windows.net/'
account_key = 'vqrHDdX2ANqgo6P+RX4gJV7x5KrUVqv8ig05RJbYCsfaBAiL89PMURmu+BAzVkszgMN5BKw0RNC7+AStPFpuCQ=='
container_name = 'model'
blob_name = 'knn_model.pkl'