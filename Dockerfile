FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt
 

COPY . /app

# EXPOSE 8000

CMD ["streamlit", "run", "--server.port", "80", "stream.py"]