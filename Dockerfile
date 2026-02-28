FROM python:3.11-slim

# install system packages: nginx only
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# copy nginx configuration
COPY nginx.conf /etc/nginx/sites-enabled/default

# create working directory
WORKDIR /app

# copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code (including start script)
COPY . .

# make start script executable (it's in /app directory)
RUN chmod +x /app/start.sh

# expose ports
EXPOSE 80 5000

# entrypoint
CMD ["/app/start.sh"]
