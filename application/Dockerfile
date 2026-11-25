FROM python:3.12-slim
WORKDIR /usr/app/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
