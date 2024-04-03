FROM python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY pipeline.py .
COPY extract.py .
COPY transform.py .
COPY load.py .

RUN mkdir data

CMD python3 pipeline.py