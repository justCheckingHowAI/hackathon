FROM python:3.12-slim

WORKDIR /api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /api/start-api.sh /api/start-worker.sh

EXPOSE 80

CMD ["/api/start-api.sh"]
