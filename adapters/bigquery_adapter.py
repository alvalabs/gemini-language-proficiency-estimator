from google.cloud import bigquery
from google.api_core import retry
from typing import List, Dict, Any, Optional
import logging
import pandas as pd

class BigQueryAdapter:
    def __init__(self, project_id: str, credentials_path: Optional[str] = None):
        """
        Initialize BigQuery client
        
        Args:
            project_id: Google Cloud project ID
            credentials_path: Path to service account credentials JSON file
        """
        self.project_id = project_id
        if credentials_path:
            self.client = bigquery.Client.from_service_account_json(
                credentials_path,
                project=project_id
            )
        else:
            # Uses default credentials
            self.client = bigquery.Client(project=project_id)
        
        self.logger = logging.getLogger(__name__)

    @retry.Retry(predicate=retry.if_transient_error)
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a BigQuery SQL query and return results as a pandas DataFrame
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
            
        Returns:
            pandas DataFrame containing query results
        """
        try:
            job_config = bigquery.QueryJobConfig()
            if params:
                job_config.query_parameters = [
                    bigquery.ScalarQueryParameter(key, self._get_param_type(value), value)
                    for key, value in params.items()
                ]

            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            # Convert results to pandas DataFrame
            df = results.to_dataframe()
            return df
            
        except Exception as e:
            self.logger.error(f"Error executing BigQuery query: {str(e)}")
            raise

    def create_table(self, dataset_id: str, table_id: str, schema: List[bigquery.SchemaField]) -> None:
        """
        Create a new BigQuery table
        
        Args:
            dataset_id: ID of the dataset
            table_id: ID of the table to create
            schema: List of SchemaField objects defining the table schema
        """
        try:
            dataset_ref = self.client.dataset(dataset_id)
            table_ref = dataset_ref.table(table_id)
            table = bigquery.Table(table_ref, schema=schema)
            
            self.client.create_table(table)
            self.logger.info(f"Created table {dataset_id}.{table_id}")
            
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            raise

    def insert_rows(self, dataset_id: str, table_id: str, rows: List[Dict[str, Any]]) -> None:
        """
        Insert rows into a BigQuery table
        
        Args:
            dataset_id: ID of the dataset
            table_id: ID of the table
            rows: List of dictionaries containing the rows to insert
        """
        try:
            table_ref = self.client.dataset(dataset_id).table(table_id)
            errors = self.client.insert_rows_json(table_ref, rows)
            
            if errors:
                raise Exception(f"Errors inserting rows: {errors}")
                
            self.logger.info(f"Successfully inserted {len(rows)} rows into {dataset_id}.{table_id}")
            
        except Exception as e:
            self.logger.error(f"Error inserting rows: {str(e)}")
            raise

    @staticmethod
    def _get_param_type(value: Any) -> str:
        """
        Get the BigQuery parameter type based on Python value type
        
        Args:
            value: Python value to check
            
        Returns:
            BigQuery parameter type string
        """
        if isinstance(value, bool):
            return 'BOOL'
        elif isinstance(value, int):
            return 'INT64'
        elif isinstance(value, float):
            return 'FLOAT64'
        elif isinstance(value, str):
            return 'STRING'
        else:
            raise ValueError(f"Unsupported parameter type: {type(value)}")
