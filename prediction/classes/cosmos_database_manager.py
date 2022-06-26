
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pandas as pd
from tqdm import tqdm


class CosmosDatabaseManager:
    def __init__(self, endpoint, write_key) -> None:
        self.client = CosmosClient(endpoint, write_key)

    def create_database(self, database_name):
        """
        Create a database.
        """
        database_name = 'BookshelfDatabase'
        database = self.client.create_database_if_not_exists(id=database_name)
        return database

    def connect_to_database(self, database_name):
        """
        Connect to a database.
        """
        database = self.client.get_database_client(database_name)
        return database

    def create_container(self, database, container_name, partition_key):
        """
        Create a container in the database.
        """
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path = '/' + partition_key),
            offer_throughput=400
            )
        return container

    def get_container(self, database, container_name):
        """
        Get a container from the database.
        """
        container = database.get_container_client(container_name)
        return container

    def create_item(self, container, item):
        """Add item into container."""
        container.create_item(body=item)
        

    def send_csv_to_container(self, container, csv_file):
        """
        Convert csv file to list of dictionaries and send to Cosmos DB container.
        """
        data = pd.read_csv(csv_file)
        data = data.reset_index().rename(columns={'index': 'id'})
        data['id'] = (data['id'] + 1).astype(str) # Cosmos DB requires id to be a string
        data = data.to_dict(orient="records")
        for item in tqdm(data):
            container.create_item(body=item)

    def get_item(self, container, item_id):
        """
        Get an item from the container.
        """
        item = container.read_item(item_id)
        return item

    def query_item(self, container, query):
        """
        Query the container.
        """
        return list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))


# </create_item>

# # Read items (key value lookups by partition key and id, aka point reads)
# # <read_item>
# for family in family_items_to_create:
#     item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
#     request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
#     print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
# # </read_item>

# # Query these items using the SQL query syntax. 
# # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
# # <query_items>
# query = "SELECT * FROM c WHERE c.lastName IN ('Wakefield', 'Andersen')"

# items = list(container.query_items(
#     query=query,
#     enable_cross_partition_query=True
# ))

# request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

# print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
# # </query_items>
