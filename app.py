import streamlit as st
import pandas as pd
import marqo
from marqo_analytics.dimensionality_reduction import dimension_reduce


marqo_url = st.text_input(label="Marqo instance URL", value="http://0.0.0.0:8882")
client = marqo.Client(url=marqo_url)

index_name = st.selectbox(label="Index name", options=[i.index_name for i in client.get_indexes()['results']])

show_settings = st.checkbox(label="Show index settings and stats", value=False)
settings = client.index(index_name).get_settings()['index_defaults']
stats = client.index(index_name).get_stats()
if show_settings:
    data = pd.DataFrame(
        data={'Search Model': settings['search_model'], 
         'Space type': settings['ann_parameters']['space_type'],
         'Vector Dimension': settings['model_properties']['dimensions'],
         'Number of Documents': stats['numberOfDocuments'],
         'Number of vectors': stats['numberOfVectors']}, index=[1])
    data.style.hide_index()
    st.table(data.transpose())

# st.write([1.0 for i in range(settings['model_properties']['dimensions'])])
dummy_result = client.index(index_name).search(
    context={'tensor':[{'vector':[1.0 for i in range(settings['model_properties']['dimensions'])], 'weight':1.0}]},
    limit=stats['numberOfVectors']
)
# st.write(dummy_result)

attribute = st.selectbox(label="Attribute", options=list(dummy_result['hits'][0].keys()))
color_by = st.selectbox(label="Color by", options=list(dummy_result['hits'][0].keys()))
target_dim = st.selectbox(label="Reduced dimension", options=[2,3])
fig, reduced_vecs = dimension_reduce(mq=client, index_name=index_name, 
                                     marqo_search_results=dummy_result,
                                     visualize=True, attribute=attribute, target_dim=int(target_dim), color_by=color_by)
# st.write(type(fig))
st.plotly_chart(fig)
