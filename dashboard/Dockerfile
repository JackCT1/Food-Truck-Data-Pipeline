FROM python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY dashboard.py .

EXPOSE 8501

CMD streamlit run dashboard.py