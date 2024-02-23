FROM python:3.11.4-slim

RUN mkdir ./work
WORKDIR ./work

COPY ./requirements.txt /work/requirements.txt

RUN pip3 install -r /work/requirements.txt

COPY ./marqo_analytics /work/marqo_analytics
COPY ./app.py /work/app.py
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]