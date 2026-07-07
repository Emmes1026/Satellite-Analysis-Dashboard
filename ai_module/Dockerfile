FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel certifi

RUN pip install --no-cache-dir torch==2.12.1+cpu torchvision==0.27.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu \
    --default-timeout=1000

COPY requirements_worker.txt .
RUN pip install --no-cache-dir -r requirements_worker.txt

COPY . .

CMD ["python", "ai_worker.py"]