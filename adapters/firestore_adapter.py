from google.cloud import firestore
import pandas as pd
from typing import List, Optional

class FirestoreAdapter:
    def __init__(self, project_id: Optional[str] = None, database_name: Optional[str] = None):
        """Initialize Firestore client.
        
        Args:
            project_id: Optional Google Cloud project ID. If None, uses default credentials.
            database_name: Optional database name. If None, uses default database.
        """
        self.db = firestore.Client(project=project_id, database=database_name) if project_id else firestore.Client(database=database_name)
        
    def list_collections(self) -> List[str]:
        """List all collections in the Firestore database.
        
        Returns:
            List of collection IDs/names
        """
        collections = self.db.collections()
        return [collection.id for collection in collections]

    def collection_to_df(self, collection_name: str) -> pd.DataFrame:
        """Convert an entire collection to a pandas DataFrame.
        
        Args:
            collection_name: Name of the Firestore collection
            
        Returns:
            pandas DataFrame containing the collection data
        """
        docs = self.db.collection(collection_name).stream()
        items = []
        for doc in docs:
            item = doc.to_dict()
            item['document_id'] = doc.id  # Add document ID as a column
            items.append(item)
        
        return pd.DataFrame(items) if items else pd.DataFrame()

    def query_to_df(self, collection_name: str, filters: List[tuple]) -> pd.DataFrame:
        """Query a collection with filters and convert results to a pandas DataFrame.
        
        Args:
            collection_name: Name of the Firestore collection
            filters: List of tuples in format [(field, operator, value), ...]
                    Operators can be '==', '<', '<=', '>', '>='
                    
        Returns:
            pandas DataFrame containing the filtered data
        """
        query = self.db.collection(collection_name)
        
        for field, op, value in filters:
            query = query.where(field, op, value)
            
        docs = query.stream()
        items = []
        for doc in docs:
            item = doc.to_dict()
            item['document_id'] = doc.id
            items.append(item)
            
        return pd.DataFrame(items) if items else pd.DataFrame()

    def get_document_as_series(self, collection_name: str, document_id: str) -> pd.Series:
        """Get a single document as a pandas Series.
        
        Args:
            collection_name: Name of the Firestore collection
            document_id: ID of the document to retrieve
            
        Returns:
            pandas Series containing the document data
        """
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            data['document_id'] = doc.id
            return pd.Series(data)
        else:
            return pd.Series()
