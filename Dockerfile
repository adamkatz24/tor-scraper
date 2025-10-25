FROM python:3.12-slim

# Install system dependencies and Chrome dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    tree \
    privoxy \
    tor \
    dos2unix \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

RUN pip install uv

COPY requirements.txt . 
# Install Python packages
RUN uv pip install -r requirements.txt --system
RUN uv pip install anthropic==0.51.0 --system

# Create necessary directories with proper permissions
RUN mkdir -p /var/lib/scrapyd/eggs \
    /var/lib/scrapyd/logs \
    /var/lib/scrapyd/items \
    /var/lib/scrapyd/dbs \
    && chmod -R 777 /var/lib/scrapyd

# Create and set permissions for projects directory
RUN mkdir -p /app/native && chmod -R 777 /app

# Copy configuration files
COPY scrapyd.conf /etc/scrapyd/
COPY scrapydweb_settings_v11.py /app/

# Copy the Scrapy project
COPY native /app/projects/native/
RUN chmod -R 777 /app/projects/native/

# Create a startup script that ensures correct startup order and debug info
COPY start.sh /app/start.sh

COPY privoxy.config /etc/privoxy/config

RUN dos2unix /app/start.sh
RUN chmod +x ./start.sh

# Expose ports
EXPOSE 6800 
EXPOSE 5000 

CMD ["bash", "/app/start.sh"]
