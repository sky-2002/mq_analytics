import umap
import numpy
from marqo_analytics.utility import (
    get_ids_from_results,
    get_tensors_from_ids,
    get_hover_data_from_ids
)

def dimension_reduced_tensors(
        reducer: umap.umap_.UMAP, 
        tensors: numpy.ndarray
        ) -> numpy.ndarray:
    """A function to perform dimensionality reduciton on
    the supplied tensors/embeddings. Currently using UMAP for 
    dimensionality reduction.

    Args:
        reducer (umap.umap_.UMAP): The UMAP object that is used to perform dimensionality reduction.
        tensors (numpy.ndarray): The tensors array on which to perform dimensionality reduction

    Returns:
        tuple(umap.umap_.UMAP, numpy.ndarray): Returns the UMAP object fit on the tensors along with
        the dimension reduced tensors.
    """
    mapper = reducer.fit(tensors)
    reduced_embedding = mapper.transform(tensors)
    return mapper, reduced_embedding

def dimension_reduce(mq, 
                     index_name: str,
                     attribute: str,
                     marqo_search_results: dict =None, 
                     reducer: umap.umap_.UMAP =None, 
                     target_dim: int =2, 
                     visualize: bool =False,
                     inline_output: bool =False
                     ) -> numpy.ndarray:
    """A function to perform dimensionality reduction on the tensors in a particular
    index and for a particular attribute. It also visualizes the reduced tensors if needed
    to aid in visualization tasks.

    Args:
        mq (marqo.client.Client): The marqo client object.
        marqo_search_results (dict, optional): The marqo search results dict. Defaults to None.
        reducer (umap.umap_.UMAP, optional): The UMAP object. Defaults to None.
        index_name (str): The index on which to perform dimensionality reduction. 
        attribute (str): The attribute whose tensors to use. 
        target_dim (int, optional): The required dimension of the reduced embedding. Defaults to 2.
        visualize (bool, optional): Whether to visualize the reduced embedding or just
        return them. Defaults to False.
        inline_output (bool, optional): If working in a notebook, where
        you want to see the results there itself, set this to true. Defaults to False.

    Returns:
        numpy.ndarray: The dimension reduced tensors.
    """
    if marqo_search_results is None:
        marqo_search_results = mq.index(index_name).search(
            "Dummy Search",
            limit=1000
        )
    assert marqo_search_results!=None

    _ids = get_ids_from_results(marqo_search_results)
    _tensors = get_tensors_from_ids(mq, _ids, index_name, attribute)

    if reducer is None:
        import umap
        _reducer = umap.UMAP(n_components=target_dim)
    else:
        _reducer = reducer
    
    _mapper, _dim_reduced_tensors = dimension_reduced_tensors(_reducer, _tensors)
    assert _dim_reduced_tensors.shape[1]==target_dim

    if visualize:
        if target_dim in [2,3]:
            import umap.plot
            _hover_data = get_hover_data_from_ids(mq, _ids, index_name)

            if inline_output:
                umap.plot.output_notebook()

            p = umap.plot.interactive(_mapper, hover_data=_hover_data, point_size=6)
            umap.plot.show(p)
    
    return _dim_reduced_tensors