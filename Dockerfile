FROM python:3.8-buster

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download es_core_news_lg
RUN python -m nltk.downloader punkt
RUN apt-get update
RUN apt-get -y install graphviz

COPY . .
RUN unzip data/medline.zip -d medline/

CMD ["python", "main.py"]
