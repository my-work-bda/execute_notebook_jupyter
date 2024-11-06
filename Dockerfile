FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]

# docker build -t flask-api-execute:v1 .
# docker run -p 5000:5000 flask-api-execute:v1