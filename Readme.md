### Repository for analytics processing.

- The dimensionality reduction code is places in `marqo_analytics` directory.
- This application can be run using the Dockerfile(use commands below to create containers). Once the container are running, a streamlit app is up and running which can be connected to a marqo instance and view the visualizations.
- `DR_demo.ipynb` notebook contains code to add sample data and visualize it using dimensionality reduction.
- The dimensionality reduction technique currently used is [`umap`](https://github.com/lmcinnes/umap).

### Demo

https://github.com/sky-2002/mq_analytics/assets/84656834/6f9e4617-3256-4269-8124-50c006916c03



#### Installing dependencies
- Run `pip install -r requirements.txt` to install the required packages. 
- For UMAP, run `pip install https://github.com/lmcinnes/umap/archive/master.zip` to install from latest master.
- `umap.plot` requires packages like `datashader`, `pandas`, `matplotlib`, `bokeh`, `holoviews`, `scikit-image`, `colorcet`. Install these separately if they are not getting installed by default, using `pip install pandas matplotlib datashader bokeh holoviews scikit-image colorcet`


### Docker setup

**Pull image**:
- Run `sudo docker pull marqoai/marqo:latest` to pull latest image(marqo version 2.2.0).
- Run 
```
sudo docker run --name <container-name> --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway \
-e MARQO_MODELS_TO_PRELOAD='[]' \  <!-- Specify if any models needed -->
marqoai/marqo:latest <!-- Image name and tag -->
```

Note - For older versions of marqo, use `marqoai/marqo:1.5.0` image, basically change the tag.

**Create network**(the streamlit app container and marqo container should be on same network):
- Run `sudo docker network create marqo_net`

**Get URL/IP of docker container**:
- Run `sudo docker inspect --format '{{ .NetworkSettings.Networks.<network-name>.IPAddress }}' <container-name>`

**Build container from Dockerfile**:
- Used `sudo docker build . -t streamlit-marqo-app:v1`  to build image from root.
- Used `sudo docker container run -d -p 8501:8501 streamlit-marqo-app:v1` to run container.

**Attach containers to network**:
- Run `sudo docker network connect marqo_net marqo_no_model`
- Run `sudo docker network connect marqo_net streamlit-marqo-app`


**To run two contaiers on same network**:
- Run `sudo docker run -d --name marqo_no_model --network marqo_net marqoai/marqo:latest`
- Run `sudo docker run -d --name streamlit-marqo-app --network marqo_net streamlit-marqo-app:v1`

**To access URL of marqo container in streamlit app**:
- Run `http://<container-name>:8882`

**Build Image**:
- Run `sudo docker build . -t streamlit-marqo-app:v1` from root of this repo.
