### Repository for analytics processing.

- The dimensionality reduction code is places in `marqo_analytics` directory.
- To use the code, please use the `DR_demo.ipynb` notebook, it contains code to add sample data and visualize it using dimensionality reduction.
- The dimensionality reduction technique currently used is [`umap`](https://github.com/lmcinnes/umap).

#### Installing dependencies
- Run `pip install -r requirements.txt` to install the required packages. 
- For UMAP, run `pip install https://github.com/lmcinnes/umap/archive/master.zip` to install from latest master.
- `umap.plot` requires packages like `datashader`, `pandas`, `matplotlib`, `bokeh`, `holoviews`, `scikit-image`, `colorcet`. Install these separately if they are not getting installed by default, using `pip install pandas matplotlib datashader bokeh holoviews scikit-image colorcet`


### Docker related

Create network
- Run `sudo docker network create marqo_net`

Get URl of docker container:
- Run `sudo docker inspect --format '{{ .NetworkSettings.Networks.<network-name>.IPAddress }}' <container-name>`

Attach container
- Run `sudo docker network connect marqo_net marqo_no_model`
- Run `sudo docker network connect marqo_net streamlit-marqo-app`

- Used `sudo docker build . -t streamlit-marqo-app:v1`  to build image
- Used `sudo docker container run -d -p 8501:8501 streamlit-marqo-app:v1` to run container

To run two contaiers on same network:
- Run `sudo docker run -d --name marqo_no_model --network marqo_net marqoai/marqo:latest`
- Run `sudo docker run -d --name streamlit-marqo-app --network marqo_net streamlit-marqo-app:v1`

To access URL of marqo container in streamlit app:
- Run `http://<container-name>:8882`

Build Image:
- Run `sudo docker build . -t streamlit-marqo-app:v1` from root of this repo.
