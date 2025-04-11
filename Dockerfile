FROM python:3.13.3-slim
USER root
RUN apt-get update && \
    apt-get install -y build-essential
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
