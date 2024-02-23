import streamlit as st
import pandas as pd
import marqo
from marqo_analytics.dimensionality_reduction import dimension_reduce


marqo_url = st.text_input(label="Marqo instance URL", value="http://0.0.0.0:8882")
client = marqo.Client(url=marqo_url)

index_name = st.selectbox(label="Index name", options=[i['indexName'] for i in client.get_indexes()['results']])

show_settings = st.checkbox(label="Show index settings and stats", value=False)
settings = client.index(index_name).get_settings()
stats = client.index(index_name).get_stats()
if show_settings:
    data = pd.DataFrame(
        data={'Search Model': settings['model'], 
         'Space type': settings['annParameters']['spaceType'],
        #  'Vector Dimension': settings['modelProperties']['dimensions'],
         'Number of Documents': stats['numberOfDocuments'],
         'Number of vectors': stats['numberOfVectors']}, index=[1])
    data.style.hide_index()
    st.table(data.transpose())

# st.write([1.0 for i in range(settings['model_properties']['dimensions'])])
dummy_result = client.index(index_name).search("Product review", limit=1)

if dummy_result:

    attribute = st.selectbox(label="Vectorized Attribute", options=list(dummy_result['hits'][0].keys()))
    color_by = st.selectbox(label="Color by", options=list(dummy_result['hits'][0].keys()))
    target_dim = st.selectbox(label="Reduced dimension", options=[2,3])
    limit = st.number_input(label="Number of results to fetch", min_value=1, step=1)
    if attribute and color_by:
        fig, reduced_vecs = dimension_reduce(_mq=client, index_name=index_name, 
                                            #  marqo_search_results=dummy_result,
                                            visualize=True, attribute=attribute, target_dim=int(target_dim), color_by=color_by, limit=limit)
        # st.write(type(fig))
        st.plotly_chart(fig)
    else:
        st.write("Please select attribute and color_by")
else:
    st.write("Error fetching results")
