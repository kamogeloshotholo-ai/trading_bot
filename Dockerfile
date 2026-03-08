FROM python:3.11-slim

# Install system dependencies for MetaTrader5
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Download and install MetaTrader5 (assuming demo version; adjust as needed)
# Note: This is a placeholder; actual MT5 installation requires manual setup or specific binaries
# For demo purposes, assume MT5 is pre-installed or use a custom image

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "web_app.py", "--server.headless", "true", "--server.port", "8501"]