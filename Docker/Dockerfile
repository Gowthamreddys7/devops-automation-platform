FROM python:3.12-slim

WORKDIR /usr/app

COPY application/ .

RUN pip install -r requirements.txt
 
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
