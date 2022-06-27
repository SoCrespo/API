# coding=utf-8
import pandas as pd
from azure.cosmos import CosmosClient


import os
import sys
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path += [CURRENT_DIR, PARENT_DIR]
from prediction import params


class CosmosDataReader:

    def __init__(self, endpoint, read_key, 
                database_name, 
                clicks_container_name, 
                articles_metadata_container_name) -> None:
        """
        Class to read data from cosmos database.
        """
        print('Connecting to Cosmos DB...', end='\r')
        self.client = CosmosClient(endpoint, read_key)
        print('Connected to Cosmos DB.', end='\r')

        print('Connecting to database...', end='\r')
        self.database = self.client.get_database_client(database_name)
        print('Connected to database.', end='\r')

        print('Connecting to clicks container...', end='\r')
        self.clicks_container = self.database.get_container_client(
                        clicks_container_name)
        print('Connected to clicks container.', end='\r')

        print('Connecting to articles metadata container...', end='\r')
        self.articles_metadata_container = self.database.get_container_client(
                        articles_metadata_container_name)
        print('Connected to articles metadata container.', end='\r')

        print('Ready!'.ljust(60))
    

    def get_data_for_user(self, user_id: int) -> pd.DataFrame:
        """
        Return dataframe of readings and metadata for user_id.
        """
        # Get data for reader
        query_for_clicks = f"""SELECT * from c WHERE c.user_id = {user_id}"""
        clicks = self.clicks_container.query_items(query_for_clicks, enable_cross_partition_query=True)
        clicks = pd.DataFrame(clicks)    
        if clicks.empty:
            raise ValueError('User not found')

        # Get metadata for reader articles
        articles_id_list = ', '.join(clicks['click_article_id'].astype(str).values.tolist())
        query_for_articles_metadata = f"""SELECT * from c WHERE c.article_id IN ({articles_id_list})"""
        articles_metadata = self.articles_metadata_container.query_items(query_for_articles_metadata,
                                                    enable_cross_partition_query=True)
        articles_metadata = pd.DataFrame(articles_metadata)

        # Merge results
        data = clicks.merge(articles_metadata, 
                          left_on='click_article_id',
                          right_on='article_id')
        return data    


    def get_most_read_articles_ids(self) -> list:
        query = f"""SELECT c.click_article_id FROM c OFFSET 0 LIMIT 5"""
        most_read = list(self.clicks_container.query_items(query, enable_cross_partition_query=True))
        most_read = pd.DataFrame(most_read)
        return most_read['click_article_id'].astype(str).values.tolist()

