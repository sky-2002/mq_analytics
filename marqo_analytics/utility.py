import numpy as np
import pandas as pd

def get_ids_from_results(results: dict) -> list:
    """A function to fetch the ids of all documents
    from the search result.

    Args:
        results (dict): The search results dictioary returned by 
        mq.index(index_name).search(query).

    Returns:
        List: A list of ids of documents returned.

    Note:
    Make sure to keep limit such that the search results return
    all the documents in the index.
    """
    _ids = []
    for r in results['hits']:
        _ids.append(r['_id'])
    return _ids

def get_tensors_from_ids(
        mq, 
        ids: list, 
        index_name: str, 
        attribute: str
        ) -> np.ndarray:
    """A function to fetch all the document tensors for a particular
    index and attribute. It also makes use of ids to access the document
    information.

    Args:
        mq (marqo.client.Client): The marqo client object.
        ids (list): A list of ids of all documents in an index returned by a search query.
        index_name (str): The name of the index whose tensors we wish to access.
        attribute (str): The attribute name, this is required as there can be multiple
        attribute(tensor fields) and hence we want the information about which ones to fetch.

    Returns:
        numpy.ndarray: A numpy array containing all the tensors from a particular index and
        a particular attribute.
    """
    tensors = []
    for i in ids:
        # Using each id, fetch the corressponding document information
        doc = mq.index(index_name).get_document(
            document_id=i,
            expose_facets=True)
        
        # Access the tensors
        _tensors = doc['_tensor_facets']

        # This _tensors contains tensors for all attributes,
        # we need to select one.
        for t in _tensors:
            # Each entry in _tensors is a dictionary
            # with the attribute name as a key and _embedding as a key
            keys = list(t.keys())

            if attribute in keys:
                tensors.append(t['_embedding'])
                break
    return np.array(tensors)

def get_hover_data_from_ids(
        mq, 
        ids: list, 
        index_name: str
        ) -> pd.DataFrame:
    """A functon to get the hover data, which is the information displayed when a user 
    hovers over the plotted points. Currently it displays entire document information.

    Args:
        mq (marqo.client.Client): The marqo client object.
        ids (list): A list of ids of all documents in an index returned by a search query.
        index_name (str): The name of the index whose documents we wish to access.

    Returns:
        pd.DataFrame: A pandas dataframe to show information on hovering over the data point.
    """
    hover_data = []
    for i in ids:
        doc = mq.index(index_name).get_document(
            document_id=i)
        hover_data.append(doc)
    return pd.DataFrame(data=hover_data)