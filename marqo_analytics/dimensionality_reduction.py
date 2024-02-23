import umap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from marqo_analytics.utility import (
    get_ids_from_results,
    get_tensors_from_ids,
    get_hover_data_from_ids
)
import sklearn.cluster as cluster
import streamlit as st

def plot_embeddings(reduced_embedding, color_by=None, hover_data=None, interactive=True, title=None):
    d = pd.DataFrame(columns=["x", "y", "label"])
    d['x'] = reduced_embedding[:, 0]
    d['y'] = reduced_embedding[:, 1]
    d = pd.concat([d, hover_data], axis=1)
    
    shape = reduced_embedding.shape
    if shape[-1]==3:
        d['z'] = reduced_embedding[:, 2]

    fig = None
    if interactive:
        if shape[-1]==3:
            fig = px.scatter_3d(data_frame=d, x='x', y='y', z='z', color=color_by, title=title, hover_data=d.columns)
        else:
            fig = px.scatter(data_frame=d, x='x', y='y', color=color_by, title=title, hover_data=d.columns)
    else:
        if shape[-1]==3:
            raise ValueError("Currently 3D only in interactive mode")
        else:
            fig = plt.figure()
            sns.scatterplot(d, hue='label', x='x', y='y')
            plt.title(title)
    return fig

@st.cache_data
def dimension_reduced_tensors(
        _reducer: umap.umap_.UMAP, 
        tensors: np.ndarray
        ) -> np.ndarray:
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
    mapper = _reducer.fit(tensors)
    reduced_embedding = mapper.transform(tensors)
    return mapper, reduced_embedding

@st.cache_data
def dimension_reduce(_mq, 
                     index_name: str,
                     attribute: str,
                     marqo_search_results: dict =None, 
                     _reducer: umap.umap_.UMAP =None, 
                     target_dim: int =2, 
                     visualize: bool =False,
                     inline_output: bool =False,
                     num_clusters: int =None,
                     color_by=None,
                     limit=5,
                     ) -> np.ndarray:
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
        num_clusters(int, optional): If specified, clustering will be performed and visualization
        will include color coding as per them, for better insights.

    Returns:
        numpy.ndarray: The dimension reduced tensors.
    """
    marqo_search_results = marqo_search_results
    if marqo_search_results is None:
        marqo_search_results = _mq.index(index_name).search(
            "Dummy Search",
            limit=limit
        )
    assert marqo_search_results!=None

    _ids = get_ids_from_results(marqo_search_results)
    _tensors = get_tensors_from_ids(_mq, _ids, index_name, attribute)
    if _reducer is None:
        import umap
        _reducer = umap.UMAP(n_components=target_dim)
    else:
        _reducer = _reducer
    
    _mapper, _dim_reduced_tensors = dimension_reduced_tensors(_reducer, _tensors)
    assert _dim_reduced_tensors.shape[1]==target_dim

    figure = None
    if visualize:
        if target_dim in [2,3]:
            import umap.plot as upl
            _hover_data = get_hover_data_from_ids(_mq, _ids, index_name)

            if inline_output:
                upl.output_notebook()

            if num_clusters is not None:
                _kmeans_labels = cluster.KMeans(n_clusters=num_clusters).fit_predict(_dim_reduced_tensors)
                # p = upl.interactive(_mapper, hover_data=_hover_data, point_size=6, labels=_kmeans_labels)
                # p = interactive_plotly(_mapper, hover_data=_hover_data, point_size=6, labels=_kmeans_labels)
                p = plot_embeddings(_dim_reduced_tensors, hover_data=_hover_data, color_by=color_by)
                figure = p
            else:
                # p = upl.interactive(_mapper, hover_data=_hover_data, point_size=6)
                # p = interactive_plotly(_mapper, hover_data=_hover_data, point_size=6)
                p = plot_embeddings(_dim_reduced_tensors, hover_data=_hover_data, color_by=color_by)
            # umap.plot.show(p)
                figure = p
    
    return figure, _dim_reduced_tensors